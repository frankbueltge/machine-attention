"""The nightly notary run: fetch warning feeds → preserve bytes → fold into
the registry of announced futures → measure verdicts and reaction → record
the run. Deterministic; no model.

The funding axis (OCHA FTS plans) is preserved daily so the money's movement
between warning and event accumulates as a committed time series; the
reaction axis (reaction.py) reads those preserved bytes back.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .. import autonomy
from ..fetch import Client, SourceUnavailable
from ..preserve import Snapshot, read_json, write_json
from . import reaction, sources
from .futures import (COLD_START_OVERDUE, DRIFT_OVERDUE, is_overdue,
                      overdue_kind, update_registry)
from .resolve import resolve_pending

# How many past UTC days of the attention series a nightly run completes.
# GDELT publishes a day's file the morning after, so the newest day is
# routinely still absent at 05:45 UTC — the run catches it up the next night.
REACTION_BACKFILL_DAYS = 3

FEEDS = (
    ("GDACS", sources.GDACS_URL, "gdacs.json", sources.gdacs_futures),
    ("NHC", sources.NHC_URL, "nhc-current-storms.json", sources.nhc_futures),
)


def run(repo_root: Path, day: str, client: Client | None = None) -> dict:
    client = client or Client()
    snap = Snapshot(repo_root, day)
    run_path = snap.dir / "run.json"
    if run_path.exists():
        raise SystemExit(f"run for {day} already recorded; snapshots are append-only (I3)")

    failures: list[dict] = []
    observed: list[dict] = []
    snapshot_files: dict[str, str] = {}
    parsed_feeds: dict[str, dict] = {}

    for name, url, filename, extract in FEEDS:
        try:
            data, status = client.fetch(url)
        except SourceUnavailable as err:
            failures.append({"scope": f"feed:{name}", "error": str(err)})
            continue
        if status != 200:
            failures.append({"scope": f"feed:{name}", "error": f"HTTP {status}"})
            continue
        entry = snap.preserve(filename, data, url, status)
        snapshot_files[name] = entry["file"]
        try:
            parsed = json.loads(data)
            parsed_feeds[name] = parsed
            observed.extend(extract(parsed))
        except (json.JSONDecodeError, KeyError, TypeError) as err:
            failures.append({"scope": f"extract:{name}",
                             "error": err.__class__.__name__})

    # The funding axis: preserved daily, folded in later analysis.
    try:
        data, status = client.fetch(sources.FTS_PLANS_URL)
        if status == 200:
            snap.preserve("fts-plans-2026.json", data, sources.FTS_PLANS_URL, status)
        else:
            failures.append({"scope": "feed:FTS", "error": f"HTTP {status}"})
    except SourceUnavailable as err:
        failures.append({"scope": "feed:FTS", "error": str(err)})

    registry_path = repo_root / "foreknown" / "registry.json"
    registry = read_json(registry_path, {"futures": {}})
    summary = update_registry(registry, observed, snapshot_files)
    write_json(registry_path, registry)

    # The resolver measures what the notary recorded: every closed-but-
    # unresolved future gets its verdict, derived from committed records only.
    resolutions = resolve_pending(repo_root, registry)

    open_futures = [f for f in registry["futures"].values() if f["status"] == "OPEN"]
    overdue = [f["id"] for f in open_futures if is_overdue(f)]
    # The machine's proposal sensor-cold-start-overdue-drift: an overdue flag
    # that cannot tell an artefact of when we started looking from a warning
    # that outlived its own window says nothing. Split, from tonight on.
    kinds = {f["id"]: overdue_kind(f) for f in open_futures}

    # The machine's proposal sensor-primary-iso3-gap: is the feed's own
    # primary country present in the future the registry committed? Since the
    # extraction was corrected the expected answer is an empty list every
    # night — which is the point. The guard stays so a regression, or a storm
    # whose reporting position leaves its own footprint, appears as a row
    # instead of a silence. It fires on any non-empty run, as the proposal
    # asks: a missing country needs no threshold to be missing.
    primary_iso3_dropped = []
    for feature in (parsed_feeds.get("GDACS") or {}).get("features", []):
        properties = feature.get("properties", {})
        hazard = properties.get("eventtype")
        fid = f"gdacs-{str(hazard).lower()}-{properties.get('eventid')}"
        known = registry["futures"].get(fid)
        if not known or known.get("kind") != "ALERT_EPISODE":
            continue
        dropped = sorted(sources.primary_iso3(properties)
                         - set(known.get("iso3") or []))
        if dropped:
            primary_iso3_dropped.append({"future": fid,
                                         "dropped_iso3": dropped})

    # The reaction axis: what moved while the warning was already running.
    # Its outages are recorded in its own block — a quiet GDELT day is not a
    # failure of the notary, and the two must stay legible apart.
    try:
        reaction_summary = reaction.run_reaction(
            repo_root, day, registry, client=client,
            backfill=REACTION_BACKFILL_DAYS)
    except Exception as err:  # noqa: BLE001 — never lose the notary's work
        reaction_summary = {"failures": [{"scope": "reaction",
                                          "error": err.__class__.__name__}]}

    snap.write_manifest()
    write_json(run_path, {
        "date": day,
        "requests": client.requests,
        "http_429": client.http_429,
        "observed": len(observed),
        "failures": failures,
        **{k: sorted(v) for k, v in summary.items()},
        "resolved": sorted(r["future"] for r in resolutions),
        "open_total": len(open_futures),
        "overdue": sorted(overdue),
        "primary_iso3_dropped": primary_iso3_dropped,
        "overdue_cold_start": sorted(f for f, k in kinds.items()
                                     if k == COLD_START_OVERDUE),
        "overdue_drift": sorted(f for f, k in kinds.items()
                                if k == DRIFT_OVERDUE),
        "reaction": reaction_summary,
    })
    autonomy.append(repo_root, "foreknown-notary-run", "machine", detail={
        "date": day, "requests": client.requests,
        "observed": len(observed), "notarized": len(summary["notarized"]),
        "revised": len(summary["revised"]), "closed": len(summary["closed"]),
        "resolved": len(resolutions),
        "open_total": len(open_futures), "failures": len(failures),
        "overdue_drift": sum(1 for k in kinds.values() if k == DRIFT_OVERDUE),
        "match_rate": reaction_summary.get("match_rate")})
    return {"date": day, "observed": len(observed), "failures": len(failures),
            **{k: len(v) for k, v in summary.items()},
            "resolved": len(resolutions),
            "open_total": len(open_futures),
            "reaction_failures": len(reaction_summary.get("failures", []))}


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Run the nightly notary.")
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--date",
                        default=datetime.now(timezone.utc).date().isoformat())
    args = parser.parse_args(argv)
    s = run(args.repo_root.resolve(), args.date)
    print(f"foreknown {s['date']}: {s['observed']} observed, "
          f"{s['notarized']} notarized, {s['revised']} revised, "
          f"{s['closed']} closed, {s['open_total']} open, "
          f"{s['failures']} failure(s), "
          f"{s['reaction_failures']} reaction failure(s)")


if __name__ == "__main__":
    main()
