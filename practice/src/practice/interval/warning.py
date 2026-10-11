"""The Interval V0, increment 2: the warning series W and its onset t0.

Pure functions over the committed IPC national long table
(interval/snapshots/<date>/ipc/ipc_global_national_long.csv); no network,
no wall clock. Candidate document: docs/2026-10-04-kandidat-the-interval.md
§3 steps 1-2; decisions in docs/2026-10-11-the-interval-v0-inkrement-2.md.

- The table comes in blocks of seven rows (all, 3+, 1, 2, 3, 4, 5), one per
  (country, analysis month, validity period). Phase 4+ is counted from the
  Number column (phase 4 plus phase 5); the rounded Percentage column is
  never read.
- The share is taken against the **total country population**, not against
  the analysed population. Analyses that cover part of a country would
  otherwise read as national alarms (Sudan, January 2026, second
  projection: 21 % of the 8.3 million analysed, 4 % of the country). The
  analysed coverage is kept beside every point.
- A few (country, month, period) keys carry more than one block (Ethiopia
  May 2021, Somalia January 2026 in the 2026-10-09 snapshot). They are not
  summed: in Ethiopia both blocks carry the same phase 5 count, in Somalia
  the second block is a near copy of the first. The block with the largest
  analysed population is taken, and the point is marked `blocks` > 1 so the
  register can show it.
- W of an analysis is the larger of the first and the second projection
  share. An analysis without any projection has no W and is skipped by the
  onset rule (neither above nor below).
- t0(θ) is an analysis with W ≥ θ that follows a run of analyses below θ
  spanning at least QUIET_MONTHS, measured from the first analysis of that
  run. A country above θ at its first analysis is left-censored, not an
  onset; a country never below θ (the chronic case) has no onset at all.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass

THETAS = (0.05, 0.10, 0.25)
QUIET_MONTHS = 6
PROJECTIONS = ("first projection", "second projection")
PERIODS = ("current",) + PROJECTIONS
_MONTHS = {m: i for i, m in enumerate(
    ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"), 1)}


@dataclass(frozen=True)
class Block:
    country: str
    month: str          # analysis month, "YYYY-MM"
    period: str         # current | first projection | second projection
    valid_from: str
    valid_to: str
    population: int     # total country population
    analysed: int       # Number in phase "all"
    phase4: int
    phase5: int


@dataclass(frozen=True)
class Point:
    country: str
    month: str
    w: float | None             # max of the projection shares, or None
    w_first: float | None
    w_second: float | None
    phase5_projected: bool
    coverage: float | None      # analysed / population of the projection used
    blocks: int                 # >1: duplicate analyses, largest kept


def analysis_month(text: str) -> str:
    """'Oct 2025' -> '2025-10'."""
    mon, year = text.split()
    return f"{int(year):04d}-{_MONTHS[mon]:02d}"


def months_between(a: str, b: str) -> int:
    """Whole months from a to b ('YYYY-MM')."""
    ya, ma = map(int, a.split("-"))
    yb, mb = map(int, b.split("-"))
    return (yb - ya) * 12 + (mb - ma)


def parse_blocks(text: str) -> list[Block]:
    """The national long CSV -> one Block per seven-row group."""
    blocks: list[Block] = []
    cur: dict | None = None

    def close():
        if cur is not None:
            blocks.append(Block(**cur))

    for row in csv.DictReader(io.StringIO(text)):
        phase = row["Phase"]
        if phase == "all":
            close()
            cur = {"country": row["Country"],
                   "month": analysis_month(row["Date of analysis"]),
                   "period": row["Validity period"],
                   "valid_from": row["From"], "valid_to": row["To"],
                   "population": int(row["Total country population"]),
                   "analysed": int(row["Number"]), "phase4": 0, "phase5": 0}
        elif cur is None:
            raise ValueError("phase row before its 'all' row")
        elif phase == "4":
            cur["phase4"] = int(row["Number"])
        elif phase == "5":
            cur["phase5"] = int(row["Number"])
    close()
    return blocks


def _share(block: Block | None) -> float | None:
    if block is None or block.population <= 0:
        return None
    return (block.phase4 + block.phase5) / block.population


def warning_series(blocks: list[Block], country: str) -> list[Point]:
    """W(country, analysis), ordered by analysis month."""
    chosen: dict[tuple[str, str], Block] = {}
    counts: dict[tuple[str, str], int] = {}
    for b in blocks:
        if b.country != country:
            continue
        key = (b.month, b.period)
        counts[key] = counts.get(key, 0) + 1
        if key not in chosen or b.analysed > chosen[key].analysed:
            chosen[key] = b
    points = []
    for month in sorted({m for m, _ in chosen}):
        first = chosen.get((month, PROJECTIONS[0]))
        second = chosen.get((month, PROJECTIONS[1]))
        w1, w2 = _share(first), _share(second)
        candidates = [(w, b) for w, b in ((w1, first), (w2, second))
                      if w is not None]
        w, used = max(candidates, key=lambda c: c[0]) if candidates else (
            None, None)
        points.append(Point(
            country=country, month=month, w=w, w_first=w1, w_second=w2,
            phase5_projected=any(b is not None and b.phase5 > 0
                                 for b in (first, second)),
            coverage=(used.analysed / used.population) if used else None,
            blocks=max(counts.get((month, p), 0) for p in PERIODS)))
    return points


def onsets(series: list[Point], theta: float,
           quiet: int = QUIET_MONTHS) -> list[str]:
    """Months of every t0(θ) in the series."""
    found = []
    run_start: str | None = None   # first analysis of the current below-run
    for p in series:
        if p.w is None:
            continue
        if p.w < theta:
            if run_start is None:
                run_start = p.month
            continue
        if run_start is not None and months_between(run_start, p.month) >= quiet:
            found.append(p.month)
        run_start = None
    return found


def left_censored(series: list[Point], theta: float) -> bool:
    """True when the first analysis with a W is already at or above θ."""
    for p in series:
        if p.w is not None:
            return p.w >= theta
    return False


def countries(blocks: list[Block]) -> list[str]:
    return sorted({b.country for b in blocks})
