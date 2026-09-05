"""What this practice tells the house about itself.

frankbueltge.de mirrors this practice as rendered HTML. Parsing those pages
back into facts would be brittle re-derivation — a layout change would break
the figure, and it would claim a precision the source never gave. So the
practice exports what it wants known, in one small file, the same way the
ecology's practices publish a work meta beside a work.

Contract: `docs/design/2026-08-09-attention-export-contract.md` in the site
repository (`attention-export/1`). Deliberately narrow: projects, statuses
and dated scalars — never individual futures, readings or snapshots, never
prose written for a page, never an address. The house records that the
instrument exists and what it reports, never its rows.

Every figure is recomputed here from committed records; nothing is typed.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .foreknown.futures import (COLD_START_OVERDUE, DRIFT_OVERDUE,
                                overdue_kind)
from .preserve import read_json, write_json

CONTRACT = "attention-export/1"

# One line per admitted project. `status` is this practice's own word, not a
# term the consumer interprets; `site_route` is null while a project lives
# only in this repository — which is the admission path's rule, not an
# oversight (no stage presence before the E-experiment is passed).
PROJECTS = (
    {"id": "foreknown", "title": "The Foreknown", "since": "2026-08-08",
     "site_route": "/attention", "status": "running"},
    # Reviewed 2026-08-22: the E-experiment did not pass, and the stage
    # ambition ended with it (docs/2026-08-22-dark-ocean-e-review.md). What
    # runs on is narrower than the project was — the nightly continuity
    # notary — so the status word is `instrument`, and the two figures below
    # carry its null result rather than leaving a green run to imply a find.
    {"id": "darkocean", "title": "Dark Ocean", "since": "2026-08-07",
     "site_route": None, "status": "instrument"},
    # Nightly since 2026-08-13, admitted 2026-08-15, absent from this list
    # until 2026-08-22 — which is why the house could not see it. Its
    # acceptance criteria are committed; the window has not opened.
    {"id": "memoryhole", "title": "Memory Hole", "since": "2026-08-15",
     "site_route": None, "status": "v0"},
    {"id": "state-before-interface", "title": "The State Before the Interface",
     "since": "2026-08-08", "site_route": "/observatory",
     "status": "running"},
)


def head_commit(repo_root: Path) -> str:
    """The commit this export was made from, read from the checkout itself —
    no subprocess, so the deterministic rebuild stays deterministic."""
    head = repo_root / ".git" / "HEAD"
    if not head.exists():
        return "unknown"
    ref = head.read_text(encoding="utf-8").strip()
    if ref.startswith("ref: "):
        target = repo_root / ".git" / ref[5:]
        if target.exists():
            return target.read_text(encoding="utf-8").strip()[:7]
        packed = repo_root / ".git" / "packed-refs"
        if packed.exists():
            for line in packed.read_text(encoding="utf-8").splitlines():
                parts = line.split()
                if len(parts) == 2 and parts[1] == ref[5:]:
                    return parts[0][:7]
        return "unknown"
    return ref[:7]


def figures(repo_root: Path) -> list[dict]:
    """Dated scalars, each recounted from the records that carry them."""
    registry = read_json(repo_root / "foreknown" / "registry.json",
                         {"futures": {}})
    futures = registry.get("futures", {})
    resolutions = [read_json(p) for p in
                   sorted((repo_root / "foreknown" / "resolutions").glob("*.json"))]
    nights = sorted(p.name for p in
                    (repo_root / "foreknown" / "snapshots").glob("*")
                    if p.is_dir())
    readings = sorted((repo_root / "darkocean" / "readings").glob("*.json"))
    continuity = sorted((repo_root / "darkocean" / "continuity").glob("*.json"))
    memoryhole = sorted((repo_root / "memoryhole" / "readings").glob("*.json"))
    # The continuity notary answers with a count and a list of catches. Both
    # are read over every committed night, so the figure cannot quietly become
    # "last night was fine" — a divergence, once found, stays on the record.
    #
    # Rechecks are events and are summed. Divergences are PRODUCTS and are
    # counted once each: a product gone from the catalog is re-caught every
    # night it stays gone, so summing per-night lengths would report the same
    # finding again each morning and climb while nothing new had happened.
    # Read as a list, not as a count — `catches` has been a list in every
    # night ever committed; `int(...)` on it read 0 for as long as the list
    # was empty and raised the night it was not (2026-09-03, four products).
    probes = [read_json(path, {}) for path in continuity]
    rechecks = sum(int(probe.get("answered") or 0) for probe in probes)
    caught: set[str] = set()
    for probe in probes:
        for entry in probe.get("catches") or []:
            caught.add(str(entry.get("id")))
    divergences = len(caught)
    # A resolution whose future was already historical at first sight closes
    # a record, not a cycle. The practice reports both numbers or neither.
    watched = sum(1 for r in resolutions if r.get("cold_start") is False)
    # Composition, because the third source arrived on 2026-08-22 and a
    # register that grows without saying where the growth came from is a
    # figure that misleads while every number in it is true.
    by_source: dict[str, int] = {}
    for future in futures.values():
        name = str(future.get("source") or "unknown").lower()
        by_source[name] = by_source.get(name, 0) + 1
    as_of = nights[-1] if nights else ""
    # The epistemic split of the source-open register, by the same rule the
    # stage uses (deterministic against the last run date, never the wall
    # clock): window_open — the announced future has not yet elapsed;
    # cold_start — already historical at first sight; drift — outlived its
    # window under this machine's watch.
    open_futures = [f for f in futures.values() if f.get("status") == "OPEN"]
    kinds = {f["id"]: overdue_kind(f, f"{as_of}T00:00:00")
             for f in open_futures} if as_of else {}
    return [
        {"key": "futures_under_watch",
         "value": len(open_futures),
         "as_of": as_of},
        {"key": "futures_window_open",
         "value": sum(1 for k in kinds.values() if k is None),
         "as_of": as_of},
        {"key": "futures_cold_start",
         "value": sum(1 for k in kinds.values() if k == COLD_START_OVERDUE),
         "as_of": as_of},
        {"key": "futures_drift",
         "value": sum(1 for k in kinds.values() if k == DRIFT_OVERDUE),
         "as_of": as_of},
        {"key": "futures_notarized_total", "value": len(futures),
         "as_of": as_of},
        {"key": "futures_resolved", "value": len(resolutions), "as_of": as_of},
        {"key": "futures_resolved_under_watch", "value": watched,
         "as_of": as_of},
        {"key": "materialized",
         "value": sum(1 for r in resolutions
                      if r.get("verdict") == "MATERIALIZED_AS_ALERT"),
         "as_of": as_of},
        {"key": "nights_on_record", "value": len(nights), "as_of": as_of},
        {"key": "darkocean_nights_on_record", "value": len(readings),
         "as_of": readings[-1].stem if readings else as_of},
        {"key": "darkocean_continuity_rechecks", "value": rechecks,
         "as_of": continuity[-1].stem if continuity else as_of},
        {"key": "darkocean_continuity_divergences", "value": divergences,
         "as_of": continuity[-1].stem if continuity else as_of},
        {"key": "memoryhole_nights_on_record", "value": len(memoryhole),
         "as_of": memoryhole[-1].stem if memoryhole else as_of},
        {"key": "sources_in_register", "value": len(by_source),
         "as_of": as_of},
    ] + [
        {"key": f"futures_notarized_{name}", "value": count, "as_of": as_of}
        for name, count in sorted(by_source.items())
    ]


def build(repo_root: Path) -> dict:
    return {
        "$contract": CONTRACT,
        "generated_from": {"repo": "machine-attention",
                           "commit": head_commit(repo_root)},
        "practice": {"id": "machine-attention", "label": "Machine Attention"},
        "projects": [dict(project) for project in PROJECTS],
        "figures": figures(repo_root),
    }


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Write the practice's export for frankbueltge.de.")
    parser.add_argument("--repo-root", default=".", type=Path)
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    payload = build(root)
    write_json(root / "export.json", payload)
    print(f"export.json: {len(payload['projects'])} projects, "
          f"{len(payload['figures'])} figures, from "
          f"{payload['generated_from']['commit']}")


if __name__ == "__main__":
    main()
