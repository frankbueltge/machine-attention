"""Stage moments of The Foreknown — real events offered to the shared stage.

The substrate contract `stage_moment` (docs/2026-08-08-projekt-aufnahme.md §5,
"Momente statt Cards") made code: the project derives, from its committed
records alone, the small set of perceivable events the practice's shared
stage may show. Deterministic — same registry, same moments.

What is a moment here and what is not:
- The first night's mass notarization is baseline, never a moment: a warning
  the machine imported on day one proves nothing about this apparatus.
- A notarization whose announced window already lay in the past at first
  sight is baseline too (a later cold start), and stays off the stage.
- Everything else the record shows happening under watch — a revision, a
  correction of the machine's own record, a source letting go, a forecast
  dissipating, a warning returning, a measured verdict — is a moment.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from ..preserve import read_json
from .futures import overdue_kind

MODES = {
    "REVISED": "revision",
    "CORRECTED": "correction",
    "CLOSED_BY_SOURCE": "closure",
    "DISSIPATED": "dissipation",
    "REAPPEARED": "reappearance",
    "NOTARIZED": "notarization",
}

STATEMENTS = {
    "CORRECTED": "The machine corrected its own record — the feed had said "
                 "it all along.",
    "CLOSED_BY_SOURCE": "A source let go of one of its warnings.",
    "DISSIPATED": "A forecast dissipated from its source's feed.",
    "REAPPEARED": "A warning came back after its source had let it go.",
    "NOTARIZED": "A new announced future entered the record.",
}

VERDICT_STATEMENTS = {
    "EPISODE_ENDED": "An announced future ran its course under watch.",
    "MATERIALIZED_AS_ALERT": "A forecast became an alert while the machine "
                             "watched.",
    "NO_ALERT_MATCH": "A forecast passed without an alert in this register.",
}


def _span_words(start: str, end: str) -> str:
    """The distance between two committed timestamps, in plain words."""
    delta = datetime.fromisoformat(end) - datetime.fromisoformat(start)
    hours = max(1, round(delta.total_seconds() / 3600))
    if hours >= 48:
        days = round(hours / 24)
        return f"{days} days"
    return f"{hours} hour{'s' if hours != 1 else ''}"


def _moment(future: dict, ts: str, mode: str, statement: str,
            evidence: str) -> dict:
    fid = future["id"]
    return {
        "project": "foreknown",
        "occurred_at": ts,
        "mode": mode,
        "statement": statement,
        "subject": future.get("what") or fid,
        "enter": f"/attention/future/{fid}.html",
        "evidence": evidence or "foreknown/registry.json",
    }


def moments(repo_root: Path) -> list[dict]:
    registry = read_json(repo_root / "foreknown" / "registry.json",
                         {"futures": {}})
    futures = registry.get("futures", {})
    run_dates = sorted(p.parent.name for p in
                       repo_root.glob("foreknown/snapshots/*/run.json"))
    first_night = run_dates[0] if run_dates else ""

    out: list[dict] = []
    for fid, future in sorted(futures.items()):
        announced_at = future.get("announced_at") or ""
        for event in future.get("history", []):
            ts = event.get("ts") or ""
            kind = event.get("event") or ""
            if not ts or kind not in MODES:
                continue
            if kind == "NOTARIZED":
                if ts[:10] <= first_night:
                    continue  # the founding import is baseline, not an event
                if overdue_kind(future, ts) is not None:
                    continue  # already historical at first sight — baseline
            if kind == "REVISED":
                statement = (f"A warning changed "
                             f"{_span_words(announced_at, ts)} after it was "
                             f"first preserved.")
            else:
                statement = STATEMENTS[kind]
            out.append(_moment(future, ts, MODES[kind], statement,
                               event.get("snapshot") or ""))

    for path in sorted(repo_root.glob("foreknown/resolutions/*.json")):
        resolution = read_json(path) or {}
        fid = resolution.get("future")
        future = futures.get(fid)
        verdict = resolution.get("verdict") or ""
        ts = resolution.get("resolved_at") or ""
        if not future or not ts or verdict not in VERDICT_STATEMENTS:
            continue
        out.append(_moment(future, ts, "resolution",
                           VERDICT_STATEMENTS[verdict],
                           f"foreknown/resolutions/{path.name}"))

    out.sort(key=lambda m: (m["occurred_at"], m["enter"], m["mode"]),
             reverse=True)
    return out
