"""Planetary Listening, V0 increment 2: the nightly T+1 reading for GE.RUE.

Pairing A (Rüdersdorf) was chosen by the spike of 2026-10-14
(docs/2026-10-14-planetary-listening-v0-inkrement-1.md). Each night reads the
previous UTC day of GE.RUE..HHZ under the storage model of audit condition 2:
the day file is fetched, hashed and discarded; at most MAX_EXCERPTS
record-aligned excerpts of strong impulses are kept, byte-identical to the
publisher's file.

Beside the waveform, three small publisher documents are preserved verbatim
(audit finding 2: the publisher certifies nothing, but dates its rewrites):

  availability  `show=latestupdate` for the read day — the `Updated` line
  extent        every segment of the channel's history with its `Updated`
  wfcatalog     the publisher's own day document (records, gaps, RMS)

Re-ingestion is the event this probe exists for: a segment of the extent that
was already closed in the previous reading and now carries a different
`Updated` has been rewritten by the archive. The open segment (the one that
reaches the read day) is updated every night by appending and is not an event.
Events are compared, never inferred: the first reading is a baseline.

Catalogues (ISC, USGS) are queried for the same day and box as the spike. An
impulse is an impulse; no record carries a class (audit, "Bewusst nicht").
"""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

from ..fetch import Client
from ..preserve import Snapshot, read_json, sha256, utc_now, write_json
from . import detect, spike

BASE = "planetary/snapshots"
READINGS = "planetary/readings"
SCHEMA = "planetary-reading-v1"
NET, STA, CHA = "GE", "RUE", "HHZ"
GEOFON = "https://geofon.gfz.de"
TEXT = {"Accept": "text/plain"}


def availability_url(day: str, nxt: str) -> str:
    return (f"{GEOFON}/fdsnws/availability/1/query?net={NET}&sta={STA}&loc=--"
            f"&cha={CHA}&start={day}T00:00:00&end={nxt}T00:00:00"
            "&show=latestupdate&format=text")


def extent_url() -> str:
    return (f"{GEOFON}/fdsnws/availability/1/extent?net={NET}&sta={STA}&loc=--"
            f"&cha={CHA}&show=latestupdate&format=text")


def wfcatalog_url(day: str, nxt: str) -> str:
    return (f"{GEOFON}/eidaws/wfcatalog/1/query?network={NET}&station={STA}"
            f"&location=--&channel={CHA}&start={day}&end={nxt}&include=sample")


def parse_table(data: bytes) -> list[dict]:
    """The FDSN availability text table: a `#` header, whitespace columns."""
    lines = data.decode("utf-8", "replace").splitlines()
    if not lines or not lines[0].startswith("#"):
        return []
    keys = lines[0].lstrip("#").split()
    rows = []
    for line in lines[1:]:
        cells = line.split()
        if len(cells) == len(keys):
            rows.append(dict(zip(keys, cells)))
    return rows


WF_FIELDS = ("num_records", "num_gaps", "num_overlaps", "percent_availability",
             "sample_rms", "quality", "start_time", "end_time")


def parse_wfcatalog(data: bytes) -> dict | None:
    try:
        docs = json.loads(data)
    except ValueError:
        return None
    if not isinstance(docs, list) or len(docs) != 1:
        return None
    doc = docs[0]
    out = {k: doc.get(k) for k in WF_FIELDS}
    out["producer_created"] = (doc.get("producer") or {}).get("created")
    return out


def _segment_key(row: dict) -> str:
    return f"{row.get('Quality')}|{row.get('SampleRate')}|{row.get('Earliest')}"


def reingestion(previous: list[dict] | None, current: list[dict]) -> list[dict]:
    """Segments closed in the previous extent whose `Updated` moved, which
    vanished, or which appeared before the previous open segment began. The
    open segment (latest `Latest`) of the previous extent grows nightly and
    is excluded; a segment that starts after it is new data, not a rewrite."""
    if previous is None:
        return []
    open_row = max(previous, key=lambda r: r.get("Latest", ""), default=None)
    open_key = _segment_key(open_row) if open_row else None
    known = {_segment_key(r) for r in previous}
    now = {_segment_key(r): r for r in current}
    events = []
    for row in previous:
        key = _segment_key(row)
        if key == open_key:
            continue
        cur = now.get(key)
        if cur is None:
            events.append({"kind": "segment_gone", "segment": key,
                           "updated_before": row.get("Updated")})
        elif cur.get("Updated") != row.get("Updated") \
                or cur.get("Latest") != row.get("Latest"):
            events.append({"kind": "segment_rewritten", "segment": key,
                           "updated_before": row.get("Updated"),
                           "updated_now": cur.get("Updated"),
                           "latest_before": row.get("Latest"),
                           "latest_now": cur.get("Latest")})
    for row in current:
        if _segment_key(row) not in known and open_row \
                and row.get("Earliest", "") < open_row.get("Earliest", ""):
            events.append({"kind": "segment_inserted",
                           "segment": _segment_key(row),
                           "updated_now": row.get("Updated")})
    return events


