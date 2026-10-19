"""Planetary Listening, V0 increment 4: the E-experiment's tally.

The acceptance criteria are committed before the window opens
(`planetary/experiment.json`, the prose in
docs/2026-10-19-planetary-listening-e-experiment-kriterien.md); they bind
once committed. This module only counts what the committed nightly readings
show against them: A1-A4, B1-B6 and the class words of C. It decides nothing:
the review after the window is the maintainer's.

B4, the clock test, is the one question the window can answer that no single
night can: Germany leaves summer time on 2026-10-25. If the weekday impulse
keeps a local clock, its UTC onset moves an hour later; if it keeps UTC, it
stays. Reported, no bar.

    python -m practice.planetary.experiment --repo-root .
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import statistics
from pathlib import Path

from ..preserve import read_json
from .nightly import BASE, READINGS

EXPERIMENT = "planetary/experiment.json"
SCHEMA = "planetary-experiment-v1"
# C: no record names a class (audit, "Bewusst nicht"; E-2).
CLASS_WORDS = ("blast", "sprengung", "explosion", "quarry")
# The request ledger quotes publishers' URLs verbatim; their words are not
# the machine's class.
_LEDGER_KEYS = ("requests",)


def nights(experiment: dict) -> list[str]:
    w = experiment["window"]
    first = dt.date.fromisoformat(w["first"])
    return [(first + dt.timedelta(days=i)).isoformat()
            for i in range(w["nights"])]


def readings(root: Path) -> list[dict]:
    return [read_json(p) for p in sorted((root / READINGS).glob("*.json"))]


def failures(reading: dict) -> list[str]:
    """A2: what a night could not get — the day file, the extent, or a
    catalogue answer. The publisher's day documents are B1, not A2."""
    out = []
    sd = reading.get("station_day", {})
    if sd.get("outage") or sd.get("http_status") != 200:
        out.append(f"day file {sd.get('http_status')}")
    if reading["publisher"]["extent"].get("http_status") != 200:
        out.append(f"extent {reading['publisher']['extent'].get('http_status')}")
    for c in reading.get("catalogues", []):
        if c.get("http_status") not in (200, 204):
            out.append(f"{c['catalogue']} {c.get('http_status')}")
    return out


def night_bytes(root: Path, reading: dict) -> int:
    """A4: what the night adds to the repository — its snapshots and the
    reading itself."""
    folder = root / BASE / reading["date"]
    snaps = sum(p.stat().st_size for p in folder.rglob("*") if p.is_file()) \
        if folder.exists() else 0
    path = root / READINGS / f"{reading['date']}.json"
    return snaps + (path.stat().st_size if path.exists() else 0)


def attest(reading: dict) -> bool:
    """B1: the publisher's own day documents for the read day arrived."""
    p = reading["publisher"]
    return (p["availability"].get("http_status") == 200
            and p["wfcatalog"].get("http_status") == 200)


def first_strong(reading: dict) -> str | None:
    strong = reading.get("station_day", {}).get("strong") or []
    return min((s["onset"] for s in strong), default=None)


def calendar_line(reading: dict) -> dict:
    """B3 and B5: one line per read day — the strong impulses and what the
    public catalogues held for the same day and box."""
    sd = reading.get("station_day", {})
    return {"day": reading["day"],
            "weekday": dt.date.fromisoformat(reading["day"]).strftime("%a"),
            "strong": [[s["onset"][11:19], s["peak_ratio"]]
                       for s in sd.get("strong") or []],
            "catalogue_rows": {c["catalogue"]: c.get("rows")
                               for c in reading.get("catalogues", [])}}


def _minutes(onset: str) -> float:
    t = dt.datetime.fromisoformat(onset)
    return t.hour * 60 + t.minute + t.second / 60


