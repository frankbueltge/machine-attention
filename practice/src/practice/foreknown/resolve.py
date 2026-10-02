"""Outcome resolvers: measured verdicts for closed futures.

The notary records; the resolver measures. Verdicts derive exclusively from
committed records — the registry's histories, anchored in manifested
snapshots. No model, no fresh fetches, no risk estimates of our own.

Honest limits, kept in the record:
- cold_start: for episodes already running when observation began,
  announced_at is OUR first sight, not the issuer's issue time.
- NO_ALERT_MATCH means "no alert-grade episode in this observatory's own
  registry" — a statement about the record, not about the world.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from ..preserve import read_json, utc_now, write_json
from .series import reaction_series  # noqa: F401  (re-exported: the join is read through the resolver)

EPISODE_ENDED = "EPISODE_ENDED"
MATERIALIZED_AS_ALERT = "MATERIALIZED_AS_ALERT"
NO_ALERT_MATCH = "NO_ALERT_MATCH"
VERDICTS = (EPISODE_ENDED, MATERIALIZED_AS_ALERT, NO_ALERT_MATCH)
# The two verdicts resolve_future ever writes for a FORECAST-kind future
# (EPISODE_ENDED is ALERT_EPISODE-only, see resolve_future below) — a
# resolution file's own verdict is enough to tell the two kinds apart
# without re-reading the registry.
FORECAST_VERDICTS = (MATERIALIZED_AS_ALERT, NO_ALERT_MATCH)
TOP_OF_LADDER = frozenset({"Red", "Extreme"})

# foreknown/proposals/sensor-lead-time-pathway-idle.json, promoted
# 2026-09-11: N=10 total FORECAST-kind resolutions accumulated (NO_ALERT_MATCH
# or MATERIALIZED_AS_ALERT combined) with the materialized count still zero.
LEAD_TIME_PATHWAY_IDLE_N = 10

_STORM_STOPWORDS = {"TROPICAL", "CYCLONE", "HURRICANE", "STORM", "TYPHOON",
                    "DEPRESSION", "POTENTIAL", "SUBTROPICAL", "SUPER"}


def storm_token(text: str) -> str | None:
    """The storm's proper name, e.g. 'Tropical Cyclone DOLPHIN-26' -> 'DOLPHIN'."""
    for token in re.findall(r"[A-Za-z]{3,}", text or ""):
        if token.upper() not in _STORM_STOPWORDS:
            return token.upper()
    return None


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        ts = datetime.fromisoformat(value)
    except ValueError:
        return None
    return ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc)


def _severity_path(future: dict) -> list[str]:
    """The alert level's trajectory, reconstructed from the revision history."""
    path: list[str] = []
    for event in future.get("history", []):
        changes = event.get("changes", {})
        if "severity" in changes:
            if not path:
                path.append(changes["severity"]["from"])
            path.append(changes["severity"]["to"])
    if not path:
        path = [future.get("severity", "")]
    return [p for p in path if p]


def _evidence(future: dict) -> list[str]:
    return sorted({e["snapshot"] for e in future.get("history", [])
                   if e.get("snapshot")})


def resolve_future(future: dict, registry_futures: dict,
                   first_run_date: str) -> dict:
    severity_path = _severity_path(future)
    revisions = sum(1 for e in future.get("history", [])
                    if e.get("event") == "REVISED")
    cold_start = (future.get("announced_at", "")[:10] == first_run_date)
    base = {
        "future": future["id"],
        "resolved_at": utc_now(),
        "cold_start": cold_start,
        "measured": {
            "revisions": revisions,
            "severity_path": severity_path,
            # The top of whichever ladder the source uses. GDACS climbs to
            # Red, CAP to Extreme; the ladders are never mixed, and the
            # existing reading is unchanged — a level reached after the first
            # sighting counts even if the alert later stepped back down.
            "escalated": (any(s in TOP_OF_LADDER for s in severity_path[1:])
                          and severity_path[0] not in TOP_OF_LADDER),
        },
        "evidence": _evidence(future),
    }

    if future.get("kind") == "ALERT_EPISODE":
        window = future.get("window") or {}
        start, end = _parse_ts(window.get("from")), _parse_ts(window.get("to"))
        base["verdict"] = EPISODE_ENDED
        base["measured"]["episode_window"] = window
        if start and end:
            base["measured"]["episode_days"] = round(
                (end - start).total_seconds() / 86400, 1)
        return base

    # FORECAST: does the observatory's own registry hold an alert-grade
    # episode for the same storm?
    token = storm_token(future.get("what", ""))
    match = None
    if token:
        for fid, other in sorted(registry_futures.items()):
            if other.get("kind") == "ALERT_EPISODE" \
                    and other.get("hazard") == "tropical cyclone" \
                    and storm_token(other.get("what", "")) == token:
                match = (fid, other)
                break
    if match:
        fid, other = match
        base["verdict"] = MATERIALIZED_AS_ALERT
        base["measured"]["matched"] = fid
        base["evidence"] = sorted(set(base["evidence"]) | set(_evidence(other)))
        announced = _parse_ts(future.get("announced_at"))
        episode_start = _parse_ts((other.get("window") or {}).get("from"))
        if announced and episode_start:
            base["measured"]["lead_time_hours"] = round(
                (episode_start - announced).total_seconds() / 3600, 1)
    else:
        base["verdict"] = NO_ALERT_MATCH
        base["note"] = ("no alert-grade episode for this storm in the "
                        "observatory's registry — a statement about the "
                        "record, not about the world")
    return base


