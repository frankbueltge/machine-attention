"""The Interval V0, increment 3: the money series M and the response t1.

Pure functions over committed FTS flow pages
(interval/snapshots/<date>/fts/<ISO3>/*.json); no network, no wall clock.
Candidate document: docs/2026-10-04-kandidat-the-interval.md §3 steps 3-4;
decisions in docs/2026-10-11-the-interval-v0-inkrement-3.md.

- The episode's boundary is a **comma list of years**, never a range. FTS
  ignores a range: `year=2011-2013` returns exactly what a query without any
  year returns (probe of 2026-10-11, Somalia: 13,246 flows and the same
  totals both ways; interval/snapshots/2026-10-11/fts/SOM/probe-boundary-*).
  The comma list is a real multi-year boundary: 1,912 flows against
  805 + 622 + 584 = 2,011 for the three single years, because a flow that
  spans years is listed once.
- The window runs from BASELINE_MONTHS before t0 to HORIZON_MONTHS - 1
  after it; its years are the boundary.
- A flow counts when it crosses the boundary inward (`boundary` incoming)
  with status paid or commitment; pledges never count. Internal and
  outgoing flows are moves inside or out of the country, not new money.
  Every flow type counts, parked and pass-through included: that is what
  FTS's own incoming flowCount counts (Sudan 2024 FSC, 2026-10-09 snapshot:
  175 of 175 flows, $801.4M against FTS's $803.2M).
- A flow listed twice (the same id on two pages) is counted once, at its
  highest versionId.
- Two time axes: `date` (when the money moved) and `firstReportedDate`
  (when it was public). A month without a counted flow is zero, not missing.
- t1(k) is the first month from t0 on with M >= k x the median of the
  BASELINE_MONTHS months before t0, searched up to the horizon and never
  past `as_of` (the month of the newest snapshot). A zero baseline has no
  t1: "any money at all" is not a response. When the search ends at
  `as_of` before the horizon, the clock is open.
"""

from __future__ import annotations

import json
import statistics
from dataclasses import dataclass

from .warning import months_between

KS = (2, 3)
AXES = ("date", "firstReportedDate")
BASELINE_MONTHS = 12
HORIZON_MONTHS = 12
COUNTED_STATUS = ("paid", "commitment")


@dataclass(frozen=True)
class Flow:
    id: str
    version: int
    amount: float
    status: str
    boundary: str
    flow_type: str
    date: str               # "YYYY-MM"
    first_reported: str     # "YYYY-MM"


@dataclass(frozen=True)
class Response:
    t0: str
    k: int
    axis: str
    baseline: float             # median of the months before t0
    t1: str | None
    gap: int | None             # months t1 - t0
    status: str                 # closed | open | none_in_horizon | baseline_zero
    open_months: int | None     # months from t0 to as_of while open
    half_month: str | None      # half of the horizon's money reached


def add_months(month: str, n: int) -> str:
    y, m = map(int, month.split("-"))
    total = y * 12 + (m - 1) + n
    return f"{total // 12:04d}-{total % 12 + 1:02d}"


def window(t0: str, baseline: int = BASELINE_MONTHS,
           horizon: int = HORIZON_MONTHS) -> tuple[str, str]:
    """First and last month of the episode's money window."""
    return add_months(t0, -baseline), add_months(t0, horizon - 1)


def boundary_years(t0: str, baseline: int = BASELINE_MONTHS,
                   horizon: int = HORIZON_MONTHS) -> str:
    """The FTS `year` parameter for the episode: a comma list, never a range."""
    start, end = window(t0, baseline, horizon)
    return ",".join(str(y) for y in range(int(start[:4]), int(end[:4]) + 1))


def _month(stamp: str | None) -> str:
    if not stamp:
        raise ValueError("flow without a date")
    return stamp[:7]


def parse_flows(pages: list[bytes | str | dict]) -> list[Flow]:
    """FTS flow pages -> flows, one per id (highest versionId kept)."""
    by_id: dict[str, Flow] = {}
    for page in pages:
        payload = page if isinstance(page, dict) else json.loads(page)
        for f in (payload.get("data") or {}).get("flows") or []:
            flow = Flow(id=str(f["id"]), version=int(f.get("versionId") or 0),
                        amount=float(f.get("amountUSD") or 0),
                        status=f.get("status") or "",
                        boundary=f.get("boundary") or "",
                        flow_type=f.get("flowType") or "",
                        date=_month(f.get("date")),
                        first_reported=_month(f.get("firstReportedDate")
                                              or f.get("date")))
            if flow.id not in by_id or flow.version > by_id[flow.id].version:
                by_id[flow.id] = flow
    return sorted(by_id.values(), key=lambda fl: fl.id)


def counted(flow: Flow) -> bool:
    return flow.boundary == "incoming" and flow.status in COUNTED_STATUS


def money_series(flows: list[Flow], axis: str, start: str,
                 end: str) -> dict[str, float]:
    """M(month) for every month from start to end inclusive; zeros included."""
    if axis not in AXES:
        raise ValueError(f"unknown axis {axis}")
    series = {add_months(start, i): 0.0
              for i in range(months_between(start, end) + 1)}
    for f in flows:
        if not counted(f):
            continue
        month = f.date if axis == "date" else f.first_reported
        if month in series:
            series[month] += f.amount
    return series


def response(flows: list[Flow], t0: str, k: int, axis: str, as_of: str,
             baseline: int = BASELINE_MONTHS,
             horizon: int = HORIZON_MONTHS) -> Response:
    """t1(k) and the gap for one onset on one time axis."""
    start, end = window(t0, baseline, horizon)
    m = money_series(flows, axis, start, end)
    base = statistics.median(m[add_months(t0, -i)]
                             for i in range(1, baseline + 1))
    last = min(end, as_of)
    after = [add_months(t0, i) for i in range(months_between(t0, last) + 1)]
    half = None
    if as_of >= end:
        total = sum(m[x] for x in after)
        running = 0.0
        for x in after:
            running += m[x]
            if total > 0 and running >= total / 2:
                half = x
                break
    if base <= 0:
        return Response(t0, k, axis, base, None, None, "baseline_zero",
                        None, half)
    for x in after:
        if m[x] >= k * base:
            return Response(t0, k, axis, base, x, months_between(t0, x),
                            "closed", None, half)
    if as_of < end:
        return Response(t0, k, axis, base, None, None, "open",
                        max(months_between(t0, as_of), 0), half)
    return Response(t0, k, axis, base, None, None, "none_in_horizon", None,
                    half)


def grid(flows: list[Flow], t0: str, as_of: str) -> list[Response]:
    """Every k x axis cell for one onset and one flow set (FSC or total)."""
    return [response(flows, t0, k, axis, as_of) for axis in AXES for k in KS]
