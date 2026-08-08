"""The nightly notary run: fetch warning feeds → preserve bytes → fold into
the registry of announced futures → record the run. Deterministic; no model.
The funding axis (OCHA FTS plans) is preserved daily so the money's movement
between warning and event accumulates as a committed time series.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .. import autonomy
from ..fetch import Client, SourceUnavailable
from ..preserve import Snapshot, read_json, write_json
from . import sources
from .futures import is_overdue, update_registry

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
            observed.extend(extract(json.loads(data)))
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

    open_futures = [f for f in registry["futures"].values() if f["status"] == "OPEN"]
    overdue = [f["id"] for f in open_futures if is_overdue(f)]

    snap.write_manifest()
    write_json(run_path, {
        "date": day,
        "requests": client.requests,
        "http_429": client.http_429,
        "observed": len(observed),
        "failures": failures,
        **{k: sorted(v) for k, v in summary.items()},
        "open_total": len(open_futures),
        "overdue": sorted(overdue),
    })
    autonomy.append(repo_root, "foreknown-notary-run", "machine", detail={
        "date": day, "requests": client.requests,
        "observed": len(observed), "notarized": len(summary["notarized"]),
        "revised": len(summary["revised"]), "closed": len(summary["closed"]),
        "open_total": len(open_futures), "failures": len(failures)})
    return {"date": day, "observed": len(observed), "failures": len(failures),
            **{k: len(v) for k, v in summary.items()},
            "open_total": len(open_futures)}


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
          f"{s['failures']} failure(s)")


if __name__ == "__main__":
    main()
