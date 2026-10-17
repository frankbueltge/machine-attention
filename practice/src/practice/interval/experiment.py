"""The Interval V0, increment 6: the E-experiment's tally.

The acceptance criteria are committed before the window opens
(`interval/experiment.json`, the prose in
docs/2026-10-14-the-interval-e-experiment-kriterien.md); they bind once
committed. This module only counts what the committed weekly readings show
against the criteria that can be counted from them (A1-A3, B1, B2), and
B6, the base rate, from the committed register (addendum of 2026-10-17,
docs/2026-10-17-the-interval-e-experiment-nachtrag.md). It decides nothing: the review after the window is the maintainer's.

    python -m practice.interval.experiment --repo-root .
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from ..preserve import read_json
from . import money
from .register import REGISTER
from .weekly import READINGS

EXPERIMENT = "interval/experiment.json"
SCHEMA = "interval-experiment-v1"
FAILED = ("unavailable", "incomplete")
# B6 (addendum of 2026-10-17): the gap a short response is read against.
B6_MAX_GAP = 1


def iso_week(day: str) -> tuple[int, int]:
    return dt.date.fromisoformat(day).isocalendar()[:2]


def readings(root: Path) -> list[dict]:
    return [read_json(p) for p in sorted((root / READINGS).glob("*.json"))]


def failures(reading: dict) -> list[str]:
    """What a reading could not get: the IPC step or a fetched query that
    ended unavailable or incomplete."""
    out = []
    if reading["ipc"].get("status") == "unavailable":
        out.append("ipc unavailable")
    for q in reading["queries"]:
        if q.get("outcome") in FAILED:
            out.append(f"{q['country']} {q['t0']} {q['set']} {q['outcome']}")
    return out


def frozen_moves(all_readings: list[dict]) -> list[str]:
    """B1: a frozen query stays frozen on the same basis day. Readings in
    date order; an episode that leaves the IPC table is not a move (B2
    reports it)."""
    seen: dict[tuple, str] = {}
    moves = []
    for r in all_readings:
        for q in r["queries"]:
            key = (q["country"], q["t0"], q["set"])
            if key in seen and (q["decision"] != "frozen"
                                or q["basis_day"] != seen[key]):
                moves.append(f"{r['date']}: {' '.join(key)} frozen on "
                             f"{seen[key]}, now {q['decision']} on "
                             f"{q['basis_day']}")
            if q["decision"] == "frozen":
                seen.setdefault(key, q["basis_day"])
    return moves


def episode_changes(all_readings: list[dict]) -> list[str]:
    """B2, reported: episodes that appear or vanish between readings."""
    out = []
    prev = None
    for r in all_readings:
        now = {(q["country"], q["t0"]) for q in r["queries"]}
        if prev is not None:
            out += [f"{r['date']}: + {c} {t0}" for c, t0 in sorted(now - prev)]
            out += [f"{r['date']}: - {c} {t0}" for c, t0 in sorted(prev - now)]
        prev = now
    return out


def base_rate(root: Path, register: dict) -> dict:
    """B6, reported, no bar (addendum of 2026-10-17): the same t1 rule at
    every other month of each onset year, as placebo onsets, against the
    real onsets, per cell set x axis x k. Reads only the pages the
    committed register names, so it fetches nothing and cannot touch A3.
    An episode whose window spans fewer than three years has no full onset
    year inside its boundary and is left out (both columns). The placebo
    months come from crisis years themselves: a base rate inside them, not
    across calm ones."""
    cells: dict[str, dict] = {}
    for e in register["episodes"]:
        for tag, side in e["money"].items():
            if side.get("status") != "read":
                continue
            years = side["boundary_years"].split(",")
            if len(years) < 3:
                continue
            flows = money.parse_flows([(root / p).read_bytes()
                                       for p in side["pages"]])
            for axis in money.AXES:
                for k in money.KS:
                    c = cells.setdefault(f"{tag} {axis} k={k}", {
                        "placebo_short": 0, "placebo_n": 0,
                        "onset_short": 0, "onset_n": 0})
                    for mo in range(1, 13):
                        t0 = f"{years[1]}-{mo:02d}"
                        r = money.response(flows, t0, k, axis, side["as_of"])
                        short = (r.status == "closed"
                                 and r.gap <= B6_MAX_GAP)
                        col = "onset" if t0 == e["t0"] else "placebo"
                        c[f"{col}_n"] += 1
                        c[f"{col}_short"] += short
    return {"max_gap_months": B6_MAX_GAP, "cells": cells}


def tally(experiment: dict, all_readings: list[dict], today: str) -> dict:
    weeks = experiment["window"]["weeks"]
    by_week: dict[tuple, list[dict]] = {}
    for r in all_readings:
        by_week.setdefault(iso_week(r["date"]), []).append(r)
    window = [r for w in weeks for r in by_week.get(iso_week(w), [])[:1]]
    due = [w for w in weeks if w <= today]
    missing = [w for w in due if iso_week(w) not in by_week]
    failed = {r["date"]: failures(r) for r in window if failures(r)}
    throttled = [r["date"] for r in window if r.get("http_429")]
    pre = [r for r in all_readings if r["date"] < weeks[0]]
    moves = frozen_moves(pre + window)
    return {
        "weeks_due": len(due), "weeks_total": len(weeks),
        "closed": today > experiment["window"]["closes"],
        "A1_missing_weeks": missing,
        "A2_readings_with_failures": failed,
        "A2_pass": len(failed) <= experiment["criteria"]["A2_max_failed_readings"],
        "A3_http_429": throttled,
        "B1_frozen_moves": moves,
        "B2_episode_changes": episode_changes(pre[-1:] + window),
        "episodes": [r["episodes"] for r in window],
    }


def full_tally(root: Path, today: str) -> dict:
    out = tally(read_json(root / EXPERIMENT), readings(root), today)
    register = root / REGISTER
    out["B6_base_rate"] = (base_rate(root, read_json(register))
                           if register.exists() else None)
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="The Interval's E-tally")
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--today", default=dt.datetime.now(dt.timezone.utc)
                        .strftime("%Y-%m-%d"))
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    out = full_tally(root, args.today)
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
