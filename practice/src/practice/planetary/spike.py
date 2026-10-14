"""Planetary Listening, V0 increment 1: the spike that decides the pairing.

Audit 2026-08-22, condition 1: detectability is measured before any window,
not assumed. Two pairings are measured with one detector:

  A  Rüdersdorf — GE.RUE on the works' own ground; the declaration side is
     the public event catalogues (ISC, USGS), which the audit measured empty.
  B  Geseke — the operator's own public blasting calendar; nearest open
     station GR.KAST, ~49 km away.

Storage model (audit condition 2): day files are fetched, hashed and
discarded; only the request ledger (literal URL per node, status, size,
SHA-256) and at most MAX_EXCERPTS record-aligned excerpts per station-day are
committed. An excerpt is a byte-identical subset of the publisher's file.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from ..fetch import Client
from ..preserve import Snapshot, sha256, utc_now, write_json
from . import detect, mseed

BASE = "planetary/probes"
READINGS = "planetary/spike"
MAX_EXCERPTS = 4
EXCERPT_BEFORE_S = 30
EXCERPT_AFTER_S = 60
# Licence filter (audit condition 3): only CC BY 4.0 networks, DOI per record.
NETWORKS = {
    "GE": {"licence": "CC-BY-4.0", "doi": "10.14470/TR560404",
           "node": "https://geofon.gfz.de/fdsnws/dataselect/1/query"},
    "GR": {"licence": "CC-BY-4.0", "doi": "10.25928/mbx6-hr74",
           "node": "https://eida.bgr.de/fdsnws/dataselect/1/query"},
}
MSEED = {"Accept": "application/vnd.fdsn.mseed"}

RUE_DAYS = [f"2026-10-{d:02d}" for d in range(5, 12)]   # Mon..Sun
# The operator page as read 2026-10-14 lists these ten dates and nothing
# later; the window "in der Regel zwischen 10:00 und 12:00 Uhr" is local
# summer time, i.e. 08:00-10:00 UTC.
GESEKE_DECLARED = ["2025-07-28", "2025-07-31", "2025-08-01", "2025-08-04",
                   "2025-08-07", "2025-08-11", "2025-08-15", "2025-08-18",
                   "2025-08-25", "2025-08-28"]
# Weekdays inside the same span with no declared date.
GESEKE_CONTROL = ["2025-07-29", "2025-07-30", "2025-08-05", "2025-08-06",
                  "2025-08-12", "2025-08-13", "2025-08-19", "2025-08-20",
                  "2025-08-26", "2025-08-27"]
GESEKE_WINDOW_UTC = ("08:00", "10:00")
STRONG_RATIO = 50.0
# Catalogue boxes (lat0, lat1, lon0, lon1), as in the audit: ~1 x 1.2 degrees.
BOX_A = (51.9, 52.9, 13.2, 14.4)
BOX_B = (51.1, 52.1, 7.9, 9.1)


def dataselect_url(net: str, sta: str, cha: str, start: str, end: str) -> str:
    """The literal request per node (audit finding 2: the FDSN query is not
    portable — GEOFON takes the short form, BGR only `location=--` long form)."""
    node = NETWORKS[net]["node"]
    if net == "GE":
        return f"{node}?net={net}&sta={sta}&loc=--&cha={cha}&start={start}&end={end}"
    return (f"{node}?network={net}&station={sta}&location=--&channel={cha}"
            f"&starttime={start}&endtime={end}")


def isc_url(start: str, end: str, box: tuple[float, float, float, float]) -> str:
    lat0, lat1, lon0, lon1 = box
    return ("https://www.isc.ac.uk/fdsnws/event/1/query?"
            f"starttime={start}&endtime={end}&minlatitude={lat0}&maxlatitude={lat1}"
            f"&minlongitude={lon0}&maxlongitude={lon1}&format=text")


def usgs_url(start: str, end: str, box: tuple[float, float, float, float]) -> str:
    lat0, lat1, lon0, lon1 = box
    return ("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
            f"&starttime={start}&endtime={end}&minlatitude={lat0}&maxlatitude={lat1}"
            f"&minlongitude={lon0}&maxlongitude={lon1}")


def analyse(data: bytes, channel: str) -> tuple[list[detect.Trigger], dict]:
    """Triggers over every contiguous trace, plus what the bytes held."""
    found: list[detect.Trigger] = []
    tr = mseed.traces(data, channel)
    for t in tr:
        found.extend(detect.triggers(detect.envelope(t.samples, t.sample_rate),
                                     t.start))
    # Overlapping traces in the publisher's file can repeat a trigger.
    unique = {t.onset: t for t in found}
    found = sorted(unique.values(), key=lambda t: t.onset)
    return found, {"traces": len(tr), "samples": sum(len(t.samples) for t in tr)}


def _next_day(day: str) -> str:
    return (date.fromisoformat(day) + timedelta(days=1)).isoformat()


def _parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def _station_day(client, snap: Snapshot, ledger: list, net: str, sta: str,
                 cha: str, start: str, end: str, tag: str,
                 within: tuple[str, str] | None = None) -> dict:
    url = dataselect_url(net, sta, cha, start, end)
    data, status = client.fetch(url, headers=MSEED)
    ledger.append({"url": url, "retrieved_at": utc_now(), "http_status": status,
                   "bytes": len(data), "sha256": sha256(data),
                   "committed": False})
    day = {"station": f"{net}.{sta}..{cha}", "day": tag, "http_status": status,
           "request_sha256": sha256(data), "licence": NETWORKS[net]["licence"],
           "doi": NETWORKS[net]["doi"]}
    if status != 200 or not data:
        day.update({"triggers": [], "outage": True})
        return day
    trig, held = analyse(data, cha)
    if within:
        trig = [t for t in trig if within[0] <= t.onset[11:16] < within[1]]
    strongest = sorted(trig, key=lambda t: -t.peak_ratio)
    excerpts = []
    for t in strongest[:MAX_EXCERPTS]:
        if t.peak_ratio < STRONG_RATIO:
            break   # weak impulses stay re-fetchable through the ledger
        onset = _parse(t.onset)
        cut = mseed.excerpt(data, onset - timedelta(seconds=EXCERPT_BEFORE_S),
                            onset + timedelta(seconds=EXCERPT_AFTER_S))
        name = f"{net}.{sta}.{cha}/{onset.strftime('%Y%m%dT%H%M%S')}.mseed"
        entry = snap.preserve(name, cut, url, status)
        excerpts.append({"onset": t.onset, "file": entry["file"]})
    day.update(held)
    day.update({
        "outage": False,
        "triggers": len(trig),
        "strong": [t.to_dict() for t in strongest if t.peak_ratio >= STRONG_RATIO],
        "top": [t.to_dict() for t in strongest[:3]],
        "excerpts": excerpts,
    })
    return day


def run(repo_root: Path, client=None, today: str | None = None) -> dict:
    client = client or Client()
    today = today or date.today().isoformat()
    snap = Snapshot(repo_root, today, base=BASE)
    ledger: list[dict] = []

    rue = []
    for d in RUE_DAYS:
        nxt = _next_day(d)
        rue.append(_station_day(client, snap, ledger, "GE", "RUE", "HHZ",
                                f"{d}T00:00:00", f"{nxt}T00:00:00", d))
    kast = []
    for d in sorted(GESEKE_DECLARED + GESEKE_CONTROL):
        row = _station_day(client, snap, ledger, "GR", "KAST", "HHZ",
                           f"{d}T07:00:00", f"{d}T11:00:00", d,
                           within=GESEKE_WINDOW_UTC)
        row["declared"] = d in GESEKE_DECLARED
        kast.append(row)

    catalogues = []
    spans = []
    if RUE_DAYS:
        spans.append(("A", RUE_DAYS[0], _next_day(RUE_DAYS[-1]), BOX_A))
    geseke = sorted(GESEKE_DECLARED + GESEKE_CONTROL)
    if geseke:
        spans.append(("B", geseke[0], _next_day(geseke[-1]), BOX_B))
    for label, start, end, box in spans:
        for name, url in (("ISC", isc_url(start, end, box)),
                          ("USGS", usgs_url(start, end, box))):
            data, status = client.fetch(url)
            ledger.append({"url": url, "retrieved_at": utc_now(),
                           "http_status": status, "bytes": len(data),
                           "sha256": sha256(data), "committed": False})
            rows = None
            if status == 204:
                rows = 0
            elif status == 200 and name == "ISC":
                rows = sum(1 for line in data.decode("utf-8", "replace").splitlines()
                           if line and not line.startswith("#"))
            elif status == 200:
                rows = data.count(b'"type":"Feature"')
            catalogues.append({"pairing": label, "catalogue": name,
                               "http_status": status, "rows": rows,
                               "box": list(box), "span": [start, end]})

    snap.write_manifest()
    reading = {
        "schema": "planetary-spike-v1", "date": today,
        "detector": detect.parameters(), "strong_ratio": STRONG_RATIO,
        "excerpt_window_s": [EXCERPT_BEFORE_S, EXCERPT_AFTER_S],
        "max_excerpts_per_station_day": MAX_EXCERPTS,
        "pairing_a": {"site": "Rüdersdorf", "station": "GE.RUE..HHZ", "days": rue},
        "pairing_b": {"site": "Geseke", "station": "GR.KAST..HHZ",
                      "window_utc": list(GESEKE_WINDOW_UTC), "days": kast},
        "catalogues": catalogues,
        "requests": ledger,
    }
    write_json(repo_root / READINGS / f"{today}.json", reading)
    return reading


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--date", default=None)
    args = parser.parse_args(argv)
    reading = run(args.repo_root.resolve(), today=args.date)
    for row in reading["pairing_a"]["days"] + reading["pairing_b"]["days"]:
        print(row["station"], row["day"], row.get("declared", ""),
              row["triggers"] if not row.get("outage") else "outage",
              len(row.get("strong", [])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
