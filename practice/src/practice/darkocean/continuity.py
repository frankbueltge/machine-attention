"""Dark Ocean — the continuity probe (criteria group N, the notarial act).

The Coverage-vs-Declaration reading records what the catalog said on the day
it looked. That makes the preservation claim — *this machine holds the
publisher's own checksummed claims* — a promise rather than a measurement:
`run.py` never reads an earlier reading, so no product going offline, no
appearing EvictionDate and no changed checksum could ever be caught.

This module is the look-back. Each night it re-probes every product the
register has already recorded, by catalog Id, keyless, and commits what the
catalog says *now* beside what was preserved *then*. A divergence is a
catch, not an error; an empty catch list is a result, not a failure
(criteria N2/N3, `docs/2026-08-09-dark-ocean-kriterien-nachtrag-notariat.md`).

Two disciplines are load-bearing:

- **Nothing is reconciled.** A changed checksum is committed with both
  values side by side. The preserved value is never overwritten with the
  newer one — that overwrite is exactly the forgetting the register exists
  to catch.
- **A missing baseline is not a silent pass.** Readings before 2026-08-09
  did not record ModificationDate, so it cannot be compared for the
  products they hold. The first probe establishes that baseline and says
  so; it never reports "unchanged" for a value it never had.
"""

from __future__ import annotations

import argparse
import json
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .. import autonomy
from ..fetch import Client, SourceUnavailable
from ..preserve import Snapshot, read_json, utc_now, write_json
from . import sources

SNAPSHOT_BASE = "darkocean/snapshots"
BATCH = 40
COMPARED = ("online", "eviction_date", "modification_date", "checksums")

NOTES = [
    "the look-back re-probes products the register already recorded; it "
    "never widens the catch to products it never held",
    "a divergence is committed with both values side by side and is never "
    "reconciled to the newer one — the overwrite is the forgetting this "
    "register exists to catch",
    "readings before 2026-08-09 carry no modification_date; for their "
    "products the first probe establishes the baseline and says so, rather "
    "than reporting an unchanged value it never had",
    "the eviction premise is structural, not observed: every product probed "
    "so far is online with EvictionDate 9999-12-31 (darkocean/METHOD.md). "
    "The probe measures whether that stays true",
    "a product absent from the catalog's answer is the strongest divergence "
    "the register can record, and is committed as its own kind of catch",
]


def continuity_dir(repo_root: Path) -> Path:
    return repo_root / "darkocean" / "continuity"


def lookback_url(ids: list[str]) -> str:
    """Batched catalog look-back. The OData `in` operator is refused by CDSE
    (HTTP 400, probed 2026-08-09); `Id eq X or Id eq Y` is accepted."""
    query = " or ".join(f"Id eq {pid}" for pid in ids)
    return (f"{sources.CDSE_BASE}?$top={len(ids)}&$filter="
            + urllib.parse.quote(query, safe="(),;=/:$"))


def recorded_products(repo_root: Path) -> dict[str, dict]:
    """Every product the register holds, with the values as first preserved.

    Readings are the origin of a product; earlier continuity records carry
    the baselines they established for fields the readings never had.
    """
    products: dict[str, dict] = {}
    for path in sorted((repo_root / "darkocean" / "readings").glob("*.json")):
        reading = read_json(path, {})
        for acquisition in reading.get("acquisitions", []):
            pid = acquisition.get("id")
            if not pid or pid in products:
                continue
            products[pid] = {
                "id": pid,
                "name": acquisition.get("name", ""),
                "first_seen": reading.get("date", path.stem),
                "preserved": {field: acquisition[field]
                              for field in COMPARED if field in acquisition},
            }
    for path in sorted(continuity_dir(repo_root).glob("*.json")):
        record = read_json(path, {})
        for baseline in record.get("baselines_established", []):
            entry = products.get(baseline.get("id", ""))
            if entry is not None:
                entry["preserved"].setdefault(baseline["field"],
                                              baseline["value"])
    return products


def current_values(product: dict) -> dict:
    """Catalog answer → the fields the register compares."""
    checksums = {c.get("Algorithm", "?").lower(): c.get("Value", "")
                 for c in (product.get("Checksum") or [])
                 if isinstance(c, dict) and c.get("Value")}
    return {
        "online": product.get("Online"),
        "eviction_date": product.get("EvictionDate"),
        "modification_date": product.get("ModificationDate"),
        "checksums": checksums,
    }