def lead_time_pathway_idle(repo_root: Path) -> dict:
    """Whether the MATERIALIZED_AS_ALERT / lead_time_hours pathway
    (resolve_future above) has ever actually fired, across every resolution
    this observatory has ever written. Reads foreknown/resolutions/ directly
    — append-only, so the count only grows — rather than the registry, since
    a resolution's own verdict already says which kind of future it came
    from (FORECAST_VERDICTS above)."""
    res_dir = repo_root / "foreknown" / "resolutions"
    total = materialized = 0
    if res_dir.is_dir():
        for path in sorted(res_dir.glob("*.json")):
            verdict = (read_json(path) or {}).get("verdict")
            if verdict not in FORECAST_VERDICTS:
                continue
            total += 1
            if verdict == MATERIALIZED_AS_ALERT:
                materialized += 1
    return {
        "forecast_resolutions_total": total,
        "materialized_as_alert_total": materialized,
        "idle": total >= LEAD_TIME_PATHWAY_IDLE_N and materialized == 0,
    }


_CLOSURE_EVENTS = ("CLOSED_BY_SOURCE", "DISSIPATED")


def resolution_reappearance_uncovered(repo_root: Path,
                                      registry: dict) -> list[dict]:
    """Every future that closed again after a REAPPEARED event while its one
    resolution file still bears an earlier closure's resolved_at.

    Implements the machine's own proposal
    `sensor-resolution-reappearance-coverage` (foreknown/proposals/,
    proposed 2026-08-30, promoted 2026-10-02): resolve_pending below is keyed
    per future id — `if path.exists(): continue` — so a future that closes,
    reappears and closes again keeps only its first life's resolution. A
    mechanical membership check against committed registry histories and
    resolution files; no threshold, and a single instance is the finding.
    Silent once resolutions are keyed per episode (the proposal's own
    falsification (a)), since then a later closure's resolved_at matches.
    """
    res_dir = repo_root / "foreknown" / "resolutions"
    uncovered = []
    for fid, future in sorted(registry.get("futures", {}).items()):
        history = future.get("history") or []
        reappeared = [_parse_ts(e.get("ts")) for e in history
                      if e.get("event") == "REAPPEARED"]
        reappeared = [ts for ts in reappeared if ts]
        if not reappeared:
            continue
        first_reappeared = min(reappeared)
        later_closures = [e["ts"] for e in history
                          if e.get("event") in _CLOSURE_EVENTS
                          and _parse_ts(e.get("ts"))
                          and _parse_ts(e["ts"]) > first_reappeared]
        if not later_closures:
            continue
        path = res_dir / f"{fid}.json"
        resolved_at = (read_json(path) or {}).get("resolved_at") \
            if path.exists() else None
        resolved = _parse_ts(resolved_at)
        # resolve.py and futures.py stamp with separate clocks; a closure
        # counts as covered when resolved_at lies within a few seconds after
        # it (obs-2026-09-25-1.json: 50 of 352 differ by one second).
        if resolved and any(
                0 <= (resolved - _parse_ts(ts)).total_seconds() <= 5
                for ts in later_closures):
            continue
        uncovered.append({"future": fid, "resolved_at": resolved_at,
                          "later_closures": later_closures})
    return uncovered


def resolve_pending(repo_root: Path, registry: dict) -> list[dict]:
    """Resolve every closed-but-unresolved future. Idempotent and append-only:
    an existing resolution is never rewritten."""
    futures = registry.get("futures", {})
    if not futures:
        return []
    first_run_date = min(f.get("announced_at", "9999")[:10]
                         for f in futures.values())
    out_dir = repo_root / "foreknown" / "resolutions"
    resolutions = []
    for fid, future in sorted(futures.items()):
        if future.get("status") == "OPEN":
            continue
        path = out_dir / f"{fid}.json"
        if path.exists():
            continue
        resolution = resolve_future(future, futures, first_run_date)
        # What moved while the clock was running (E1 review, 2026-08-22). The
        # resolver stays pure; the join happens here, where the records are.
        series = reaction_series(repo_root, fid)
        if series:
            resolution["reaction"] = series
        write_json(path, resolution)
        resolutions.append(resolution)
    return resolutions
