"""Dark Ocean V0 — the nightly Coverage-vs-Declaration reading.

Implements the GO of 2026-08-08/09 (docs/2026-08-08-dark-ocean-audit.md)
under its four conditions: fully keyless, license spine on Copernicus and
agency AIS, the DMA outage recorded per night rather than bridged, and the
practice substrate reused unchanged wherever it holds.

The machine notarizes the act of looking against the act of declaring:
which Sentinel-1 acquisitions covered which half-degree bins of the Baltic
on day D (catalog rows with the issuer's own checksums — scene bytes are
referenced, never fetched), and how the declared ocean distributed itself
over the same bins in the Digitraffic sample at reading time. Counts only —
no vessel identity ever enters a derived record; preserved source bytes
remain the issuer's documents, as everywhere in this practice.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .. import autonomy
from ..fetch import Client, SourceUnavailable
from ..preserve import Snapshot, utc_now, write_json
from . import sources
from .region import CELL, LAT0, LAT1, LON0, LON1

SNAPSHOT_BASE = "darkocean/snapshots"
MAX_CATALOG_PAGES = 5

NOTES = [
    "cells are geometric half-degree bins over the bounding box, not sea "
    "masks — a bin is a bin, not a body of water",
    "the catalog row is the record of the act of observation; scene bytes "
    "(1-2 GB, login-walled) are never fetched — the issuer's own checksums "
    "stand in for them, and EvictionDate is why the row is preserved the "
    "day it is seen",
    "the reading records the catalog as it stood at retrieval time; scenes "
    "published later belong to later catalogs and are never backfilled",
    "the declared axis is a sample at reading time from one agency's "
    "receiver range (Finnish coastal waters) — its boundary is itself a "
    "visibility regime, not a defect of the reading",
    "counts only: no vessel identity enters a derived record",
    "an 'observed silent' bin is a statement about the overlap of two "
    "committed registers, never about ships hiding",
]


def readings_dir(repo_root: Path) -> Path:
    return repo_root / "darkocean" / "readings"


def run(repo_root: Path, day: str, client: Client | None = None,
        dma_probe=sources.probe_dma) -> dict:
    client = client or Client()
    reading_path = readings_dir(repo_root) / f"{day}.json"
    if reading_path.exists():
        raise SystemExit(f"darkocean reading for {day} exists; "
                         "records are append-only (I3)")

    failures: list[dict] = []
    snap = Snapshot(repo_root, day, base=SNAPSHOT_BASE)
    refs: dict = {}

    # The observation axis: the day's catalog rows, page by page.
    pages: list[dict] = []
    url = sources.cdse_url(day)
    page_no = 1
    while url and page_no <= MAX_CATALOG_PAGES:
        try:
            data, status = client.fetch(url)
        except SourceUnavailable as err:
            failures.append({"scope": "darkocean:CDSE", "error": str(err)})
            break
        if status != 200:
            failures.append({"scope": "darkocean:CDSE",
                             "error": f"HTTP {status}"})
            break
        entry = snap.preserve(f"cdse-catalog-p{page_no}.json", data, url,
                              status)
        refs.setdefault("CDSE-catalog", []).append(entry["file"])
        try:
            page = json.loads(data)
        except json.JSONDecodeError:
            failures.append({"scope": "darkocean:CDSE",
                             "error": "JSONDecodeError"})
            break
        pages.append(page)
        url = page.get("@odata.nextLink")
        page_no += 1

    scenes = sources.cdse_scenes(pages)
    acquisitions = sources.acquisitions(scenes)

    # The declared axis: one sample of the living feed, at reading time.
    declared = None
    sample_at = None
    try:
        data, status = client.fetch(sources.DIGITRAFFIC_URL,
                                    headers={"Accept-Encoding": "gzip"})
        if status == 200:
            document = sources.gunzip_if_needed(data)
            entry = snap.preserve("digitraffic-locations.json", document,
                                  sources.DIGITRAFFIC_URL, status)
            refs["Digitraffic-AIS"] = entry["file"]
            sample_at = entry["retrieved_at"]
            try:
                declared = sources.declared_sample(json.loads(document))
            except json.JSONDecodeError:
                failures.append({"scope": "darkocean:Digitraffic",
                                 "error": "JSONDecodeError"})
        else:
            failures.append({"scope": "darkocean:Digitraffic",
                             "error": f"HTTP {status}"})
    except SourceUnavailable as err:
        failures.append({"scope": "darkocean:Digitraffic",
                         "error": str(err)})

    dma = dma_probe()

    snap.write_manifest()

    observed: dict[str, int] = {}
    for acquisition in acquisitions:
        for cell in acquisition["cells"]:
            observed[cell] = observed.get(cell, 0) + 1
    declared_cells = (declared or {}).get("cells", {})
    cells = {cid: {"observed_passes": observed.get(cid, 0),
                   "declared_sample": declared_cells.get(cid, 0)}
             for cid in sorted(set(observed) | set(declared_cells))}

    reading = {
        "date": day,
        "generated_at": utc_now(),
        "region": {"bbox": [LON0, LAT0, LON1, LAT1], "cell_deg": CELL},
        "sources": refs,
        "declared_sample_at": sample_at,
        "declared_axis": declared,
        "moment_axis": {"state": "idle — no per-moment declared source in "
                                 "the charter is reachable; nothing is "
                                 "inferred in its place",
                        "dma_probe": dma},
        "acquisitions": acquisitions,
        "cells": cells,
        "coverage": {
            "catalog_products": len(scenes),
            "acquisitions": len(acquisitions),
            "cells_observed": len(observed),
            "cells_declared_sample": len(declared_cells),
            "cells_observed_and_declared_sample":
                len(set(observed) & set(declared_cells)),
            "cells_observed_silent_in_sample":
                len(set(observed) - set(declared_cells)),
            "cells_declared_unobserved_today":
                len(set(declared_cells) - set(observed)),
        },
        "failures": failures,
        "notes": NOTES,
    }
    write_json(reading_path, reading)
    autonomy.append(repo_root, "darkocean-run", "machine", detail={
        "date": day, "requests": client.requests,
        "catalog_products": len(scenes),
        "acquisitions": len(acquisitions),
        "cells_observed": len(observed),
        "declared_vessels_in_region":
            (declared or {}).get("vessels_in_region"),
        "dma": dma["state"], "failures": len(failures)})
    return {"date": day, "catalog_products": len(scenes),
            "acquisitions": len(acquisitions),
            "cells_observed": len(observed),
            "declared_in_region": (declared or {}).get("vessels_in_region"),
            "dma": dma["state"], "failures": failures}


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Run the nightly Dark Ocean reading.")
    parser.add_argument("--repo-root", default=".", type=Path)
    yesterday = (datetime.now(timezone.utc).date()
                 - timedelta(days=1)).isoformat()
    parser.add_argument("--date", default=yesterday,
                        help="UTC day to read (default: yesterday — the "
                             "last completed day)")
    args = parser.parse_args(argv)
    summary = run(args.repo_root.resolve(), args.date)
    print(f"darkocean {summary['date']}: {summary['catalog_products']} "
          f"catalog products, {summary['acquisitions']} acquisitions, "
          f"{summary['cells_observed']} cells observed, "
          f"{summary['declared_in_region']} vessels declared in region "
          f"(sample), dma {summary['dma']}, "
          f"{len(summary['failures'])} failure(s)")
    for failure in summary["failures"]:
        print(f"  - {failure['scope']}: {failure['error']}")


if __name__ == "__main__":
    main()
