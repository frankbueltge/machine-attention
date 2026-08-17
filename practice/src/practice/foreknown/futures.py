"""The registry of announced futures — the notary's ledger.

Rules (docs/2026-08-08-foreknown-001-audit-und-entwurf.md):
- A future is NOTARIZED the first time it is seen; announced_at is the
  retrieval time of the preserved bytes and never changes afterwards.
- A change to window or severity is a REVISED event, appended to history —
  the original stays in the history, nothing is overwritten (I3).
- A future that leaves its feed is CLOSED_BY_SOURCE (alert episodes) or
  DISSIPATED (forecasts). V0 does not claim ARRIVED/NOT_ARRIVED — that
  verdict needs a resolver against outcome data and is honestly deferred.
- A future whose window.to lies in the past but which is still fed stays
  OPEN and is flagged overdue — a difference worth watching, not an error.
  Since 2026-08-08 that flag is split into two kinds; see overdue_kind.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from ..preserve import utc_now

OPEN = "OPEN"
CLOSED_BY_SOURCE = "CLOSED_BY_SOURCE"
DISSIPATED = "DISSIPATED"

COLD_START_OVERDUE = "cold_start_overdue"
DRIFT_OVERDUE = "drift_overdue"

DROUGHT_ROLLING = "rolling"
DROUGHT_FROZEN = "frozen"
DROUGHT_IRREGULAR = "irregular"

TRACKED_FIELDS = ("severity", "window", "what", "where")


def is_overdue(future: dict, now_iso: str | None = None) -> bool:
    to = (future.get("window") or {}).get("to")
    if not to or future["status"] != OPEN:
        return False
    now_iso = now_iso or datetime.now(timezone.utc).isoformat()
    return to[:19] < now_iso[:19]


def window_to_at_notarization(future: dict) -> str | None:
    """The window end this future carried when it was first notarized.

    Revisions are appended and never overwrite (I3), so the first recorded
    window change still holds the value the warning was announced with.
    """
    for event in future.get("history", []):
        change = (event.get("changes") or {}).get("window")
        if change:
            return (change.get("from") or {}).get("to")
    return (future.get("window") or {}).get("to")


def overdue_kind(future: dict, now_iso: str | None = None) -> str | None:
    """Which kind of overdue this is, or None if the future is not overdue.

    Implements the machine's own proposal `sensor-cold-start-overdue-drift`
    (foreknown/proposals/, discovery pass of 2026-08-08), which criticised
    this observatory's undivided overdue flag:

    - cold_start_overdue — the announced window had already passed when the
      observatory first saw the warning. An artefact of when observation
      began, not an observed fact about the warning.
    - drift_overdue — the warning was inside its window when first seen and
      outlived it under this observatory's own eyes. This is the case the
      flag was meant to catch.

    Decided from committed records alone: announced_at and the window end as
    of notarization, both immutable once written.
    """
    if not is_overdue(future, now_iso):
        return None
    first_to = window_to_at_notarization(future)
    announced_at = future.get("announced_at") or ""
    if first_to and announced_at and first_to[:19] < announced_at[:19]:
        return COLD_START_OVERDUE
    return DRIFT_OVERDUE


def _window_to_series(future: dict) -> list[tuple[str, str | None]]:
    """(observation_date, window.to) pairs this future has carried, oldest
    first — the NOTARIZED value followed by every REVISED window change.
    Read from committed history alone (window is a TRACKED_FIELD, so every
    change is already an appended event); no state beyond the registry."""
    history = future.get("history") or []
    if not history:
        return []
    series = [(history[0]["ts"][:10], window_to_at_notarization(future))]
    for event in history:
        change = (event.get("changes") or {}).get("window")
        if change:
            series.append((event["ts"][:10], (change.get("to") or {}).get("to")))
    return series


def drought_window_class(future: dict, day: str) -> dict | None:
    """Classifies an OPEN drought's window.to trajectory as rolling, frozen
    or irregular, from this future's own committed revision history — no
    extra state, since window is a TRACKED_FIELD and every change it has
    ever carried is already an appended REVISED event (I3).

    Implements the machine's own proposal
    `sensor-drought-window-class-crossing` (foreknown/proposals/, difference
    observations of 2026-08-10 and 2026-08-15; promoted 2026-08-17):

    - rolling — window.to has advanced by exactly one calendar day per
      calendar day elapsed at every recorded change (GDACS keeps extending
      the episode's stated end).
    - frozen — window.to has not changed since NOTARIZED, across at least
      two nights this future has been observed.
    - irregular — a change occurred that did not match the rolling step
      exactly. This is the crossing the sensor exists to catch (a rolling
      drought whose window.to stops advancing, or any other rate never seen
      in the two classes established so far) as well as any drought whose
      trajectory never fit the two-class split at all.

    Returns None when there is not yet enough committed history to decide
    (fewer than two nights of observation) or the future is not an OPEN
    drought.
    """
    if future.get("hazard") != "drought" or future.get("status") != OPEN:
        return None
    series = _window_to_series(future)
    if not series:
        return None
    # A night with no REVISED window event still is an observation: carry
    # the last known value forward so a rolling drought that stops advancing
    # shows up as a broken step tonight, not as a silently unchanged series.
    if series[-1][0] != day:
        series = series + [(day, series[-1][1])]
    nights_observed = (date.fromisoformat(day)
                       - date.fromisoformat(series[0][0])).days + 1
    if nights_observed < 2:
        return None
    if len({t for _, t in series}) == 1:
        return {"class": DROUGHT_FROZEN, "nights_observed": nights_observed,
                "window_to": series[-1][1]}
    for (d1, t1), (d2, t2) in zip(series, series[1:]):
        if not t1 or not t2:
            return {"class": DROUGHT_IRREGULAR, "nights_observed": nights_observed}
        day_delta = (date.fromisoformat(d2) - date.fromisoformat(d1)).days
        to_delta = (date.fromisoformat(t2[:10]) - date.fromisoformat(t1[:10])).days
        if day_delta != to_delta:
            return {"class": DROUGHT_IRREGULAR, "nights_observed": nights_observed,
                    "since": d2, "day_delta": day_delta, "todate_delta": to_delta}
    return {"class": DROUGHT_ROLLING, "nights_observed": nights_observed,
            "window_to": series[-1][1]}


def drought_window_crossings(registry: dict, day: str) -> list[dict]:
    """Every OPEN drought whose class (drought_window_class) changed between
    yesterday and tonight — computed twice, statelessly, from the same
    committed history with and without tonight's own events, rather than
    stored, so the comparison stays recomputable from committed bytes alone.
    """
    yesterday = (date.fromisoformat(day) - timedelta(days=1)).isoformat()
    crossings = []
    for fid, future in sorted(registry.get("futures", {}).items()):
        if future.get("hazard") != "drought" or future.get("status") != OPEN:
            continue
        today_state = drought_window_class(future, day)
        prior_history = [e for e in (future.get("history") or [])
                         if e["ts"][:10] != day]
        if not prior_history:
            continue
        prior_future = {**future, "history": prior_history}
        prior_state = drought_window_class(prior_future, yesterday)
        if not today_state or not prior_state:
            continue
        if today_state["class"] != prior_state["class"]:
            crossings.append({"future": fid, "from_class": prior_state["class"],
                              "to_class": today_state["class"], "run_date": day})
    return crossings


def update_registry(registry: dict, observed: list[dict],
                    snapshot_files: dict[str, str]) -> dict:
    """Fold one night's observations into the registry.

    observed: future records from the source adapters (this run).
    snapshot_files: source name -> preserved file path (provenance anchor).
    Returns a summary of what happened tonight.
    """
    futures: dict = registry.setdefault("futures", {})
    now = utc_now()
    seen_ids = set()
    summary = {"notarized": [], "revised": [], "closed": [], "reopened": []}

    for record in observed:
        fid = record["id"]
        seen_ids.add(fid)
        anchor = snapshot_files.get(record["source"], "")
        if fid not in futures:
            futures[fid] = {
                **record,
                "announced_at": now,
                "status": OPEN,
                "history": [{"ts": now, "event": "NOTARIZED", "snapshot": anchor}],
            }
            summary["notarized"].append(fid)
            continue

        known = futures[fid]
        if known["status"] != OPEN:
            # A closed future reappearing in its feed is itself a difference.
            known["status"] = OPEN
            known["history"].append({"ts": now, "event": "REAPPEARED",
                                     "snapshot": anchor})
            summary["reopened"].append(fid)

        changes = {}
        for field in TRACKED_FIELDS:
            if known.get(field) != record.get(field):
                changes[field] = {"from": known.get(field), "to": record.get(field)}
                known[field] = record[field]
        if changes:
            known["history"].append({"ts": now, "event": "REVISED",
                                     "changes": changes, "snapshot": anchor})
            summary["revised"].append(fid)

    observed_sources = {r["source"] for r in observed} | set(snapshot_files)
    for fid, known in sorted(futures.items()):
        if known["status"] != OPEN or fid in seen_ids:
            continue
        if known["source"] not in observed_sources:
            continue  # source was down tonight — absence proves nothing (I4)
        known["status"] = DISSIPATED if known["kind"] == "FORECAST" \
            else CLOSED_BY_SOURCE
        known["history"].append({"ts": now, "event": known["status"]})
        summary["closed"].append(fid)

    return summary
