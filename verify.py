#!/usr/bin/env python3
"""Walk the provenance chain backwards and fail on any hole (invariant I1).

Checks: snapshot manifests ↔ bytes (SHA-256, both directions), registry
history anchored in manifested snapshots, announced_at immutability rules,
autonomy protocol coverage, and the stage as a byte-identical deterministic
rebuild of the committed records. Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

VALID_STATUS = {"OPEN", "CLOSED_BY_SOURCE", "DISSIPATED"}
VALID_EVENTS = {"NOTARIZED", "REVISED", "CORRECTED", "REAPPEARED",
                "CLOSED_BY_SOURCE",
                "DISSIPATED"}
VALID_VERDICTS = {"EPISODE_ENDED", "MATERIALIZED_AS_ALERT", "NO_ALERT_MATCH"}
MANIFEST_KEYS = ("file", "url", "retrieved_at", "http_status", "sha256")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_snapshots(root: Path, base: str, problems: list[str],
                    registry_files: dict[str, dict], require_run: bool) -> None:
    """Manifests ↔ bytes, both directions, for one snapshot family."""
    snap_base = root / base
    day_dirs = sorted(d for d in snap_base.iterdir() if d.is_dir()) \
        if snap_base.exists() else []
    for day_dir in day_dirs:
        manifest_path = day_dir / "manifest.json"
        if not manifest_path.exists():
            problems.append(f"{base}/{day_dir.name}: missing manifest.json")
            continue
        manifest = load(manifest_path)
        listed = set()
        for entry in manifest.get("entries", []):
            missing = [k for k in MANIFEST_KEYS if k not in entry]
            if missing:
                problems.append(f"{manifest_path}: entry missing {missing}")
                continue
            target = root / entry["file"]
            listed.add(entry["file"])
            if not target.exists():
                problems.append(f"{entry['file']}: listed but missing")
            elif sha256_file(target) != entry["sha256"]:
                problems.append(f"{entry['file']}: bytes do not match manifest sha256")
            else:
                registry_files[entry["file"]] = entry
        if require_run and not (day_dir / "run.json").exists():
            problems.append(f"{base}/{day_dir.name}: missing run.json")
        for file in day_dir.rglob("*"):
            if file.is_file() and file.name not in ("manifest.json", "run.json"):
                rel = file.relative_to(root).as_posix()
                if rel not in listed:
                    problems.append(f"{rel}: preserved but not manifested")


def _median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2


def check_reaction(root: Path, registry: dict, registry_files: dict,
                   problems: list[str]) -> None:
    """Redo the reaction axis from the committed bytes it claims to rest on.

    Deliberately a second implementation rather than a call into
    practice/: an auditor that reuses the code under audit only proves the
    code agrees with itself. The arithmetic here is small enough to restate.
    """
    base = root / "foreknown" / "reaction"
    if not base.exists():
        return

    fips_codes: set[str] = set()
    lookups = sorted(base.glob("snapshots/*/fips-country.txt"))
    if lookups:
        for line in lookups[-1].read_text(encoding="utf-8").splitlines():
            parts = line.split("\t")
            if len(parts) == 2 and parts[0]:
                fips_codes.add(parts[0])

    crosswalk_path = base / "iso3-fips.json"
    crosswalk: dict[str, str] = {}
    if crosswalk_path.exists():
        seen: dict[str, str] = {}
        for iso3, entry in sorted(load(crosswalk_path).get("entries", {}).items()):
            code = entry.get("fips")
            crosswalk[iso3] = code
            if fips_codes and code not in fips_codes:
                problems.append(f"crosswalk {iso3}: FIPS {code!r} is not in "
                                "the preserved GDELT code list")
            if code in seen:
                problems.append(f"crosswalk {iso3}: FIPS {code} is already "
                                f"mapped from {seen[code]}")
            seen[code] = iso3

    days: dict[str, dict] = {}
    for path in sorted(base.glob("attention/*.json")):
        record = load(path)
        days[path.stem] = record
        if record.get("date") != path.stem:
            problems.append(f"attention {path.stem}: date field disagrees "
                            "with the file name")
        source = record.get("source", {})
        missing = [k for k in ("url", "sha256", "bytes", "retrieved_at")
                   if not source.get(k)]
        if missing:
            problems.append(f"attention {path.stem}: source reference "
                            f"missing {missing}")
        for metric in ("events", "articles", "mentions"):
            summed = sum(c.get(metric, 0)
                         for c in record.get("countries", {}).values())
            summed += record.get("unlocated", {}).get(metric, 0)
            if record.get("world", {}).get(metric) != summed:
                problems.append(f"attention {path.stem}: world {metric} "
                                f"{record.get('world', {}).get(metric)} does "
                                f"not equal {summed} summed over countries")

    for path in sorted(base.glob("readings/*.json")):
        reading = load(path)
        name = f"reading {path.stem}"
        sources = reading.get("sources", {})
        for ref in sources.values():
            if not (root / ref).exists():
                problems.append(f"{name}: source {ref} is missing")
            elif ref not in registry_files:
                problems.append(f"{name}: source {ref} is not manifested")

        plans: dict[int, dict] = {}
        if "FTS-plans" in sources and (root / sources["FTS-plans"]).exists():
            for plan in load(root / sources["FTS-plans"]).get("data", []):
                if plan.get("id") is not None:
                    plans[plan["id"]] = {
                        "iso3": {loc.get("iso3") for loc in plan.get("locations", [])
                                 if isinstance(loc, dict) and loc.get("iso3")},
                        "requirements": plan.get("revisedRequirements")
                        or plan.get("origRequirements") or 0}
        funding: dict[int, int] = {}
        if "FTS-funding" in sources and (root / sources["FTS-funding"]).exists():
            report = (load(root / sources["FTS-funding"]).get("data")
                      or {}).get("report3") or {}
            for obj in report.get("fundingTotals", {}).get("objects", []):
                for entry in obj.get("singleFundingObjects", []):
                    if entry.get("id") is not None:
                        funding[entry["id"]] = entry.get("totalFunding") or 0

        day = reading.get("attention_day")
        window = reading.get("attention_baseline_window", [])
        if day and day not in days:
            problems.append(f"{name}: attention day {day} has no committed record")
        matched_episodes = 0
        for fid, entry in sorted(reading.get("futures", {}).items()):
            future = registry["futures"].get(fid)
            if future is None:
                problems.append(f"{name}: unknown future {fid}")
                continue
            iso3 = set(entry.get("iso3", []))
            money = entry.get("money", {})
            expected = sorted(pid for pid, plan in plans.items()
                              if plan["iso3"] & iso3)
            if plans and money.get("plans") != expected:
                problems.append(f"{name}/{fid}: plan match {money.get('plans')} "
                                f"is not {expected} in the preserved plan list")
            if plans and money.get("has_fts_plan_match") != bool(expected):
                problems.append(f"{name}/{fid}: has_fts_plan_match disagrees "
                                "with the preserved plan list")
            if plans and money.get("plan_requirements_usd") != sum(
                    plans[pid]["requirements"] for pid in expected):
                problems.append(f"{name}/{fid}: plan requirements do not add up")
            if funding and money.get("plan_funded_usd") != sum(
                    funding.get(pid, 0) for pid in expected):
                problems.append(f"{name}/{fid}: plan funding does not add up")
            if future.get("kind") == "ALERT_EPISODE" and expected:
                matched_episodes += 1

            expected_fips = sorted({crosswalk[c] for c in iso3 if c in crosswalk})
            if crosswalk and entry.get("fips") != expected_fips:
                problems.append(f"{name}/{fid}: fips {entry.get('fips')} is not "
                                f"the crosswalk's {expected_fips}")
            att = entry.get("attention")
            if not att or day not in days:
                continue
            counts = days[day].get("countries", {})
            articles = sum(counts.get(code, {}).get("articles", 0)
                           for code in entry.get("fips", []))
            world = days[day].get("world", {}).get("articles", 0)
            baseline = _median([float(sum(
                days[d].get("countries", {}).get(code, {}).get("articles", 0)
                for code in entry.get("fips", []))) for d in window if d in days])
            expected_att = {
                "articles": articles,
                "share_per_10k": round(articles / world * 10_000, 1) if world else None,
                "baseline_median_articles": baseline,
                "ratio_to_baseline": round(articles / baseline, 2) if baseline else None,
            }
            if att != expected_att:
                problems.append(f"{name}/{fid}: attention {att} is not "
                                f"{expected_att} recomputed from the "
                                "committed day records")

        coverage = reading.get("coverage", {})
        if plans and coverage.get("with_fts_plan_match") != matched_episodes:
            problems.append(f"{name}: coverage count {coverage.get('with_fts_plan_match')} "
                            f"is not the {matched_episodes} recounted")


# Dark Ocean's grid, restated on purpose: the verifier must not import the
# code under audit, so the region constants and the point test live twice.
_DO_LON0, _DO_LON1, _DO_LAT0, _DO_LAT1, _DO_CELL = 9.0, 30.0, 53.5, 66.0, 0.5


def _do_cells():
    lat = _DO_LAT0
    while lat < _DO_LAT1 - 1e-9:
        lon = _DO_LON0
        while lon < _DO_LON1 - 1e-9:
            yield f"E{lon:.1f}_N{lat:.1f}", lon + _DO_CELL / 2, lat + _DO_CELL / 2
            lon += _DO_CELL
        lat += _DO_CELL


def _do_point_in_ring(lon, lat, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > lat) != (yj > lat) and \
                lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def _do_covered_cells(geojson):
    if not geojson:
        return []
    kind, coords = geojson.get("type"), geojson.get("coordinates") or []
    rings = [coords[0]] if kind == "Polygon" and coords else \
        [poly[0] for poly in coords if poly] if kind == "MultiPolygon" else []
    covered = []
    for cid, clon, clat in _do_cells():
        for ring in rings:
            lons = [p[0] for p in ring]
            lats = [p[1] for p in ring]
            if min(lons) <= clon <= max(lons) and \
                    min(lats) <= clat <= max(lats) and \
                    _do_point_in_ring(clon, clat, ring):
                covered.append(cid)
                break
    return covered


def _do_cell_id(lon, lat):
    if not (_DO_LON0 <= lon < _DO_LON1 and _DO_LAT0 <= lat < _DO_LAT1):
        return None
    return (f"E{_DO_LON0 + int((lon - _DO_LON0) / _DO_CELL) * _DO_CELL:.1f}"
            f"_N{_DO_LAT0 + int((lat - _DO_LAT0) / _DO_CELL) * _DO_CELL:.1f}")


def check_darkocean(root: Path, registry_files: dict,
                    problems: list[str]) -> None:
    """Redo each Coverage-vs-Declaration reading from its preserved bytes."""
    base = root / "darkocean"
    if not base.exists():
        return
    for path in sorted(base.glob("readings/*.json")):
        reading = load(path)
        name = f"darkocean {path.stem}"
        if reading.get("date") != path.stem:
            problems.append(f"{name}: date field disagrees with file name")
        refs = reading.get("sources", {})
        catalog_refs = refs.get("CDSE-catalog", [])
        for ref in [*catalog_refs,
                    *([refs["Digitraffic-AIS"]]
                      if "Digitraffic-AIS" in refs else [])]:
            if not (root / ref).exists():
                problems.append(f"{name}: source {ref} is missing")
            elif ref not in registry_files:
                problems.append(f"{name}: source {ref} is not manifested")

        # Observation axis, recomputed.
        products = 0
        acquisitions: dict = {}
        for ref in catalog_refs:
            if not (root / ref).exists():
                continue
            for product in load(root / ref).get("value", []):
                if "GRD" not in product.get("Name", ""):
                    continue
                products += 1
                key = (product.get("Name", "")[:3],
                       (product.get("ContentDate") or {}).get("Start", ""),
                       (product.get("ContentDate") or {}).get("End", ""))
                acquisitions.setdefault(
                    key, _do_covered_cells(product.get("GeoFootprint")))
        observed: dict[str, int] = {}
        for cells in acquisitions.values():
            for cell in cells:
                observed[cell] = observed.get(cell, 0) + 1

        coverage = reading.get("coverage", {})
        if coverage.get("catalog_products") != products:
            problems.append(f"{name}: catalog_products "
                            f"{coverage.get('catalog_products')} is not the "
                            f"{products} recounted from preserved pages")
        if coverage.get("acquisitions") != len(acquisitions):
            problems.append(f"{name}: acquisitions "
                            f"{coverage.get('acquisitions')} is not the "
                            f"{len(acquisitions)} recounted")
        got_acq = {(a.get("platform"), a.get("start"), a.get("end")):
                   sorted(a.get("cells", []))
                   for a in reading.get("acquisitions", [])}
        want_acq = {key: sorted(cells)
                    for key, cells in acquisitions.items()}
        if got_acq != want_acq:
            problems.append(f"{name}: acquisition cells do not match the "
                            "footprints in the preserved catalog pages")

        # Declared axis, recomputed.
        declared_cells: dict[str, int] = {}
        in_region = None
        digitraffic_ref = refs.get("Digitraffic-AIS")
        if digitraffic_ref and (root / digitraffic_ref).exists():
            in_region = 0
            for feature in load(root / digitraffic_ref).get("features", []):
                coords = (feature.get("geometry") or {}).get("coordinates") or []
                if len(coords) < 2:
                    continue
                cid = _do_cell_id(coords[0], coords[1])
                if cid:
                    in_region += 1
                    declared_cells[cid] = declared_cells.get(cid, 0) + 1
            declared = reading.get("declared_axis") or {}
            if declared.get("cells") != declared_cells:
                problems.append(f"{name}: declared cells do not match the "
                                "preserved Digitraffic document")
            if declared.get("vessels_in_region") != in_region:
                problems.append(f"{name}: vessels_in_region "
                                f"{declared.get('vessels_in_region')} is not "
                                f"the {in_region} recounted")

        expected_cells = {cid: {"observed_passes": observed.get(cid, 0),
                                "declared_sample": declared_cells.get(cid, 0)}
                          for cid in sorted(set(observed) | set(declared_cells))}
        if reading.get("cells") != expected_cells:
            problems.append(f"{name}: per-cell figures do not match the "
                            "recomputation from preserved bytes")
        expected_coverage = {
            "catalog_products": products,
            "acquisitions": len(acquisitions),
            "cells_observed": len(observed),
            "cells_declared_sample": len(declared_cells),
            "cells_observed_and_declared_sample":
                len(set(observed) & set(declared_cells)),
            "cells_observed_silent_in_sample":
                len(set(observed) - set(declared_cells)),
            "cells_declared_unobserved_today":
                len(set(declared_cells) - set(observed)),
        }
        if coverage != expected_coverage:
            problems.append(f"{name}: coverage block does not match the "
                            "recomputation")
        text = json.dumps(reading, ensure_ascii=False)
        if '"mmsi"' in text.lower():
            problems.append(f"{name}: a vessel identity leaked into a "
                            "derived record")


def check_darkocean_continuity(root: Path, registry_files: dict,
                               problems: list[str]) -> None:
    """Redo each continuity record from the preserved look-back pages.

    Second implementation of criteria group N: the catches are recomputed
    against what the readings preserved, so a record cannot claim a
    divergence the bytes do not show — nor quietly drop one they do.
    """
    base = root / "darkocean" / "continuity"
    if not base.exists():
        return
    compared = ("online", "eviction_date", "modification_date", "checksums")

    # What the readings preserved, first sighting wins — the same origin the
    # probe uses, rebuilt independently here.
    preserved: dict[str, dict] = {}
    for path in sorted((root / "darkocean" / "readings").glob("*.json")):
        for acquisition in load(path).get("acquisitions", []):
            pid = acquisition.get("id")
            if pid and pid not in preserved:
                preserved[pid] = acquisition

    for path in sorted(base.glob("*.json")):
        record = load(path)
        name = f"darkocean continuity {path.stem}"
        if record.get("date") != path.stem:
            problems.append(f"{name}: date field disagrees with file name")
        for ref in record.get("sources", {}).get("CDSE-lookback", []):
            if not (root / ref).exists():
                problems.append(f"{name}: source {ref} is missing")
            elif ref not in registry_files:
                problems.append(f"{name}: source {ref} is not manifested")

        answered: dict[str, dict] = {}
        for ref in record.get("sources", {}).get("CDSE-lookback", []):
            if not (root / ref).exists():
                continue
            for product in load(root / ref).get("value", []):
                checksums = {c.get("Algorithm", "?").lower(): c.get("Value", "")
                             for c in (product.get("Checksum") or [])
                             if isinstance(c, dict) and c.get("Value")}
                answered[product.get("Id", "")] = {
                    "online": product.get("Online"),
                    "eviction_date": product.get("EvictionDate"),
                    "modification_date": product.get("ModificationDate"),
                    "checksums": checksums,
                }

        # Baselines this record established are part of the comparison basis
        # for the fields the readings never carried.
        basis = {pid: dict(entry) for pid, entry in preserved.items()}
        for baseline in record.get("baselines_established", []):
            entry = basis.get(baseline.get("id", ""))
            if entry is not None and entry.get(baseline["field"]) in (None, {}):
                entry[baseline["field"]] = baseline["value"]

        wanted: set = set()
        for pid, current in answered.items():
            entry = basis.get(pid)
            if entry is None:
                problems.append(f"{name}: the look-back answered for {pid}, "
                                "which no reading ever recorded")
                continue
            for field in compared:
                then = entry.get(field)
                if then in (None, {}):
                    continue
                if then != current.get(field):
                    wanted.add((pid, field))

        got = {(catch.get("id"), catch.get("field"))
               for catch in record.get("catches", [])
               if catch.get("kind") == "changed"}
        if got != wanted:
            problems.append(f"{name}: the recorded changes do not match the "
                            "recomputation from the preserved look-back "
                            f"({sorted(got)} vs {sorted(wanted)})")

        for catch in record.get("catches", []):
            if catch.get("kind") != "changed":
                continue
            entry = preserved.get(catch.get("id"), {})
            baselines = {b["field"]: b["value"]
                         for b in record.get("baselines_established", [])
                         if b.get("id") == catch.get("id")}
            was = entry.get(catch.get("field"), baselines.get(catch.get("field")))
            if catch.get("preserved") != was:
                problems.append(f"{name}: catch on {catch.get('id')} reports a "
                                "preserved value the register does not hold — "
                                "a reconciliation, which group N forbids")

        text = json.dumps(record, ensure_ascii=False)
        if '"mmsi"' in text.lower():
            problems.append(f"{name}: a vessel identity leaked into a "
                            "derived record")


def check(root: Path) -> list[str]:
    problems: list[str] = []
    registry_files: dict[str, dict] = {}

    check_snapshots(root, "foreknown/snapshots", problems, registry_files, True)
    check_snapshots(root, "foreknown/reaction/snapshots", problems,
                    registry_files, False)
    check_snapshots(root, "darkocean/snapshots", problems, registry_files,
                    False)

    registry = load(root / "foreknown" / "registry.json") \
        if (root / "foreknown" / "registry.json").exists() else {"futures": {}}
    for fid, future in sorted(registry["futures"].items()):
        if future.get("status") not in VALID_STATUS:
            problems.append(f"{fid}: illegal status {future.get('status')!r}")
        history = future.get("history", [])
        if not history:
            problems.append(f"{fid}: empty history")
            continue
        if history[0].get("event") != "NOTARIZED":
            problems.append(f"{fid}: history does not begin with NOTARIZED")
        if not future.get("announced_at"):
            problems.append(f"{fid}: missing announced_at")
        elif history[0].get("ts") != future["announced_at"]:
            problems.append(f"{fid}: announced_at diverges from notarization event")
        for event in history:
            if event.get("event") not in VALID_EVENTS:
                problems.append(f"{fid}: unknown history event {event.get('event')!r}")
            anchor = event.get("snapshot")
            if anchor and anchor not in registry_files:
                problems.append(f"{fid}: history anchor {anchor} not manifested")

    for res_file in sorted(root.glob("foreknown/resolutions/*.json")):
        resolution = load(res_file)
        fid = resolution.get("future", res_file.stem)
        future = registry["futures"].get(fid)
        if future is None:
            problems.append(f"resolution {fid}: unknown future")
            continue
        if future.get("status") == "OPEN":
            problems.append(f"resolution {fid}: future is still OPEN")
        if resolution.get("verdict") not in VALID_VERDICTS:
            problems.append(f"resolution {fid}: illegal verdict "
                            f"{resolution.get('verdict')!r}")
        if not resolution.get("resolved_at"):
            problems.append(f"resolution {fid}: missing resolved_at")
        if not isinstance(resolution.get("measured"), dict):
            problems.append(f"resolution {fid}: measured is not a record")
        for anchor in resolution.get("evidence", []):
            if anchor not in registry_files:
                problems.append(f"resolution {fid}: evidence {anchor} "
                                "not manifested")

    check_reaction(root, registry, registry_files, problems)
    check_darkocean(root, registry_files, problems)
    check_darkocean_continuity(root, registry_files, problems)

    log_path = root / "autonomy" / "log.jsonl"
    run_dates = {load(p)["date"] for p in root.glob("foreknown/snapshots/*/run.json")}
    logged = set()
    if log_path.exists():
        for i, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), 1):
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f"autonomy log line {i}: unparseable")
                continue
            if entry.get("step") == "foreknown-notary-run":
                logged.add(entry.get("detail", {}).get("date"))
    for missing_date in sorted(run_dates - logged):
        problems.append(f"run {missing_date} has no autonomy protocol entry")

    generator = root / "stage" / "generate.py"
    public = root / "public"
    if generator.exists():
        spec = importlib.util.spec_from_file_location("stagegen", generator)
        stagegen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(stagegen)
        with tempfile.TemporaryDirectory() as tmp:
            fresh = stagegen.build(root, Path(tmp) / "public")
            fresh_files = {p.relative_to(fresh).as_posix(): p.read_bytes()
                           for p in fresh.rglob("*") if p.is_file()}
            public_files = {p.relative_to(public).as_posix(): p.read_bytes()
                            for p in public.rglob("*") if p.is_file()} \
                if public.exists() else {}
            if not public_files:
                problems.append("public/ missing — stage not generated")
            elif fresh_files != public_files:
                diff = sorted(set(fresh_files) ^ set(public_files)) or sorted(
                    k for k in fresh_files if fresh_files[k] != public_files.get(k))
                problems.append("public/ is not a deterministic rebuild "
                                f"(differs: {diff[:5]})")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", type=Path)
    args = parser.parse_args(argv)
    problems = check(args.repo_root.resolve())
    if problems:
        print(f"provenance chain has {len(problems)} hole(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("provenance chain intact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