def compare(entry: dict, current: dict) -> tuple[list[dict], list[dict]]:
    """One product against its preserved values → (catches, baselines).

    A field the register never preserved cannot diverge; it gets a baseline
    and is named as such.
    """
    catches: list[dict] = []
    baselines: list[dict] = []
    for field in COMPARED:
        now = current.get(field)
        # A field the catalog never answered for is not a baseline either: an
        # absent value and a recorded null are the same fact — the register
        # holds nothing to compare, so it may not call anything a change.
        if entry["preserved"].get(field) in (None, {}):
            if now not in (None, {}):
                baselines.append({"id": entry["id"], "name": entry["name"],
                                  "field": field, "value": now,
                                  "reason": "not recorded when the product "
                                            "was first seen"})
            continue
        then = entry["preserved"][field]
        if then != now:
            catches.append({"kind": "changed", "id": entry["id"],
                            "name": entry["name"],
                            "first_seen": entry["first_seen"],
                            "field": field, "preserved": then,
                            "current": now})
    return catches, baselines


def run(repo_root: Path, day: str, client: Client | None = None) -> dict:
    client = client or Client()
    record_path = continuity_dir(repo_root) / f"{day}.json"
    if record_path.exists():
        raise SystemExit(f"darkocean continuity record for {day} exists; "
                         "records are append-only (I3)")

    products = recorded_products(repo_root)
    ids = sorted(products)
    failures: list[dict] = []
    snap = Snapshot(repo_root, day, base=SNAPSHOT_BASE)
    refs: list[str] = []
    answered: dict[str, dict] = {}
    batches = 0

    for start in range(0, len(ids), BATCH):
        chunk = ids[start:start + BATCH]
        url = lookback_url(chunk)
        batches += 1
        try:
            data, status = client.fetch(url)
        except SourceUnavailable as err:
            failures.append({"scope": "darkocean:CDSE-lookback",
                             "error": str(err), "batch": batches})
            continue
        if status != 200:
            failures.append({"scope": "darkocean:CDSE-lookback",
                             "error": f"HTTP {status}", "batch": batches})
            continue
        entry = snap.preserve(f"cdse-lookback-b{batches}.json", data, url,
                              status)
        refs.append(entry["file"])
        try:
            page = json.loads(data)
        except json.JSONDecodeError:
            failures.append({"scope": "darkocean:CDSE-lookback",
                             "error": "JSONDecodeError", "batch": batches})
            continue
        for product in page.get("value", []):
            pid = product.get("Id", "")
            if pid in products:
                answered[pid] = current_values(product)

    snap.write_manifest()

    catches: list[dict] = []
    baselines: list[dict] = []
    unchanged = 0
    # A product only counts as absent if its own batch was answered at all;
    # a failed batch is a failure, never evidence of a vanished product.
    failed_batches = {failure["batch"] for failure in failures}
    for index, pid in enumerate(ids):
        if (index // BATCH) + 1 in failed_batches:
            continue
        entry = products[pid]
        current = answered.get(pid)
        if current is None:
            catches.append({"kind": "gone_from_catalog", "id": pid,
                            "name": entry["name"],
                            "first_seen": entry["first_seen"],
                            "preserved": entry["preserved"],
                            "current": None})
            continue
        found, established = compare(entry, current)
        catches.extend(found)
        baselines.extend(established)
        if not found:
            unchanged += 1

    record = {
        "date": day,
        "generated_at": utc_now(),
        "sources": {"CDSE-lookback": refs},
        "probed": len(ids),
        "answered": len(answered),
        "batches": batches,
        "products_unchanged": unchanged,
        "catches": catches,
        "baselines_established": baselines,
        "failures": failures,
        "notes": NOTES,
    }
    write_json(record_path, record)
    autonomy.append(repo_root, "darkocean-continuity", "machine", detail={
        "date": day, "requests": client.requests, "probed": len(ids),
        "answered": len(answered), "catches": len(catches),
        "baselines_established": len(baselines),
        "failures": len(failures)})
    return record


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Re-probe every recorded Dark Ocean product (group N).")
    parser.add_argument("--repo-root", default=".", type=Path)
    yesterday = (datetime.now(timezone.utc).date()
                 - timedelta(days=1)).isoformat()
    parser.add_argument("--date", default=yesterday)
    args = parser.parse_args(argv)
    record = run(args.repo_root.resolve(), args.date)
    print(f"darkocean continuity {record['date']}: {record['probed']} "
          f"products probed in {record['batches']} batch(es), "
          f"{record['answered']} answered, {len(record['catches'])} catch(es), "
          f"{len(record['baselines_established'])} baseline(s) established, "
          f"{len(record['failures'])} failure(s)")
    for catch in record["catches"]:
        print(f"  ! {catch['kind']}: {catch['name']} "
              f"({catch.get('field', 'product')})")


if __name__ == "__main__":
    main()
