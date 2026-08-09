"""A one-time correction: the primary country the extraction dropped.

`gdacs_futures` built each future's `iso3` array from `affectedcountries`
alone and never read the feed's top-level singular `iso3`. Six tropical
cyclones therefore entered the registry without the country their own
`where` text names — Vietnam among them. The machine's discovery pass found
it (`foreknown/proposals/obs-2026-08-09-1.json`); the extraction is fixed as
of 2026-08-09.

The fix alone does not repair them: `iso3` is not in `TRACKED_FIELDS`, so a
future's country list is written once, at notarization, and never revisited.
This module repairs the already-committed open futures from the preserved
snapshot bytes.

Why it is not a REVISED event: nothing changed in the world or in the feed.
The register was wrong about a record it already held. That is a
**CORRECTED** event, named as ours, with the cause in the record — the
practice attributes its own errors rather than dressing them as news from
the source. Snapshots are untouched: the correction is recomputed from them,
never written into them.

Run once:

    python -m practice.foreknown.correct --repo-root .
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .. import autonomy
from ..preserve import read_json, utc_now, write_json
from . import sources

CAUSE = ("the register's own extraction read only `affectedcountries` and "
         "dropped the feed's top-level primary `iso3`; corrected 2026-08-09 "
         "from the preserved snapshot, not from a fresh fetch "
         "(foreknown/proposals/obs-2026-08-09-1.json)")


def latest_gdacs_snapshot(repo_root: Path) -> Path | None:
    paths = sorted(repo_root.glob("foreknown/snapshots/*/gdacs.json"))
    return paths[-1] if paths else None


def corrections(registry: dict, parsed: dict) -> list[dict]:
    """Open GDACS futures whose committed iso3 misses the feed's primary
    country. Only additions are proposed: the correction may extend what the
    register holds, never quietly drop from it."""
    found = []
    for feature in parsed.get("features", []):
        properties = feature.get("properties", {})
        hazard = properties.get("eventtype")
        fid = f"gdacs-{str(hazard).lower()}-{properties.get('eventid')}"
        known = registry.get("futures", {}).get(fid)
        if not known or known.get("status") != "OPEN":
            continue
        held = list(known.get("iso3") or [])
        missing = sorted(sources.primary_iso3(properties) - set(held))
        if missing:
            found.append({"future": fid, "from": held,
                          "to": sorted(set(held) | set(missing)),
                          "added": missing, "where": known.get("where", "")})
    return found


def apply(repo_root: Path) -> dict:
    registry_path = repo_root / "foreknown" / "registry.json"
    registry = read_json(registry_path, {"futures": {}})
    snapshot = latest_gdacs_snapshot(repo_root)
    if snapshot is None:
        return {"corrected": [], "note": "no preserved GDACS snapshot"}

    parsed = read_json(snapshot, {})
    found = corrections(registry, parsed)
    now = utc_now()
    anchor = str(snapshot.relative_to(repo_root))
    for correction in found:
        known = registry["futures"][correction["future"]]
        known["iso3"] = correction["to"]
        known["history"].append({
            "ts": now, "event": "CORRECTED", "snapshot": anchor,
            "corrections": {"iso3": {"from": correction["from"],
                                     "to": correction["to"]}},
            "cause": CAUSE,
        })
    if found:
        write_json(registry_path, registry)
    autonomy.append(repo_root, "foreknown-correct-primary-iso3", "human",
                    corrected_by="the machine's discovery pass "
                                 "(obs-2026-08-09-1)",
                    human_intervention="one-time repair of already-committed "
                                       "futures after the extraction fix; "
                                       "recomputed from the preserved "
                                       "snapshot, never from a fresh fetch",
                    detail={"snapshot": anchor, "corrected": len(found),
                            "futures": [c["future"] for c in found],
                            "added": {c["future"]: c["added"] for c in found}})
    return {"corrected": found, "snapshot": anchor}


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Repair futures whose primary country the extraction "
                    "dropped (one-time).")
    parser.add_argument("--repo-root", default=".", type=Path)
    args = parser.parse_args(argv)
    result = apply(args.repo_root.resolve())
    found = result["corrected"]
    print(f"{len(found)} future(s) corrected from {result.get('snapshot')}")
    for correction in found:
        print(f"  {correction['future']}: +{','.join(correction['added'])} "
              f"({correction['where']})")


if __name__ == "__main__":
    main()
