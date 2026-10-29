"""What the house may draw: the rows behind the figures at frankbueltge.de/machine-attention.

export.py says what the practice is (projects, statuses, dated scalars); this
file carries the rows the site's figures are drawn from. Until 2026-10-29 the
two projects in their acceptance windows kept every figure off the site
(criterion C of both). The maintainer lifted that bar on 2026-10-29 (wording
private; docs/2026-10-29-sperre-aufgehoben.md), knowing both experiments then
miss criterion C at their review. So this file exists.

Contract `attention-views/1`. Everything is recomputed from committed records
with the projects' own code; nothing is typed, nothing is fetched:

- planetary: every reading night — the day read, outage, trigger count, the
  strong impulses (onset, peak ratio, duration), the top candidates, and for
  every preserved excerpt a min/max envelope decoded from the committed
  miniSEED bytes (practice.planetary.mseed);
- interval: every episode of interval/register.json — country, onset t0,
  warning share W, the warning series W(month) of that country around t0
  (practice.interval.warning) and the monthly money M(month) of both flow
  sets on the date axis over the episode window, from the preserved FTS
  pages (practice.interval.money), with t1 at k = 2.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from .interval import money, warning
from .planetary import mseed
from .preserve import read_json, write_json

CONTRACT = "attention-views/1"
ENVELOPE_BINS = 480  # min/max pairs per excerpt: enough for a wide figure, small on the wire
WARNING_MONTHS_BEFORE = 24


def _iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def envelope(data: bytes, bins: int = ENVELOPE_BINS) -> dict | None:
    """The excerpt as `bins` (min, max) pairs over its whole span, demeaned."""
    traces = mseed.traces(data)
    if not traces:
        return None
    tr = max(traces, key=lambda t: len(t.samples))
    s = tr.samples
    if len(s) < bins:
        return None
    mean = sum(s) / len(s)
    step = len(s) / bins
    lo, hi = [], []
    for i in range(bins):
        chunk = s[int(i * step):max(int((i + 1) * step), int(i * step) + 1)]
        lo.append(round(min(chunk) - mean))
        hi.append(round(max(chunk) - mean))
    return {"start": _iso(tr.start), "seconds": round(len(s) / tr.sample_rate, 2),
            "min": lo, "max": hi}


def planetary(root: Path) -> list[dict]:
    out = []
    for path in sorted((root / "planetary" / "readings").glob("*.json")):
        r = read_json(path, None)
        if not r:
            continue
        sd = r.get("station_day") or {}
        excerpts = []
        for ex in sd.get("excerpts") or []:
            f = root / ex["file"]
            env = envelope(f.read_bytes()) if f.exists() else None
            excerpts.append({"onset": ex["onset"], "envelope": env})
        keep = ("onset", "peak_ratio", "duration_s")
        out.append({
            "date": r["date"], "day": sd.get("day") or r.get("day"),
            "outage": bool(sd.get("outage", False)),
            "triggers": sd.get("triggers"),
            "strong": [{k: s[k] for k in keep} for s in sd.get("strong") or []],
            "top": [{k: s[k] for k in keep} for s in sd.get("top") or []],
            "excerpts": excerpts,
        })
    return out


def _series(root: Path, pages: list[str], start: str, end: str) -> dict[str, float]:
    flows = money.parse_flows([(root / p).read_bytes() for p in pages])
    return {m: round(v) for m, v in money.money_series(flows, "date", start, end).items()}


def interval(root: Path) -> list[dict]:
    reg = read_json(root / "interval" / "register.json", None)
    if not reg:
        return []
    ipc = root / reg["ipc_snapshot"]
    blocks = warning.parse_blocks(ipc.read_text(encoding="utf-8")) if ipc.exists() else []
    out = []
    for e in reg["episodes"]:
        start, end = e["window"]
        w_from = money.add_months(e["t0"], -WARNING_MONTHS_BEFORE)
        w_series = [{"month": p.month, "w": None if p.w is None else round(p.w, 6)}
                    for p in warning.warning_series(blocks, e["country"])
                    if w_from <= p.month <= end]
        sets = {}
        for name in ("fsc", "total"):
            m = e["money"].get(name) or {}
            cell = next((c for c in m.get("cells", [])
                         if c["axis"] == "date" and c["k"] == 2), None)
            sets[name] = {
                "series": _series(root, m.get("pages", []), start, end),
                "baseline_usd": cell and cell["baseline_usd"],
                "t1": cell and cell["t1"], "gap_months": cell and cell["gap_months"],
                "status": cell and cell["status"],
            }
        out.append({"country": e["country"], "t0": e["t0"], "w": e["w"],
                    "phase5_projected": e["phase5_projected"], "window": e["window"],
                    "warning": w_series, "money": sets})
    return out


def build(root: Path) -> dict:
    return {"$contract": CONTRACT, "planetary": planetary(root), "interval": interval(root)}


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    args = ap.parse_args(argv)
    payload = build(args.repo_root)
    write_json(args.repo_root / "views.json", payload)
    print(f"views: {len(payload['planetary'])} planetary nights, "
          f"{len(payload['interval'])} interval episodes")


if __name__ == "__main__":
    main()
