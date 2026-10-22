"""The Interval V0, increment 4: the register.

`interval/register.json` is a pure function of committed snapshots and the
hand-kept, cited `interval/drivers.json`; no network, no wall clock.
`verify.py` recomputes it independently and fails on any difference.
Candidate document: docs/2026-10-04-kandidat-the-interval.md §3 step 5 and
§6 increment 4; decisions in docs/2026-10-12-the-interval-v0-inkrement-4.md.

- An **episode** is one (country, t0) that is an onset at one or more θ of
  the grid; the θ at which it is an onset are listed with it. Left-censored
  countries are listed per θ, never as episodes.
- The warning side is read from the newest committed IPC national table.
- The money side is read per episode and per flow set (`fsc`, `total`)
  from the newest snapshot day that holds a **complete** page set for the
  episode's comma-list boundary: every page HTTP 200, the last without a
  `nextLink`. Without one the set is `not_preserved`: nothing is estimated.
- `as_of` of a flow set is the month of the snapshot day it was read from,
  so an open clock never runs past what that snapshot could have seen.
- Money is rounded to cents and shares to six places, after summing in
  flow-id order, so two implementations agree byte for byte.
- A driver is `unassigned` until `interval/drivers.json` names one with a
  source. A driver without a source is refused, not shown.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from ..preserve import read_json, sha256, write_json
from . import money, warning

SCHEMA = "interval-register-v1"
REGISTER = "interval/register.json"
DRIVERS = "interval/drivers.json"
SNAPSHOTS = "interval/snapshots"
IPC_FILE = "ipc/ipc_global_national_long.csv"
SETS = {"fsc": "destinationGlobalClusterCode:FSC", "total": None}
DRIVER_VALUES = ("drought", "conflict", "economic", "mixed", "weather",
                 "unassigned")
_PAGE = re.compile(r"^(fsc|total)-([0-9_]+)-p(\d{3})\.json$")


def _days(root: Path) -> list[str]:
    base = root / SNAPSHOTS
    if not base.exists():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir())


def _manifest(root: Path, day: str) -> dict[str, dict]:
    doc = read_json(root / SNAPSHOTS / day / "manifest.json", {"entries": []})
    return {e["file"]: e for e in doc["entries"]}


def newest_ipc(root: Path) -> str | None:
    for day in reversed(_days(root)):
        rel = f"{SNAPSHOTS}/{day}/{IPC_FILE}"
        if rel in _manifest(root, day):
            return rel
    return None


def fts_pages(root: Path, day: str, iso3: str, tag: str,
              years: str) -> list[str] | None:
    """Manifested page files of one query on one day, if complete."""
    entries = _manifest(root, day)
    prefix = f"{SNAPSHOTS}/{day}/fts/{iso3}/"
    stem = years.replace(",", "_")
    pages = []
    for rel, entry in entries.items():
        if not rel.startswith(prefix):
            continue
        m = _PAGE.match(rel[len(prefix):])
        if m and m.group(1) == tag and m.group(2) == stem:
            pages.append((int(m.group(3)), rel, entry["http_status"]))
    pages.sort()
    if not pages or [p[0] for p in pages] != list(range(1, len(pages) + 1)):
        return None
    if any(status != 200 for _, _, status in pages):
        return None
    last = json.loads((root / pages[-1][1]).read_bytes())
    if (last.get("meta") or {}).get("nextLink"):
        return None
    return [rel for _, rel, _ in pages]


def newest_fts(root: Path, iso3: str, tag: str, years: str,
               before: str | None = None) -> tuple[str, list[str]] | None:
    """Newest complete page set; with `before`, among earlier days only."""
    for day in reversed(_days(root)):
        if before is not None and day >= before:
            continue
        pages = fts_pages(root, day, iso3, tag, years)
        if pages:
            return day, pages
    return None


def load_drivers(root: Path) -> dict[tuple[str, str], dict]:
    doc = read_json(root / DRIVERS, {"drivers": []})
    out = {}
    for d in doc["drivers"]:
        if d.get("driver") not in DRIVER_VALUES:
            raise ValueError(f"{DRIVERS}: unknown driver {d.get('driver')!r}")
        if d["driver"] != "unassigned" and not d.get("source"):
            raise ValueError(f"{DRIVERS}: {d['country']} {d['t0']}: "
                             "a driver needs a source")
        out[(d["country"], d["t0"])] = d
    return out


def read_onsets(ipc_text: str):
    """IPC national table -> (series per country, {(country, t0): [θ]},
    left-censored countries per θ)."""
    blocks = warning.parse_blocks(ipc_text)
    onsets: dict[tuple[str, str], list[float]] = {}
    censored: dict[str, list[str]] = {}
    series = {c: warning.warning_series(blocks, c)
              for c in warning.countries(blocks)}
    for theta in warning.THETAS:
        censored[f"{theta:.2f}"] = sorted(
            c for c, s in series.items() if warning.left_censored(s, theta))
        for c, s in series.items():
            for t0 in warning.onsets(s, theta):
                onsets.setdefault((c, t0), []).append(theta)
    return series, onsets, censored


def _round6(x: float | None) -> float | None:
    return None if x is None else round(x, 6)


def _money_side(root: Path, iso3: str, t0: str, tag: str) -> dict:
    years = money.boundary_years(t0)
    found = newest_fts(root, iso3, tag, years)
    if not found:
        return {"status": "not_preserved", "boundary_years": years}
    day, pages = found
    flows = money.parse_flows([(root / p).read_bytes() for p in pages])
    as_of = day[:7]
    cells = []
    for r in money.grid(flows, t0, as_of):
        cells.append({"k": r.k, "axis": r.axis,
                      "baseline_usd": round(r.baseline, 2), "t1": r.t1,
                      "gap_months": r.gap, "status": r.status,
                      "open_months": r.open_months,
                      "half_month": r.half_month})
    return {"status": "read", "boundary_years": years, "as_of": as_of,
            "pages": pages,
            "pages_sha256": [sha256((root / p).read_bytes()) for p in pages],
            "flows": len(flows),
            "flows_counted": sum(1 for f in flows if money.counted(f)),
            "cells": cells}


def build(root: Path) -> dict:
    ipc = newest_ipc(root)
    if ipc is None:
        raise FileNotFoundError("no committed IPC snapshot")
    drivers = load_drivers(root)
    series, onsets, censored = read_onsets(
        (root / ipc).read_text(encoding="utf-8"))
    episodes = []
    for (country, t0), thetas in sorted(onsets.items()):
        point = next(p for p in series[country] if p.month == t0)
        d = drivers.get((country, t0))
        episodes.append({
            "country": country, "t0": t0,
            "onset_at_theta": [f"{t:.2f}" for t in thetas],
            "w": _round6(point.w), "w_first": _round6(point.w_first),
            "w_second": _round6(point.w_second),
            "coverage": _round6(point.coverage), "blocks": point.blocks,
            "phase5_projected": point.phase5_projected,
            "window": list(money.window(t0)),
            "driver": {"driver": d["driver"], "source": d.get("source")}
            if d else {"driver": "unassigned", "source": None},
            "money": {tag: _money_side(root, country, t0, tag)
                      for tag in SETS},
        })
    return {
        "schema": SCHEMA,
        "ipc_snapshot": ipc,
        "ipc_sha256": sha256((root / ipc).read_bytes()),
        "grid": {"theta": [f"{t:.2f}" for t in warning.THETAS],
                 "k": list(money.KS), "axis": list(money.AXES),
                 "set": list(SETS),
                 "quiet_months": warning.QUIET_MONTHS,
                 "baseline_months": money.BASELINE_MONTHS,
                 "horizon_months": money.HORIZON_MONTHS},
        "left_censored": censored,
        "episodes": episodes,
    }


def write(root: Path) -> dict:
    register = build(root)
    write_json(root / REGISTER, register)
    return register


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Rebuild interval/register.json")
    parser.add_argument("--repo-root", default=".", type=Path)
    args = parser.parse_args(argv)
    register = write(args.repo_root.resolve())
    print(f"{REGISTER}: {len(register['episodes'])} episodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