def previous_reading(repo_root: Path, today: str) -> dict | None:
    """The newest earlier reading that holds an extent to compare against."""
    folder = repo_root / READINGS
    older = sorted(p for p in folder.glob("*.json") if p.stem < today) \
        if folder.exists() else []
    for path in reversed(older):
        reading = read_json(path)
        if (reading.get("publisher", {}).get("extent") or {}).get("rows") is not None:
            return reading
    return None


def _document(client, snap: Snapshot, ledger: list, url: str, name: str,
              headers: dict | None = None) -> tuple[bytes, int, str | None]:
    data, status = client.fetch(url, headers=headers)
    ledger.append({"url": url, "retrieved_at": utc_now(), "http_status": status,
                   "bytes": len(data), "sha256": sha256(data),
                   "committed": status == 200 and bool(data)})
    if status != 200 or not data:
        return data, status, None
    return data, status, snap.preserve(name, data, url, status)["file"]


def run(repo_root: Path, client=None, today: str | None = None) -> dict:
    today = today or date.today().isoformat()
    existing = repo_root / READINGS / f"{today}.json"
    if existing.exists():
        # A night that already has its reading is never read again: the manifest beside it may
        # be stamped in the anchor ledger, and a second fetch would rewrite it (2026-10-16).
        return read_json(existing)
    client = client or Client()
    day = (date.fromisoformat(today) - timedelta(days=1)).isoformat()
    nxt = today
    snap = Snapshot(repo_root, today, base=BASE)
    ledger: list[dict] = []

    # The excerpts are written by the spike's day routine; it records the
    # day file in the ledger as fetched-hashed-discarded (committed: false).
    station_day = spike._station_day(client, snap, ledger, NET, STA, CHA,
                                     f"{day}T00:00:00", f"{nxt}T00:00:00", day)

    prefix = f"{NET}.{STA}.{CHA}"
    av_bytes, av_status, av_file = _document(
        client, snap, ledger, availability_url(day, nxt),
        f"{prefix}/availability-{day}.txt", TEXT)
    ex_bytes, ex_status, ex_file = _document(
        client, snap, ledger, extent_url(), f"{prefix}/extent.txt", TEXT)
    wf_bytes, wf_status, wf_file = _document(
        client, snap, ledger, wfcatalog_url(day, nxt),
        f"{prefix}/wfcatalog-{day}.json")

    extent = parse_table(ex_bytes) if ex_file else None
    prev = previous_reading(repo_root, today)
    prev_extent = (prev or {}).get("publisher", {}).get("extent", {}).get("rows")
    publisher = {
        "availability": {"http_status": av_status, "file": av_file,
                         "rows": parse_table(av_bytes) if av_file else None},
        "extent": {"http_status": ex_status, "file": ex_file, "rows": extent},
        "wfcatalog": {"http_status": wf_status, "file": wf_file,
                      "day": parse_wfcatalog(wf_bytes) if wf_file else None},
    }
    reingest = {
        "compared_with": f"{READINGS}/{prev['date']}.json"
        if prev and prev_extent is not None else None,
        "events": reingestion(prev_extent, extent)
        if extent is not None and prev_extent is not None else [],
    }
    if extent is not None and prev_extent is None:
        reingest["baseline"] = True
    if extent is None:
        reingest["unverifiable"] = "extent not read tonight"

    catalogues = []
    for name, url in (("ISC", spike.isc_url(day, nxt, spike.BOX_A)),
                      ("USGS", spike.usgs_url(day, nxt, spike.BOX_A))):
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
        catalogues.append({"catalogue": name, "http_status": status,
                           "rows": rows, "box": list(spike.BOX_A),
                           "span": [day, nxt]})

    snap.write_manifest()
    reading = {
        "schema": SCHEMA, "date": today, "day": day,
        "site": "Rüdersdorf", "station": station_day["station"],
        "detector": detect.parameters(), "strong_ratio": spike.STRONG_RATIO,
        "excerpt_window_s": [spike.EXCERPT_BEFORE_S, spike.EXCERPT_AFTER_S],
        "max_excerpts_per_station_day": spike.MAX_EXCERPTS,
        "station_day": station_day,
        "publisher": publisher,
        "reingestion": reingest,
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
    r = run(args.repo_root.resolve(), today=args.date)
    sd = r["station_day"]
    print(sd["station"], r["day"],
          "outage" if sd.get("outage") else f"{sd['triggers']} triggers, "
          f"{len(sd.get('strong', []))} strong",
          f"reingestion events: {len(r['reingestion']['events'])}",
          "catalogues:", {c["catalogue"]: c["rows"] for c in r["catalogues"]})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