def clock_test(all_readings: list[dict], rule: dict) -> dict:
    """B4: the median UTC minute of each weekday's first strong impulse,
    before and after the shift day, every committed reading counted. A side
    with fewer than `min_days_each_side` days is undetermined."""
    shift = rule["shift_day"]
    before, after = [], []
    for r in all_readings:
        onset = first_strong(r)
        if onset is None or dt.date.fromisoformat(r["day"]).weekday() > 4:
            continue
        (before if r["day"] < shift else after).append(_minutes(onset))
    out = {"days_before": len(before), "days_after": len(after),
           "verdict": "undetermined", "delta_min": None}
    if min(len(before), len(after)) < rule["min_days_each_side"]:
        return out
    delta = statistics.median(after) - statistics.median(before)
    tol = rule["tolerance_min"]
    out["delta_min"] = round(delta, 2)
    if abs(delta - 60) <= tol:
        out["verdict"] = "local"
    elif abs(delta) <= tol:
        out["verdict"] = "utc"
    else:
        out["verdict"] = "neither"
    return out


def class_words(reading: dict) -> list[str]:
    """C: words of a class anywhere in the record outside the verbatim
    request ledger."""
    text = json.dumps({k: v for k, v in reading.items()
                       if k not in _LEDGER_KEYS}).lower()
    return [w for w in CLASS_WORDS if w in text]


def tally(experiment: dict, all_readings: list[dict], today: str,
          sizes: dict[str, int] | None = None) -> dict:
    window_nights = nights(experiment)
    by_date = {r["date"]: r for r in all_readings}
    window = [by_date[n] for n in window_nights if n in by_date]
    due = [n for n in window_nights if n <= today]
    missing = [n for n in due if n not in by_date]
    run = longest = 0
    for n in due:
        run = run + 1 if n in missing else 0
        longest = max(longest, run)
    c = experiment["criteria"]
    failed = {r["date"]: failures(r) for r in window if failures(r)}
    throttled = sorted({r["date"] for r in window
                        for q in r.get("requests", [])
                        if q.get("http_status") == 429})
    sizes = sizes or {}
    heavy = {d: b for d, b in sizes.items()
             if d in window_nights and b > c["A4_max_night_bytes"]}
    detector_changes = [
        r["date"] for r in window
        if r.get("detector") != c["B6_detector"]
        or r.get("strong_ratio") != c["B6_strong_ratio"]
        or r.get("max_excerpts_per_station_day") != c["B6_max_excerpts"]]
    return {
        "nights_due": len(due), "nights_total": len(window_nights),
        "closed": today > experiment["window"]["closes"],
        "A1_missing_nights": missing,
        "A1_pass": (len(window_nights) - len(missing) >= c["A1_min_nights"]
                    and longest <= c["A1_max_consecutive_missing"]),
        "A2_nights_with_failures": failed,
        "A2_pass": len(failed) <= c["A2_max_failed_nights"],
        "A3_http_429": throttled,
        "A4_nights_over_budget": heavy,
        "B1_attest_present": [r["date"] for r in window if attest(r)],
        "B1_attest_missing": [r["date"] for r in window if not attest(r)],
        "B2_reingestion_events": {r["date"]: r["reingestion"]["events"]
                                  for r in window
                                  if r["reingestion"].get("events")},
        "B3_B5_calendar": [calendar_line(r) for r in window],
        "B4_clock": clock_test(all_readings, experiment["clock_test"]),
        "B6_detector_changes": detector_changes,
        "C_class_words": {r["date"]: class_words(r) for r in window
                          if class_words(r)},
    }


def full_tally(root: Path, today: str) -> dict:
    all_readings = readings(root)
    sizes = {r["date"]: night_bytes(root, r) for r in all_readings}
    return tally(read_json(root / EXPERIMENT), all_readings, today, sizes)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Planetary Listening's E-tally")
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--today", default=dt.datetime.now(dt.timezone.utc)
                        .strftime("%Y-%m-%d"))
    args = parser.parse_args(argv)
    out = full_tally(args.repo_root.resolve(), args.today)
    print(json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
