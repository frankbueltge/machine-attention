#!/usr/bin/env python3
"""Walk the provenance chain backwards and fail on any hole (invariant I1).

Checks: snapshot manifests ↔ bytes (SHA-256, both directions), registry
history anchored in manifested snapshots, announced_at immutability rules,
autonomy protocol coverage, the OpenTimestamps anchors against the manifests
they commit to, and the stage as a byte-identical deterministic rebuild of the
committed records. Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from datetime import date, datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

VALID_STATUS = {"OPEN", "CLOSED_BY_SOURCE", "DISSIPATED"}
VALID_EVENTS = {"NOTARIZED", "REVISED", "CORRECTED", "REAPPEARED",
                "CLOSED_BY_SOURCE",
                "DISSIPATED"}
VALID_VERDICTS = {"EPISODE_ENDED", "MATERIALIZED_AS_ALERT", "NO_ALERT_MATCH"}
MANIFEST_KEYS = ("file", "url", "retrieved_at", "http_status", "sha256")
# An OpenTimestamps proof begins with this magic, then one version byte, then the hash op
# and the digest of the file it commits to. Read from the format, not from the client, so
# the pairing proof <-> manifest can be checked with the standard library alone.
OTS_MAGIC = bytes.fromhex("004f70656e54696d657374616d7073000050726f6f6600bf89e2e884e89294")
OTS_SHA256_OP = 0x08


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


def _crosswalk_as_of(doc: dict, day: str) -> dict[str, str]:
    """The iso3->FIPS crosswalk as it stood on `day`.

    iso3-fips.json's own scope note says the table "grows when the record
    shows it must" (foreknown/reaction/iso3-fips.json), so a reading from
    before a later growth was computed against a smaller table than the
    file holds today. Checking every historical reading against today's
    full table would flag every such reading as wrong forever, the day
    after the table did exactly what it says it does. `revisions` (each
    `{"date", "added": {iso3: fips}}`) names when each later entry joined,
    so a reading is checked against what existed on its own day."""
    revised_iso3 = {iso3 for rev in doc.get("revisions", [])
                    for iso3 in rev.get("added", {})}
    authored = doc.get("authored")
    result: dict[str, str] = {}
    if not authored or authored <= day:
        result = {iso3: entry.get("fips")
                   for iso3, entry in doc.get("entries", {}).items()
                   if iso3 not in revised_iso3}
    for rev in sorted(doc.get("revisions", []), key=lambda r: r.get("date", "")):
        if rev.get("date", "") <= day:
            result.update(rev.get("added", {}))
    return result


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
    crosswalk_doc: dict = {}
    crosswalk: dict[str, str] = {}
    if crosswalk_path.exists():
        crosswalk_doc = load(crosswalk_path)
        seen: dict[str, str] = {}
        for iso3, entry in sorted(crosswalk_doc.get("entries", {}).items()):
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
        reading_day = reading.get("date", path.stem)
        crosswalk_then = (_crosswalk_as_of(crosswalk_doc, reading_day)
                          if crosswalk_doc else crosswalk)
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

            expected_fips = sorted({crosswalk_then[c] for c in iso3 if c in crosswalk_then})
            if crosswalk_then and entry.get("fips") != expected_fips:
                problems.append(f"{name}/{fid}: fips {entry.get('fips')} is not "
                                f"the crosswalk's {expected_fips} as of {reading_day}")
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
    # Mirrors darkocean/continuity.py's own BATCH, independently reimplemented
    # here rather than imported — this function is the second implementation
    # of criteria group N and does not share code with the first.
    batch_size = 40

    # What the readings preserved, first sighting wins — the same origin the
    # probe uses, rebuilt independently here.
    preserved: dict[str, dict] = {}
    for path in sorted((root / "darkocean" / "readings").glob("*.json")):
        reading = load(path)
        day = reading.get("date", path.stem)
        for acquisition in reading.get("acquisitions", []):
            pid = acquisition.get("id")
            if pid and pid not in preserved:
                entry = dict(acquisition)
                entry["_first_seen"] = day
                preserved[pid] = entry

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

        # A product only counts as absent if the batch it fell in was
        # actually answered — the same rule run.py itself applies — and only
        # products a reading dated on or before this record's own day could
        # have been probed for at all (a later reading's products did not
        # exist yet on this record's night).
        day = record.get("date", path.stem)
        ids = sorted(pid for pid, entry in preserved.items()
                     if entry.get("_first_seen", "") <= day)
        failed_batches = {failure.get("batch")
                          for failure in record.get("failures", [])}
        wanted_gone = {pid for index, pid in enumerate(ids)
                      if (index // batch_size) + 1 not in failed_batches
                      and pid not in answered}

        got_gone = {catch.get("id") for catch in record.get("catches", [])
                   if catch.get("kind") == "gone_from_catalog"}
        if got_gone != wanted_gone:
            problems.append(f"{name}: the recorded catalog-absences do not "
                            "match the recomputation from the preserved "
                            f"readings ({sorted(got_gone)} vs "
                            f"{sorted(wanted_gone)})")

        for catch in record.get("catches", []):
            if catch.get("kind") != "gone_from_catalog":
                continue
            if catch.get("current") is not None:
                problems.append(f"{name}: gone_from_catalog catch on "
                                f"{catch.get('id')} names a current value — "
                                "the catalog did not omit it")
            entry = basis.get(catch.get("id"), {})
            expected = {field: entry[field] for field in compared
                       if field in entry}
            if catch.get("preserved") != expected:
                problems.append(f"{name}: gone_from_catalog catch on "
                                f"{catch.get('id')} reports a preserved value "
                                "the register does not hold — a "
                                "reconciliation, which group N forbids")

        text = json.dumps(record, ensure_ascii=False)
        if '"mmsi"' in text.lower():
            problems.append(f"{name}: a vessel identity leaked into a "
                            "derived record")


# ---------------------------------------------------------------------------
# Memory Hole: the institutional wording, rechecked.
#
# Restated on purpose, like Dark Ocean's grid above: the verifier must not
# import the code under audit. Everything below — the tag strip, the validity
# gate, the sentence diff, the event rules, the sampling draw — is a second
# implementation of the same written specification, so a reading that agrees
# with itself still has to agree with an independent recomputation from the
# preserved bytes.
# ---------------------------------------------------------------------------
_MH_SAMPLE_PER_INSTITUTION = 5
_MH_MIN_TOKENS = 60
_MH_MIN_PROSE_SENTENCES = 3
_MH_CONSENT_MAX_TOKENS = 400
_MH_CONSENT_MIN_MARKERS = 2
_MH_ALIGN_FLOOR = 0.5
_MH_PROSE_MIN_TOKENS = 5
_MH_PROSE_MAX_TOKENS = 60
_MH_PROSE_MIN_STOPWORD_RATIO = 0.18

_MH_CHALLENGE = (
    "verifying your browser", "incident id", "attention required",
    "just a moment", "checking your browser",
    "enable javascript and cookies to continue", "please enable cookies",
    "ray id", "access denied", "request unsuccessful", "bot detection",
    "ihre anfrage konnte nicht verarbeitet werden", "zugriff verweigert")
_MH_CONSENT = (
    "cookie", "cookies", "consent", "einwilligung", "datenschutzerklärung",
    "privacy policy", "matomo", "google analytics", "tracking", "opt-out",
    "opt out", "notwendige", "essenziell", "third-party")
_MH_STOPWORDS = set(
    "the a an of and or to in on for with as by that this is are was were be "
    "been has have had it its their they we you at from which who will not no "
    "but than into under over between about can may should would these those "
    "our your how der die das und oder zu im auf für mit als von dem den des "
    "ein eine einer ist sind war waren sein hat haben es sie wir an aus durch "
    "über unter zwischen nicht kein keine aber dass wird werden soll sollen "
    "muss diese dieser ihre unser wie".split())

_MH_WS = re.compile(r"\s+")
_MH_SENT = re.compile(r"(?<=[.!?])\s+")
_MH_WORD_ONLY = re.compile(r"[^\W\d_]+", re.UNICODE)
_MH_TOKEN = re.compile(r"[^\W_]+", re.UNICODE)
_MH_NUMERIC = re.compile(r"^\d[\d.,]*$")
_MH_YEAR = re.compile(r"^(?:19|20)\d{2}$")
_MH_MONTH = re.compile(
    r"\b(?:january|february|march|april|may|june|july|august|september"
    r"|october|november|december|januar|februar|märz|mai|juni|juli|august"
    r"|september|oktober|november|dezember)\b", re.I)
_MH_NEGATION = re.compile(
    r"\b(?:no|not|never|none|kein|keine|keinen|nicht|niemals)\b", re.I)
_MH_COMMIT = re.compile(
    r"\b(?:will|shall|must|commit|commits|committed|pledge|pledged|pledges"
    r"|wird|werden|muss|müssen|soll|sollen|verpflichtet)\b", re.I)
_MH_ATTRIBUTION = re.compile(
    r"\b(?:according to|as stated by|said|says|stated|told|announced by"
    r"|spokesperson|spokeswoman|spokesman|director|minister|president"
    r"|commissioner|chairman|chairwoman|chair of|head of|dr\.|prof\."
    r"|laut|zufolge|sagte|sagt|erklärte|betonte|teilte mit|nach angaben"
    r"|sprecher|sprecherin|präsident|präsidentin|minister|ministerin"
    r"|staatssekretär|direktor|direktorin|leiter|leiterin|vorstand)\b", re.I)
_MH_NUMBER_SIG = re.compile(
    r"(?<!\w)\d[\d.,]*\s?(?:%|percent|prozent|mio|million|millionen|mrd"
    r"|billion|bn)?", re.I)
_MH_DATE_SIG = re.compile(
    r"\b(?:19|20)\d{2}\b"
    r"|\b\d{1,2}\.\s?\d{1,2}\.\s?(?:19|20)\d{2}\b"
    r"|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"
    r"|januar|februar|märz|mai|juni|juli|oktober|dezember)\b", re.I)
_MH_CAPWORD = re.compile(r"[A-ZÄÖÜ][\wÄÖÜäöüß]+")
_MH_WEIGHTS = {"number": 2, "date": 2, "named_entity": 1, "negation": 2,
               "commitment_verb": 3}
_MH_SKIP_TAGS = {"script", "style", "nav", "header", "footer", "aside",
                 "noscript", "title", "head", "svg", "form"}


class _MhStrip(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip = 0
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in _MH_SKIP_TAGS:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in _MH_SKIP_TAGS and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self._buf.append(data)

    def text(self) -> str:
        return _MH_WS.sub(" ", " ".join(self._buf)).strip()


def _mh_text(data: bytes) -> str:
    for encoding in ("utf-8", "cp1252"):
        try:
            html = data.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        html = data.decode("utf-8", errors="replace")
    if not html.strip():
        return ""
    parser = _MhStrip()
    try:
        parser.feed(html)
    except Exception:  # noqa: BLE001
        pass
    return parser.text()


def _mh_sentences(text: str) -> list[str]:
    return [s.strip() for s in _MH_SENT.split(text.strip()) if s.strip()]


def _mh_is_prose(text: str) -> bool:
    n = len(text.split())
    if n < _MH_PROSE_MIN_TOKENS or n > _MH_PROSE_MAX_TOKENS:
        return False
    words = [w.lower() for w in _MH_WORD_ONLY.findall(text)]
    if not words:
        return False
    stop = sum(1 for w in words if w in _MH_STOPWORDS)
    return stop / len(words) >= _MH_PROSE_MIN_STOPWORD_RATIO


def _mh_gate(text: str, status) -> tuple[bool, str]:
    if str(status) != "200":
        return False, f"status_{status}"
    low = text.lower()
    if any(m in low for m in _MH_CHALLENGE):
        return False, "challenge_fingerprint"
    tokens = len(text.split())
    if tokens < _MH_MIN_TOKENS:
        return False, "too_short"
    markers = sum(1 for m in _MH_CONSENT if m in low)
    if markers >= _MH_CONSENT_MIN_MARKERS and tokens < _MH_CONSENT_MAX_TOKENS:
        return False, "consent_boilerplate"
    prose = [s for s in _mh_sentences(text) if _mh_is_prose(s)]
    if len(prose) < _MH_MIN_PROSE_SENTENCES:
        return False, "not_prose"
    return True, "ok"


def _mh_similarity(a: str, b: str) -> float:
    ta = {t.casefold() for t in _MH_TOKEN.findall(a)}
    tb = {t.casefold() for t in _MH_TOKEN.findall(b)}
    union = ta | tb
    return len(ta & tb) / len(union) if union else 0.0


def _mh_diff(before: str, after: str):
    import difflib
    a, b = _mh_sentences(before), _mh_sentences(after)
    removed: list[str] = []
    added: list[str] = []
    pairs: list[tuple[str, str]] = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
            a=a, b=b, autojunk=False).get_opcodes():
        if tag == "delete":
            removed.extend(a[i1:i2])
        elif tag == "insert":
            added.extend(b[j1:j2])
        elif tag == "replace":
            left, right = a[i1:i2], b[j1:j2]
            free = list(range(len(right)))
            taken: set[int] = set()
            for i, sentence in enumerate(left):
                best, best_score = None, _MH_ALIGN_FLOOR
                for j in free:
                    score = _mh_similarity(sentence, right[j])
                    if score > best_score:
                        best, best_score = j, score
                if best is not None:
                    pairs.append((sentence, right[best]))
                    free.remove(best)
                    taken.add(i)
            removed.extend(s for i, s in enumerate(left) if i not in taken)
            added.extend(right[j] for j in free)
    return removed, added, pairs


def _mh_salience(text: str) -> int:
    counts = {
        "number": len(_MH_NUMBER_SIG.findall(text)),
        "date": len(_MH_DATE_SIG.findall(text)),
        "negation": len(_MH_NEGATION.findall(text)),
        "commitment_verb": len(_MH_COMMIT.findall(text)),
        "named_entity": sum(
            1 for sentence in _MH_SENT.split(text)
            for word in sentence.split()[1:] if _MH_CAPWORD.match(word)),
    }
    return sum(_MH_WEIGHTS[k] * min(v, 5) for k, v in counts.items() if v > 0)


def _mh_numeric(tokens: list[str]) -> dict[str, int]:
    counted: dict[str, int] = {}
    for token in tokens:
        if _MH_NUMERIC.match(token):
            counted[token] = counted.get(token, 0) + 1
    return counted


def _mh_pair_types(before: str, after: str) -> list[str]:
    found: list[str] = []
    nb = _mh_numeric(_MH_TOKEN.findall(before))
    na = _mh_numeric(_MH_TOKEN.findall(after))
    if nb != na:
        changed = [t for t, n in nb.items() for _ in range(max(0, n - na.get(t, 0)))]
        changed += [t for t, n in na.items() for _ in range(max(0, n - nb.get(t, 0)))]
        if any(_MH_YEAR.match(t) for t in changed):
            found.append("date_shifted")
        if any(not _MH_YEAR.match(t) for t in changed):
            found.append("number_revised")
    elif _MH_MONTH.search(before) and not _MH_MONTH.search(after):
        found.append("date_shifted")
    if len(_MH_NEGATION.findall(before)) != len(_MH_NEGATION.findall(after)):
        found.append("negation_flipped")
    if _MH_COMMIT.findall(before) and not _MH_COMMIT.findall(after):
        found.append("commitment_removed")
    if _MH_ATTRIBUTION.search(before) and not _MH_ATTRIBUTION.search(after):
        found.append("attribution_removed")
    return found


def _mh_removal_types(text: str) -> list[str]:
    found: list[str] = []
    if _MH_COMMIT.findall(text):
        found.append("commitment_removed")
    if _MH_ATTRIBUTION.search(text):
        found.append("attribution_removed")
    return found


def _mh_events(removed: list[str], pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """(type, sha256 of the before passage), sorted — the projection a reading
    is held to."""
    out: list[tuple[str, str]] = []
    for before, after in pairs:
        if not (_mh_is_prose(before) or _mh_is_prose(after)):
            continue
        digest = hashlib.sha256(before.encode("utf-8")).hexdigest()
        out.extend((kind, digest) for kind in _mh_pair_types(before, after))
    for passage in removed:
        if not _mh_is_prose(passage):
            continue
        digest = hashlib.sha256(passage.encode("utf-8")).hexdigest()
        out.extend((kind, digest) for kind in _mh_removal_types(passage))
    return sorted(out)


def _mh_rows(path: Path) -> list[dict]:
    raw = path.read_bytes().decode("utf-8", errors="replace").strip()
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return []
    if not parsed or len(parsed) < 2:
        return []
    rows = [{"timestamp": str(r[0]), "original": str(r[1]),
             "statuscode": str(r[2]), "digest": str(r[3])}
            for r in parsed[1:] if len(r) >= 4]
    rows.sort(key=lambda r: r["timestamp"])
    return rows


def _mh_history_class(rows: list[dict], day: str) -> tuple[str, str]:
    stamp = day.replace("-", "")
    rows = [r for r in rows if r["timestamp"] <= stamp + "235959"]
    if not rows:
        return "unverifiable", "no_capture_in_archive"
    newest = rows[-1]
    if not newest["timestamp"].startswith(stamp):
        return "unchanged", "no_new_digest_on_day"
    earlier_ok = [r for r in rows[:-1] if r["statuscode"] == "200"]
    if newest["statuscode"] == "200":
        if not earlier_ok:
            return "unverifiable", "no_earlier_capture"
        return "changed_candidate", "new_digest"
    if newest["statuscode"].startswith("4"):
        return "deletion_candidate", f"archive_status_{newest['statuscode']}"
    return "unverifiable", f"archive_status_{newest['statuscode']}"


def check_memoryhole_verdicts(root: Path, problems: list[str]) -> None:
    """Verdict files are estimates delivered by the discovery pass — the
    routine channel, Frank's decision of 2026-08-15: one channel for all the
    practice's model work instead of a second billing path. A verdicts file
    annotates a committed reading, it never amends one. Checked here: every
    verdict points at an abstention its reading actually carries, stays
    inside the committed type set and the nightly cap, names its model, and
    wears the estimated flag — a verdict without one would read as a
    finding, which it is not."""
    allowed = {"number_revised", "date_shifted", "negation_flipped",
               "commitment_removed", "attribution_removed", "none_of_these"}
    for path in sorted(root.glob("memoryhole/verdicts/*.json")):
        name = path.stem
        try:
            block = load(path)
        except (json.JSONDecodeError, UnicodeDecodeError):
            problems.append(f"memoryhole verdicts {name}: unparseable")
            continue
        if block.get("date") != name:
            problems.append(f"memoryhole verdicts {name}: date field "
                            f"disagrees with filename")
        reading_path = root / "memoryhole" / "readings" / f"{name}.json"
        if not reading_path.exists():
            problems.append(f"memoryhole verdicts {name}: no reading to "
                            f"annotate")
            continue
        reading = load(reading_path)
        abstained = {a.get("before_sha256")
                     for entry in reading.get("entries", [])
                     for a in entry.get("abstentions", [])}
        if block.get("estimated") is not True:
            problems.append(f"memoryhole verdicts {name}: not labelled "
                            f"estimated")
        if not block.get("model"):
            problems.append(f"memoryhole verdicts {name}: no model id")
        cap = block.get("cap")
        verdicts = block.get("verdicts", [])
        if not isinstance(cap, int) or len(verdicts) > cap:
            problems.append(f"memoryhole verdicts {name}: {len(verdicts)} "
                            f"verdicts against cap {cap!r}")
        for i, item in enumerate(verdicts):
            if item.get("estimated") is not True:
                problems.append(f"memoryhole verdicts {name}[{i}]: not "
                                f"labelled estimated")
            if item.get("type") not in allowed:
                problems.append(f"memoryhole verdicts {name}[{i}]: unknown "
                                f"type {item.get('type')!r}")
            if item.get("before_sha256") not in abstained:
                problems.append(f"memoryhole verdicts {name}[{i}]: no "
                                f"matching abstention in the reading")


def check_memoryhole(root: Path, registry_files: dict,
                     problems: list[str]) -> None:
    """Recompute every Memory Hole reading from the bytes it rests on."""
    base = root / "memoryhole"
    if not base.exists():
        return
    watchlist_path = base / "watchlist.json"
    if not watchlist_path.exists():
        problems.append("memoryhole/ exists without watchlist.json")
        return
    watchlist = load(watchlist_path)
    excluded = set(watchlist.get("excluded", {}).get("urls", []))
    control_urls = {c["url"] for c in watchlist.get("controls", [])}
    if not excluded:
        problems.append("memoryhole watchlist: chamber 1's pages are not "
                        "named, so nothing proves they are avoided")
    for entry in watchlist.get("institutions", []):
        if not isinstance(entry.get("probe"), dict):
            problems.append(f"memoryhole watchlist {entry.get('slug')}: no "
                            "recorded live probe for its query strategy")

    for path in sorted(base.glob("readings/*.json")):
        reading = load(path)
        day = path.stem
        name = f"memoryhole {day}"
        if reading.get("date") != day:
            problems.append(f"{name}: date field disagrees with file name")

        entries = reading.get("entries", [])
        # every referenced byte must exist and be manifested
        for entry in entries:
            refs = [entry.get("history")]
            for side in ("before", "after"):
                capture = (entry.get("captures") or {}).get(side) or {}
                refs.append(capture.get("file"))
            for ref in [r for r in refs if r]:
                if not (root / ref).exists():
                    problems.append(f"{name}: source {ref} is missing")
                elif ref not in registry_files:
                    problems.append(f"{name}: source {ref} is not manifested")

        # the day's sample, redrawn from the preserved discovery answers
        sampled = {e["url"] for e in entries if e.get("kind") == "sampled"}
        expected: set[str] = set()
        for institution in reading.get("institutions", []):
            source = institution.get("source")
            if not source or not (root / source).exists():
                continue
            urls = sorted({r["original"] for r in _mh_rows(root / source)})
            if institution.get("urls_seen") != len(urls):
                problems.append(
                    f"{name}/{institution.get('slug')}: urls_seen "
                    f"{institution.get('urls_seen')} is not the {len(urls)} "
                    "recounted from the preserved discovery answer")
            eligible = [u for u in urls if u not in excluded]
            eligible.sort(key=lambda u: hashlib.sha256(
                f"{day}|{u}".encode("utf-8")).hexdigest())
            drawn = {u for u in eligible[:_MH_SAMPLE_PER_INSTITUTION]
                     if u not in control_urls}
            expected |= drawn
        if expected != sampled:
            problems.append(f"{name}: the sampled pages are not the "
                            "deterministic draw from the preserved discovery "
                            f"answers ({len(sampled)} recorded, "
                            f"{len(expected)} redrawn)")

        for entry in entries:
            eid = f"{name}/{entry.get('id')}"
            if entry.get("url") in excluded:
                problems.append(f"{eid}: is a page chamber 1 already watches")
            history = entry.get("history")
            if not history or not (root / history).exists():
                continue
            kind, reason = _mh_history_class(_mh_rows(root / history), day)
            recorded = entry.get("class")

            if kind == "deletion_candidate":
                result = entry.get("recheck") or {}
                if recorded == "gone" and result.get("class") not in (
                        "gone_404", "gone_410"):
                    problems.append(f"{eid}: called gone without a live "
                                    "recheck saying so")
                if recorded not in ("gone", "unverifiable"):
                    problems.append(f"{eid}: a 4xx candidate ended as "
                                    f"{recorded!r} instead of gone or "
                                    "unverifiable")
                continue
            if recorded == "gone":
                problems.append(f"{eid}: gone, but the preserved history shows "
                                f"{kind}")
                continue
            if kind == "unchanged" and recorded != "unchanged":
                problems.append(f"{eid}: recorded {recorded!r}, the preserved "
                                "history shows no new digest that day")
            if kind == "changed_candidate" and recorded == "unchanged":
                problems.append(f"{eid}: recorded unchanged, the preserved "
                                "history shows a new digest that day")
            if kind == "unverifiable" and recorded == "changed":
                problems.append(f"{eid}: recorded changed on a history that "
                                f"is {reason}")

            captures = entry.get("captures") or {}
            if not captures:
                continue
            texts = {}
            gates = {}
            for side in ("before", "after"):
                ref = (captures.get(side) or {}).get("file")
                if not ref or not (root / ref).exists():
                    texts = {}
                    break
                texts[side] = _mh_text((root / ref).read_bytes())
                gates[side] = _mh_gate(texts[side],
                                       captures[side].get("archive_status"))
            if len(texts) != 2:
                continue
            for side, (valid, gate_reason) in gates.items():
                recorded_gate = (entry.get("gate") or {}).get(side) or {}
                if recorded_gate.get("valid") != valid or \
                        recorded_gate.get("reason") != gate_reason:
                    problems.append(
                        f"{eid}: the {side} gate verdict "
                        f"{recorded_gate.get('reason')!r} is not the "
                        f"{gate_reason!r} recomputed from the preserved bytes")
            if not (gates["before"][0] and gates["after"][0]):
                if recorded == "changed":
                    problems.append(f"{eid}: recorded changed although a "
                                    "capture fails the validity gate")
                continue

            removed, _added, pairs = _mh_diff(texts["before"], texts["after"])
            tokens = sum(len(p.split()) for p in removed)
            if entry.get("removed_tokens") != tokens:
                problems.append(f"{eid}: removed_tokens "
                                f"{entry.get('removed_tokens')} is not the "
                                f"{tokens} recomputed")
            expected_events = _mh_events(removed, pairs)
            got_events = sorted((e.get("type"), e.get("before_sha256"))
                                for e in entry.get("events", []))
            if got_events != expected_events:
                problems.append(f"{eid}: the typed events do not match the "
                                "recomputation from the preserved bytes "
                                f"({len(got_events)} recorded, "
                                f"{len(expected_events)} recomputed)")
            for event in entry.get("events", []):
                for field in ("before", "after"):
                    text = event.get(field)
                    if text and _MH_ATTRIBUTION.search(text):
                        problems.append(
                            f"{eid}: an event carries a passage with an "
                            "ascription to a person as text (I8 says digest)")

        # rates, recounted
        counts = {"unchanged": 0, "changed": 0, "unverifiable": 0, "gone": 0}
        for entry in entries:
            if entry.get("class") in counts:
                counts[entry["class"]] += 1
            else:
                problems.append(f"{name}: entry {entry.get('id')} has class "
                                f"{entry.get('class')!r}")
        recorded_rates = reading.get("rates", {})
        if recorded_rates.get("counts") != counts:
            problems.append(f"{name}: class counts {recorded_rates.get('counts')} "
                            f"are not the {counts} recounted")
        if recorded_rates.get("examined") != len(entries):
            problems.append(f"{name}: examined "
                            f"{recorded_rates.get('examined')} is not "
                            f"{len(entries)}")

        # the model layer never becomes a finding on its own
        model = reading.get("model") or {}
        if model.get("state", "").startswith("on"):
            if not all(v.get("estimated") for v in model.get("verdicts", [])):
                problems.append(f"{name}: a model verdict is not marked "
                                "estimated")
            if model.get("submitted", 0) > model.get("cap", 0):
                problems.append(f"{name}: the model layer exceeded its "
                                "nightly cap")
        elif model.get("verdicts"):
            problems.append(f"{name}: model verdicts without a running model "
                            "layer")


def check_foreknown_reaction_series(root: Path, problems: list[str]) -> None:
    """The reaction series in a resolution, recomputed from the readings.

    A second implementation on purpose (added 2026-08-22 with the join
    itself): the resolver's summary is checked against the committed nights,
    not against the resolver. A claim about what money and attention did while
    a warning ran is worth exactly as much as its arithmetic survives.
    """
    readings = {}
    for path in sorted(root.glob("foreknown/reaction/readings/*.json")):
        doc = load(path)
        readings[doc.get("date") or path.stem] = doc

    for res_file in sorted(root.glob("foreknown/resolutions/*.json")):
        resolution = load(res_file)
        series = resolution.get("reaction")
        if series is None:
            continue
        fid = resolution.get("future", res_file.stem)
        nights = series.get("nights")
        if not isinstance(nights, list) or not nights:
            problems.append(f"resolution {fid}: reaction block without nights")
            continue

        carried = sorted(date for date, doc in readings.items()
                         if (doc.get("futures") or {}).get(fid))
        listed = [night.get("date") for night in nights]
        if listed != sorted(listed):
            problems.append(f"resolution {fid}: reaction nights out of order")
        # Every watched night up to the resolution must be listed, and nothing
        # may be listed that no reading carries. Nights *after* the resolution
        # are deliberately not demanded: a future can REAPPEAR and re-enter the
        # readings, and an append-only resolution cannot grow to follow it —
        # requiring equality would turn that legal event into a red verifier on
        # an untouched record, which is the deadlock shape that cost this
        # practice two nights in August.
        cutoff = (resolution.get("resolved_at") or "9999")[:10]
        owed = [date for date in carried if date < cutoff]
        missing = sorted(set(owed) - set(listed))
        extra = sorted(set(listed) - set(carried))
        if missing or extra:
            problems.append(
                f"resolution {fid}: reaction nights do not match the committed "
                f"readings (missing {missing}, not in any reading {extra})")

        for night in nights:
            doc = readings.get(night.get("date"))
            if doc is None:
                problems.append(f"resolution {fid}: reaction night "
                                f"{night.get('date')} has no committed reading")
                continue
            entry = (doc.get("futures") or {}).get(fid) or {}
            money = entry.get("money") or {}
            attention = entry.get("attention") or {}
            for key, actual in (
                    ("attention_day", doc.get("attention_day")),
                    ("articles", attention.get("articles")),
                    ("ratio_to_baseline", attention.get("ratio_to_baseline")),
                    ("has_fts_plan_match", money.get("has_fts_plan_match")),
                    ("plan_requirements_usd", money.get("plan_requirements_usd")),
                    ("plan_funded_usd", money.get("plan_funded_usd"))):
                if night.get(key) != actual:
                    problems.append(
                        f"resolution {fid}: reaction night {night.get('date')} "
                        f"{key} says {night.get(key)!r}, the reading says "
                        f"{actual!r}")

        measured = series.get("measured") or {}
        if measured.get("nights_watched") != len(nights):
            problems.append(f"resolution {fid}: nights_watched "
                            f"{measured.get('nights_watched')!r} against "
                            f"{len(nights)} nights")
        rated = [n for n in nights if n.get("ratio_to_baseline") is not None]
        if rated:
            top = max(rated, key=lambda n: (n["ratio_to_baseline"], n["date"]))
            if (measured.get("attention_peak") or {}).get("date") != top["date"]:
                problems.append(f"resolution {fid}: attention peak is not the "
                                f"loudest committed night ({top['date']})")
        funded = [n for n in nights if n.get("plan_funded_usd") is not None
                  and n.get("has_fts_plan_match")]
        if funded:
            delta = funded[-1]["plan_funded_usd"] - funded[0]["plan_funded_usd"]
            if measured.get("money_funded_delta_usd") != delta:
                problems.append(
                    f"resolution {fid}: money delta "
                    f"{measured.get('money_funded_delta_usd')!r} against {delta} "
                    "from the readings")
        elif measured.get("money_plan_match") is not False:
            problems.append(f"resolution {fid}: no funded night, but the "
                            "record does not say the plan match is absent")
        if not series.get("limits"):
            problems.append(f"resolution {fid}: reaction series without its "
                            "own limits in the record")


def check_anchors(root: Path, problems: list[str]) -> None:
    """The OpenTimestamps anchors (D2): the ledger's claims against the bytes.

    Deliberately WITHOUT the ots client — this verifier is stdlib-only, and a check that
    needs an optional dependency is a check that quietly stops running. Everything below
    is readable from the files themselves:

      * a proof's own header carries the SHA-256 of the file it commits to, so the pairing
        proof <-> manifest is provable here rather than taken from the ledger's word;
      * the ledger's digests are recomputed from the manifests;
      * every manifest in the registers appears in the ledger, so a night cannot be
        silently dropped from the anchoring record (an unstamped night is legitimate and
        must be listed as such);
      * a proof declared complete names the Bitcoin blocks a reader can check.

    What stays out of reach here, stated rather than implied: whether a block actually
    contains the commitment. That needs a Bitcoin node — `ots verify -f <manifest> <proof>`
    — and no verifier of ours can stand in for one.
    """
    proofs_dir = root / "anchors"
    ledger_path = proofs_dir / "ledger.json"
    if not proofs_dir.exists():
        return  # nothing anchored yet — not a hole
    if not ledger_path.exists():
        problems.append("anchors/ exists without anchors/ledger.json")
        return

    ledger = load(ledger_path)
    entries = ledger.get("anchors", [])
    listed = {e.get("manifest") for e in entries}

    # every register night must appear in the ledger, anchored or not
    for manifest in sorted(root.glob("*/**/snapshots/*/manifest.json")):
        rel = manifest.relative_to(root).as_posix()
        if rel not in listed:
            problems.append(f"anchor ledger omits {rel}")

    counted = {"complete": 0, "pending": 0}
    for entry in entries:
        rel = entry.get("manifest", "?")
        manifest = root / rel
        if not manifest.exists():
            problems.append(f"anchor ledger names a manifest that is gone: {rel}")
            continue
        digest = sha256_file(manifest)
        if entry.get("sha256") != digest:
            problems.append(f"anchor {rel}: ledger digest diverges from the bytes")
        state = entry.get("state")
        if state in counted:
            counted[state] += 1
        if state in {"pending", "complete"}:
            proof = root / entry.get("proof", "")
            if not proof.exists():
                problems.append(f"anchor {rel}: proof {entry.get('proof')} missing")
                continue
            raw = proof.read_bytes()
            if not raw.startswith(OTS_MAGIC):
                problems.append(f"anchor {rel}: {entry.get('proof')} is not an "
                                "OpenTimestamps proof")
                continue
            # magic, one version byte, then the hash op — 0x08 is SHA-256 — then 32 bytes
            head = len(OTS_MAGIC) + 1
            if raw[head] != OTS_SHA256_OP:
                problems.append(f"anchor {rel}: proof commits with an unexpected "
                                f"hash op {raw[head]:#04x}")
                continue
            committed = raw[head + 1:head + 33].hex()
            if committed != digest:
                problems.append(f"anchor {rel}: proof commits to {committed[:16]}…, "
                                f"the manifest hashes to {digest[:16]}…")
        if state == "complete" and not re.search(r"bitcoin block\(s\) \d{6,}",
                                                 entry.get("evidence", "")):
            # "attestation present" is our assertion; a height is checkable against a chain
            problems.append(f"anchor {rel}: complete without a named Bitcoin block")

    for key, claimed in (("complete", counted["complete"]), ("pending", counted["pending"])):
        if ledger.get("counts", {}).get(key) != claimed:
            problems.append(f"anchor ledger counts {key}={ledger.get('counts', {}).get(key)}, "
                            f"the entries say {claimed}")

    for orphan in sorted(proofs_dir.rglob("*.ots")):
        rel = orphan.relative_to(proofs_dir)
        if not (root / rel.parent / rel.name[:-4]).exists():
            problems.append(f"orphan proof {orphan.relative_to(root)}: "
                            "the manifest it commits to is gone")
    for leftover in sorted(proofs_dir.rglob("*.bak")):
        problems.append(f"client backup committed: {leftover.relative_to(root)}")


def _closed_at(history: list[dict], resolved_at: str | None) -> bool:
    """Whether the future's last history event at or before resolved_at is a
    closure (CLOSED_BY_SOURCE or DISSIPATED)."""
    if not resolved_at:
        return False

    def as_utc(ts: str) -> datetime | None:
        try:
            parsed = datetime.fromisoformat(ts)
        except (TypeError, ValueError):
            return None
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)

    cutoff = as_utc(resolved_at)
    if cutoff is None:
        return False
    last = None
    for event in history:
        ts = as_utc(event.get("ts", ""))
        if ts is not None and ts <= cutoff:
            last = event
    return last is not None and last.get("event") in ("CLOSED_BY_SOURCE",
                                                      "DISSIPATED")


RETIRABLE = ("foreknown", "darkocean")
DATED_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})(\.json)?$")


def check_retired(root: Path, problems: list[str]) -> None:
    """Closing records of retired projects (The Foreknown and Dark Ocean,
    2026-10-04: <project>/RETIRED.json).

    A retired project ends on its last night: a dated night or reading
    recorded after it would be the project running on under a record that
    says it stopped — the one silent restart this check exists to make loud.
    The file's shape is held too, because the export, the staleness check
    and, for The Foreknown, the stage and the moments all read it."""
    for project in RETIRABLE:
        rel = f"{project}/RETIRED.json"
        path = root / rel
        if not path.exists():
            continue
        record = load(path)
        for key in ("project", "status", "last_night", "decided", "record",
                    "reason"):
            if not record.get(key):
                problems.append(f"{rel}: missing {key}")
        if record.get("status") != "RETIRED" or record.get("project") != project:
            problems.append(f"{rel}: must say status RETIRED for project {project}")
        last = str(record.get("last_night") or "")
        if record.get("record") and not (root / record["record"]).exists():
            problems.append(f"{rel}: record {record['record']} does not exist")
        for entry in sorted((root / project).rglob("*")):
            match = DATED_NAME.match(entry.name)
            if match and last and match.group(1) > last:
                problems.append(
                    f"{entry.relative_to(root).as_posix()}: recorded after the "
                    f"project was retired (last night {last})")


IV_BASE = "interval/snapshots"
IV_THETAS = (0.05, 0.10, 0.25)
IV_KS = (2, 3)
IV_AXES = ("date", "firstReportedDate")
IV_SETS = ("fsc", "total")
IV_DRIVERS = ("drought", "conflict", "economic", "mixed", "unassigned")
IV_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec")
IV_PAGE = re.compile(r"^(fsc|total)-([0-9_]+)-p(\d{3})\.json$")


def _iv_index(month: str) -> int:
    return int(month[:4]) * 12 + int(month[5:7]) - 1


def _iv_month(index: int) -> str:
    return f"{index // 12:04d}-{index % 12 + 1:02d}"


def _iv_warning(text: str) -> dict[str, list[dict]]:
    """IPC national long table -> per country, the analyses with W, recomputed
    without the practice package (The Interval, increment 2 semantics)."""
    import csv
    import io
    keyed: dict[tuple, list[dict]] = {}
    block = None
    for row in csv.DictReader(io.StringIO(text)):
        if row["Phase"] == "all":
            mon, year = row["Date of analysis"].split()
            block = {"pop": int(row["Total country population"]),
                     "analysed": int(row["Number"]), "p4": 0, "p5": 0}
            key = (row["Country"],
                   f"{int(year):04d}-{IV_MONTHS.index(mon) + 1:02d}",
                   row["Validity period"])
            keyed.setdefault(key, []).append(block)
        elif row["Phase"] in ("4", "5"):
            block["p" + row["Phase"]] = int(row["Number"])
    out: dict[str, list[dict]] = {}
    months = sorted({(c, m) for c, m, _ in keyed})
    for country, month in months:
        picked = {}
        for period in ("first projection", "second projection"):
            cands = keyed.get((country, month, period), [])
            if cands:
                picked[period] = max(cands, key=lambda b: b["analysed"])
        shares = {p: (b["p4"] + b["p5"]) / b["pop"] if b["pop"] > 0 else None
                  for p, b in picked.items()}
        best = [(s, picked[p]) for p, s in shares.items() if s is not None]
        w, used = max(best, key=lambda x: x[0]) if best else (None, None)
        out.setdefault(country, []).append({
            "month": month, "w": w,
            "w_first": shares.get("first projection"),
            "w_second": shares.get("second projection"),
            "coverage": used["analysed"] / used["pop"] if used else None,
            "blocks": max(len(keyed.get((country, month, p), []))
                          for p in ("current", "first projection",
                                    "second projection")),
            "phase5": any(b["p5"] > 0 for b in picked.values())})
    return out


def _iv_onsets(series: list[dict], theta: float) -> list[str]:
    found, quiet_from = [], None
    for p in series:
        if p["w"] is None:
            continue
        if p["w"] < theta:
            quiet_from = quiet_from or p["month"]
        else:
            if quiet_from and _iv_index(p["month"]) - _iv_index(quiet_from) >= 6:
                found.append(p["month"])
            quiet_from = None
    return found


def _iv_pages(root: Path, iso3: str, tag: str, years: str,
              before: str | None = None):
    """Newest complete page set of one FTS query: (day, [files]) or None;
    with `before`, among earlier snapshot days only."""
    base = root / IV_BASE
    days = sorted((p.name for p in base.iterdir() if p.is_dir()), reverse=True) \
        if base.exists() else []
    for day in days:
        if before is not None and day >= before:
            continue
        mpath = base / day / "manifest.json"
        if not mpath.exists():
            continue
        prefix = f"{IV_BASE}/{day}/fts/{iso3}/"
        found = []
        for e in load(mpath).get("entries", []):
            if not e["file"].startswith(prefix):
                continue
            m = IV_PAGE.match(e["file"][len(prefix):])
            if m and m.group(1) == tag and m.group(2) == years.replace(",", "_"):
                found.append((int(m.group(3)), e["file"], e["http_status"]))
        found.sort()
        if (not found or [f[0] for f in found] != list(range(1, len(found) + 1))
                or any(f[2] != 200 for f in found)
                or (load(root / found[-1][1]).get("meta") or {}).get("nextLink")):
            continue
        return day, [f[1] for f in found]
    return None


def _iv_money(root: Path, iso3: str, t0: str, tag: str) -> dict:
    i0 = _iv_index(t0)
    first, last = i0 - 12, i0 + 11
    years = ",".join(str(y) for y in range(first // 12, last // 12 + 1))
    found = _iv_pages(root, iso3, tag, years)
    if not found:
        return {"status": "not_preserved", "boundary_years": years}
    day, pages = found
    flows: dict[str, dict] = {}
    for rel in pages:
        for f in (load(root / rel).get("data") or {}).get("flows") or []:
            fid, ver = str(f["id"]), int(f.get("versionId") or 0)
            if fid not in flows or ver > flows[fid]["v"]:
                flows[fid] = {"v": ver, "amount": float(f.get("amountUSD") or 0),
                              "ok": f.get("boundary") == "incoming"
                              and f.get("status") in ("paid", "commitment"),
                              "date": f["date"][:7],
                              "firstReportedDate": (f.get("firstReportedDate")
                                                    or f["date"])[:7]}
    as_of = _iv_index(day[:7])
    cells = []
    for axis in IV_AXES:
        series = {i: 0.0 for i in range(first, last + 1)}
        for fid in sorted(flows):
            f = flows[fid]
            idx = _iv_index(f[axis])
            if f["ok"] and idx in series:
                series[idx] += f["amount"]
        base = _median([series[i0 - i] for i in range(1, 13)])
        after = list(range(i0, min(last, as_of) + 1))
        half = None
        if as_of >= last:
            total, run = sum(series[i] for i in after), 0.0
            for i in after:
                run += series[i]
                if total > 0 and run >= total / 2:
                    half = _iv_month(i)
                    break
        for k in IV_KS:
            cell = {"k": k, "axis": axis, "baseline_usd": round(base, 2),
                    "t1": None, "gap_months": None, "open_months": None,
                    "half_month": half}
            hit = next((i for i in after if series[i] >= k * base), None) \
                if base > 0 else None
            if base <= 0:
                cell["status"] = "baseline_zero"
            elif hit is not None:
                cell.update(status="closed", t1=_iv_month(hit),
                            gap_months=hit - i0)
            elif as_of < last:
                cell.update(status="open", open_months=max(as_of - i0, 0))
            else:
                cell["status"] = "none_in_horizon"
            cells.append(cell)
    return {"status": "read", "boundary_years": years, "as_of": day[:7],
            "pages": pages, "pages_sha256": [sha256_file(root / p) for p in pages],
            "flows": len(flows),
            "flows_counted": sum(1 for f in flows.values() if f["ok"]),
            "cells": cells}


IV_OUTCOMES = ("preserved", "unchanged", "incomplete", "unavailable")


def _iv_shas(root: Path, files: list[str]) -> list[str]:
    day = files[0].split("/")[2]
    entries = {e["file"]: e for e in
               load(root / IV_BASE / day / "manifest.json").get("entries", [])}
    return [entries[f]["sha256"] for f in files]


def check_interval_readings(root: Path, problems: list[str]) -> None:
    """The Interval's weekly readings (V0 increment 5, 2026-10-13): every
    fetch-or-freeze decision is recomputed from the snapshot days before the
    reading, and every page hash the reading names must be the one the
    manifest holds (preserved) or the basis held (unchanged)."""
    for path in sorted((root / "interval" / "readings").glob("*.json")):
        rel = f"interval/readings/{path.name}"
        r = load(path)
        day = path.stem
        if r.get("schema") != "interval-reading-v1" or r.get("date") != day:
            problems.append(f"{rel}: schema or date does not match its name")
            continue
        grace = r.get("grace_months")
        if grace != 3:
            problems.append(f"{rel}: grace_months {grace!r}, expected 3")
            continue
        ipc = (r.get("ipc") or {}).get("snapshot") or ""
        ipc_day = ipc.split("/")[2] if ipc.count("/") >= 3 else ""
        if (not ipc.startswith(IV_BASE + "/") or ipc_day > day
                or not (root / ipc).exists()
                or sha256_file(root / ipc) != r["ipc"].get("sha256")):
            problems.append(f"{rel}: ipc snapshot {ipc!r} missing, later "
                            "than the reading, or with another hash")
            continue
        series = _iv_warning((root / ipc).read_text(encoding="utf-8"))
        keys = sorted({(c, t0) for theta in IV_THETAS
                       for c, s in series.items() for t0 in _iv_onsets(s, theta)})
        want = [(c, t0, tag) for c, t0 in keys for tag in IV_SETS]
        got = [(q.get("country"), q.get("t0"), q.get("set"))
               for q in r.get("queries", [])]
        if got != want:
            problems.append(f"{rel}: queries are not the episodes x sets of "
                            f"{ipc}")
            continue
        for q in r["queries"]:
            name = f"{rel}: {q['country']} {q['t0']} {q['set']}"
            i0 = _iv_index(q["t0"])
            years = ",".join(str(y) for y in
                             range((i0 - 12) // 12, (i0 + 11) // 12 + 1))
            end = _iv_month(i0 + 11)
            basis = _iv_pages(root, q["country"], q["set"], years, before=day)
            decision = ("frozen" if basis and _iv_index(basis[0][:7])
                        > _iv_index(end) + grace else "fetch")
            if (q.get("boundary_years"), q.get("window_end"),
                    q.get("basis_day"), q.get("decision")) != (
                    years, end, basis[0] if basis else None, decision):
                problems.append(f"{name}: decision differs from its "
                                "recomputation")
                continue
            if decision == "frozen":
                if "outcome" in q:
                    problems.append(f"{name}: frozen query carries an outcome")
                continue
            outcome = q.get("outcome")
            if outcome not in IV_OUTCOMES:
                problems.append(f"{name}: unknown outcome {outcome!r}")
            elif outcome == "unchanged":
                if not basis or q.get("pages_sha256") != _iv_shas(root, basis[1]):
                    problems.append(f"{name}: unchanged, but not the basis's "
                                    "page hashes")
            elif outcome in ("preserved", "incomplete"):
                prefix = (f"{IV_BASE}/{day}/fts/{q['country']}/{q['set']}-"
                          f"{years.replace(',', '_')}-p")
                mpath = root / IV_BASE / day / "manifest.json"
                entries = sorted((e["file"], e["sha256"]) for e in
                                 (load(mpath).get("entries", [])
                                  if mpath.exists() else [])
                                 if e["file"].startswith(prefix))
                if [h for _, h in entries] != q.get("pages_sha256"):
                    problems.append(f"{name}: preserved pages differ from "
                                    "the manifest")
                complete = _iv_pages(root, q["country"], q["set"], years,
                                     before=_iv_next_day(day))
                if (outcome == "preserved") != bool(complete
                                                    and complete[0] == day):
                    problems.append(f"{name}: outcome {outcome} contradicts "
                                    "the preserved pages")


def check_interval_experiment(root: Path, problems: list[str]) -> None:
    """The Interval's E-experiment (V0 increment 6, 2026-10-14): the
    criteria bind once committed, so they must predate the window. The file
    names consecutive Mondays (at least four, candidate document §6), its
    prose by hash, and no reading in the window may predate the commit.
    Dated addenda are held the same way."""
    import datetime as _dt
    rel = "interval/experiment.json"
    if not (root / rel).exists():
        return
    e = load(root / rel)
    try:
        committed = _dt.date.fromisoformat(e["committed"])
        weeks = [_dt.date.fromisoformat(w) for w in e["window"]["weeks"]]
        closes = _dt.date.fromisoformat(e["window"]["closes"])
        review = _dt.date.fromisoformat(e["window"]["review_from"])
        doc = root / e["document"]
    except (KeyError, TypeError, ValueError) as exc:
        problems.append(f"{rel}: malformed ({exc})")
        return
    if e.get("schema") != "interval-experiment-v1":
        problems.append(f"{rel}: unknown schema {e.get('schema')!r}")
    if len(weeks) < 4 or any(w.weekday() != 0 for w in weeks) or any(
            b - a != _dt.timedelta(days=7) for a, b in zip(weeks, weeks[1:])):
        problems.append(f"{rel}: window is not four or more consecutive "
                        "Mondays")
        return
    if not committed < weeks[0]:
        problems.append(f"{rel}: criteria committed {committed}, not before "
                        f"the window opens {weeks[0]}")
    if closes != weeks[-1] + _dt.timedelta(days=6) or review <= closes:
        problems.append(f"{rel}: closes/review_from do not follow the weeks")
    if not doc.exists() or sha256_file(doc) != e.get("document_sha256"):
        problems.append(f"{rel}: {e['document']} missing or changed "
                        "without its hash")
    if e.get("criteria", {}).get("A1_weeks_required") != len(weeks):
        problems.append(f"{rel}: A1 must require every week of the window")
    for day in e.get("pre_window_readings", []):
        if not day < weeks[0].isoformat() or not (
                root / "interval" / "readings" / f"{day}.json").exists():
            problems.append(f"{rel}: pre-window reading {day} missing or "
                            "inside the window")
    # Dated addenda (criteria §0, first one 2026-10-17): each binds like
    # the document itself, so it must predate the window and keep its hash.
    for a in e.get("addenda", []):
        day, adoc = a.get("date") or "", a.get("document") or ""
        if not day or not day < weeks[0].isoformat() or day < e["committed"]:
            problems.append(f"{rel}: addendum {adoc!r} dated {day!r}, not "
                            "between the criteria and the window")
        if not adoc or not (root / adoc).exists() or sha256_file(
                root / adoc) != a.get("document_sha256"):
            problems.append(f"{rel}: addendum {adoc!r} missing or changed "
                            "without its hash")


def check_planetary_experiment(root: Path, problems: list[str]) -> None:
    """Planetary Listening's E-experiment (V0 increment 4, 2026-10-19): the
    criteria bind once committed, so they must predate the first night. The
    window is at least the audit's fourteen nights, the prose is held by
    hash, and dated addenda the same way."""
    import datetime as _dt
    rel = "planetary/experiment.json"
    if not (root / rel).exists():
        return
    e = load(root / rel)
    try:
        committed = _dt.date.fromisoformat(e["committed"])
        first = _dt.date.fromisoformat(e["window"]["first"])
        count = int(e["window"]["nights"])
        closes = _dt.date.fromisoformat(e["window"]["closes"])
        review = _dt.date.fromisoformat(e["window"]["review_from"])
        crit = e["criteria"]
    except (KeyError, TypeError, ValueError) as exc:
        problems.append(f"{rel}: malformed ({exc})")
        return
    if e.get("schema") != "planetary-experiment-v1":
        problems.append(f"{rel}: unknown schema {e.get('schema')!r}")
    if count < 14:
        problems.append(f"{rel}: window shorter than the audit's 14 nights")
    if not committed < first:
        problems.append(f"{rel}: criteria committed {committed}, not before "
                        f"the first night {first}")
    if closes != first + _dt.timedelta(days=count - 1) or review <= closes:
        problems.append(f"{rel}: closes/review_from do not follow the nights")
    doc = root / e.get("document", "")
    if not e.get("document") or not doc.exists() or \
            sha256_file(doc) != e.get("document_sha256"):
        problems.append(f"{rel}: {e.get('document')} missing or changed "
                        "without its hash")
    if not 0 < crit.get("A1_min_nights", 0) <= count:
        problems.append(f"{rel}: A1 must require nights inside the window")
    if crit.get("A4_max_night_bytes", 0) > 400 * 1024:
        problems.append(f"{rel}: A4 above the audit's 400 KB a night")
    for day in e.get("pre_window_readings", []):
        if not day < first.isoformat() or not (
                root / "planetary" / "readings" / f"{day}.json").exists():
            problems.append(f"{rel}: pre-window reading {day} missing or "
                            "inside the window")
    for a in e.get("addenda", []):
        day, adoc = a.get("date") or "", a.get("document") or ""
        if not day or not day < first.isoformat() or day < e["committed"]:
            problems.append(f"{rel}: addendum {adoc!r} dated {day!r}, not "
                            "between the criteria and the window")
        if not adoc or not (root / adoc).exists() or sha256_file(
                root / adoc) != a.get("document_sha256"):
            problems.append(f"{rel}: addendum {adoc!r} missing or changed "
                            "without its hash")


def _iv_next_day(day: str) -> str:
    import datetime as _dt
    return (_dt.date.fromisoformat(day) + _dt.timedelta(days=1)).isoformat()


def check_interval(root: Path, problems: list[str]) -> None:
    """The Interval's register (V0 increment 4, 2026-10-12) is recomputed
    here from the committed snapshots and drivers.json, independently of the
    practice package, and must match the committed file exactly."""
    rel = "interval/register.json"
    if not (root / rel).exists():
        return
    drivers = {}
    dpath = root / "interval" / "drivers.json"
    for d in (load(dpath).get("drivers", []) if dpath.exists() else []):
        if d.get("driver") not in IV_DRIVERS:
            problems.append(f"interval/drivers.json: unknown driver {d.get('driver')!r}")
        elif d["driver"] != "unassigned" and not d.get("source"):
            problems.append(f"interval/drivers.json: {d.get('country')} "
                            f"{d.get('t0')}: driver without a source")
        drivers[(d.get("country"), d.get("t0"))] = d
    ipc = None
    base = root / IV_BASE
    for day in sorted((p.name for p in base.iterdir() if p.is_dir()),
                      reverse=True) if base.exists() else []:
        cand = f"{IV_BASE}/{day}/ipc/ipc_global_national_long.csv"
        mpath = base / day / "manifest.json"
        if mpath.exists() and any(e["file"] == cand
                                  for e in load(mpath).get("entries", [])):
            ipc = cand
            break
    if ipc is None:
        problems.append(f"{rel}: no committed IPC snapshot to recompute from")
        return
    series = _iv_warning((root / ipc).read_text(encoding="utf-8"))
    r6 = lambda x: None if x is None else round(x, 6)  # noqa: E731
    onsets: dict[tuple[str, str], list[str]] = {}
    censored = {}
    for theta in IV_THETAS:
        censored[f"{theta:.2f}"] = sorted(
            c for c, s in series.items()
            if next((p["w"] >= theta for p in s if p["w"] is not None), False))
        for c, s in series.items():
            for t0 in _iv_onsets(s, theta):
                onsets.setdefault((c, t0), []).append(f"{theta:.2f}")
    episodes = []
    for (country, t0), thetas in sorted(onsets.items()):
        p = next(x for x in series[country] if x["month"] == t0)
        d = drivers.get((country, t0))
        i0 = _iv_index(t0)
        episodes.append({
            "country": country, "t0": t0, "onset_at_theta": thetas,
            "w": r6(p["w"]), "w_first": r6(p["w_first"]),
            "w_second": r6(p["w_second"]), "coverage": r6(p["coverage"]),
            "blocks": p["blocks"], "phase5_projected": p["phase5"],
            "window": [_iv_month(i0 - 12), _iv_month(i0 + 11)],
            "driver": {"driver": d["driver"], "source": d.get("source")}
            if d else {"driver": "unassigned", "source": None},
            "money": {tag: _iv_money(root, country, t0, tag) for tag in IV_SETS},
        })
    expected = {
        "schema": "interval-register-v1", "ipc_snapshot": ipc,
        "ipc_sha256": sha256_file(root / ipc),
        "grid": {"theta": [f"{t:.2f}" for t in IV_THETAS], "k": list(IV_KS),
                 "axis": list(IV_AXES), "set": list(IV_SETS),
                 "quiet_months": 6, "baseline_months": 12,
                 "horizon_months": 12},
        "left_censored": censored, "episodes": episodes}
    committed = load(root / rel)
    if committed == expected:
        return
    if committed.get("episodes") != episodes:
        got = {(e.get("country"), e.get("t0")): e
               for e in committed.get("episodes", [])}
        for e in episodes:
            if got.get((e["country"], e["t0"])) != e:
                problems.append(f"{rel}: episode {e['country']} {e['t0']} "
                                "differs from its recomputation")
        extra = set(got) - {(e["country"], e["t0"]) for e in episodes}
        for key in sorted(extra):
            problems.append(f"{rel}: episode {key[0]} {key[1]} has no onset "
                            "in the snapshot")
    else:
        problems.append(f"{rel}: header differs from its recomputation")


# Planetary Listening (V0 increment 1, 2026-10-14). The declared theatre lives
# here, not in a config (audit 2026-08-22, ethics 1 and 4): industrial sites
# in EU states, licence-filtered networks only, no citizen stations (AM).
PL_BASE = "planetary/probes"
PL_SNAP = "planetary/snapshots"     # nightly readings (V0 increment 2)
PL_STATIONS = {"GE.RUE", "GR.KAST"}
PL_NETWORKS = {"GE": "10.14470/TR560404", "GR": "10.25928/mbx6-hr74"}
PL_HOSTS = {"geofon.gfz.de", "eida.bgr.de", "www.isc.ac.uk",
            "earthquake.usgs.gov"}
PL_MAX_EXCERPTS = 4


def _pl_records(data: bytes) -> list[tuple[str, str, int]]:
    """(network, station, length) per miniSEED 2 record; raises ValueError."""
    out, offset = [], 0
    while offset < len(data):
        head = data[offset:offset + 48]
        if len(head) < 48 or head[6:7] not in (b"D", b"R", b"Q", b"M"):
            raise ValueError(f"no record at byte {offset}")
        order = ">" if 1900 <= int.from_bytes(head[20:22], "big") <= 2100 else "<"
        blk = int.from_bytes(head[46:48], "big" if order == ">" else "little")
        reclen = None
        for _ in range(16):
            if not blk:
                break
            at = offset + blk
            kind = int.from_bytes(data[at:at + 2], "big" if order == ">" else "little")
            if kind == 1000:
                reclen = 1 << data[at + 6]
            blk = int.from_bytes(data[at + 2:at + 4], "big" if order == ">" else "little")
        if not reclen:
            raise ValueError(f"no blockette 1000 at byte {offset}")
        out.append((head[18:20].decode("ascii").strip(),
                    head[8:13].decode("ascii").strip(), reclen))
        offset += reclen
    if offset != len(data):
        raise ValueError("trailing bytes are not record-aligned")
    return out


def check_planetary(root: Path, registry_files: dict, problems: list[str]) -> None:
    per_station_day: dict[tuple[str, str], int] = {}
    excerpts = [f for b in (PL_BASE, PL_SNAP) if (root / b).exists()
                for f in sorted((root / b).rglob("*.mseed"))]
    for f in excerpts:
        rel = f.relative_to(root).as_posix()
        try:
            recs = _pl_records(f.read_bytes())
        except ValueError as e:
            problems.append(f"{rel}: not record-aligned miniSEED ({e})")
            continue
        for net, sta, _len in recs:
            if net not in PL_NETWORKS or f"{net}.{sta}" not in PL_STATIONS:
                problems.append(f"{rel}: station {net}.{sta} outside the "
                                "declared theatre")
                break
        key = (f.parent.name, f.name[:8])
        per_station_day[key] = per_station_day.get(key, 0) + 1
    for (station, day), n in sorted(per_station_day.items()):
        if n > PL_MAX_EXCERPTS:
            problems.append(f"{PL_BASE}: {station} {day}: {n} excerpts, "
                            f"more than {PL_MAX_EXCERPTS}")
    for rpath in sorted(root.glob("planetary/spike/*.json")):
        rel = rpath.relative_to(root).as_posix()
        reading = load(rpath)
        if reading.get("schema") != "planetary-spike-v1":
            problems.append(f"{rel}: unknown schema")
            continue
        for req in reading.get("requests", []):
            host = req.get("url", "").split("/")[2] if "://" in req.get("url", "") else ""
            if host not in PL_HOSTS:
                problems.append(f"{rel}: request to {host or '?'} outside the "
                                "audited sources")
            if not re.fullmatch(r"[0-9a-f]{64}", str(req.get("sha256", ""))):
                problems.append(f"{rel}: request without a SHA-256")
        for pairing in ("pairing_a", "pairing_b"):
            for day in reading.get(pairing, {}).get("days", []):
                net, sta = day.get("station", "..").split(".")[:2]
                if f"{net}.{sta}" not in PL_STATIONS:
                    problems.append(f"{rel}: station {net}.{sta} outside the "
                                    "declared theatre")
                elif day.get("doi") != PL_NETWORKS[net]:
                    problems.append(f"{rel}: {net}.{sta} {day.get('day')}: "
                                    "network DOI missing or wrong")
                for ex in day.get("excerpts", []):
                    if ex.get("file") not in registry_files:
                        problems.append(f"{rel}: excerpt {ex.get('file')} "
                                        "not manifested")
    check_planetary_readings(root, registry_files, problems)


def _pl_table(data: bytes) -> list[dict]:
    lines = data.decode("utf-8", "replace").splitlines()
    if not lines or not lines[0].startswith("#"):
        return []
    keys = lines[0].lstrip("#").split()
    return [dict(zip(keys, c)) for c in (line.split() for line in lines[1:])
            if len(c) == len(keys)]


def _pl_reingestion(prev: list[dict], cur: list[dict]) -> list[dict]:
    """Independent recomputation of nightly.reingestion (same rule, kept here
    so the verifier does not trust the code it checks)."""
    key = lambda r: f"{r.get('Quality')}|{r.get('SampleRate')}|{r.get('Earliest')}"
    open_row = max(prev, key=lambda r: r.get("Latest", ""), default=None)
    now = {key(r): r for r in cur}
    out = []
    for r in prev:
        if open_row is not None and key(r) == key(open_row):
            continue
        c = now.get(key(r))
        if c is None:
            out.append(("segment_gone", key(r)))
        elif (c.get("Updated"), c.get("Latest")) != (r.get("Updated"), r.get("Latest")):
            out.append(("segment_rewritten", key(r)))
    known = {key(r) for r in prev}
    for r in cur:
        if key(r) not in known and open_row is not None \
                and r.get("Earliest", "") < open_row.get("Earliest", ""):
            out.append(("segment_inserted", key(r)))
    return out


def check_planetary_readings(root: Path, registry_files: dict,
                             problems: list[str]) -> None:
    """Nightly GE.RUE readings: one day behind their date, only audited
    hosts, every claim on a manifested file, re-ingestion events recomputed
    from the committed extent documents."""
    prev_rows, prev_rel = None, None
    for rpath in sorted(root.glob("planetary/readings/*.json")):
        rel = rpath.relative_to(root).as_posix()
        r = load(rpath)
        if r.get("schema") != "planetary-reading-v1":
            problems.append(f"{rel}: unknown schema")
            continue
        try:
            expected = (date.fromisoformat(rpath.stem) - timedelta(days=1)).isoformat()
        except ValueError:
            problems.append(f"{rel}: file name is not a date")
            continue
        if r.get("date") != rpath.stem or r.get("day") != expected:
            problems.append(f"{rel}: not a T+1 reading of {expected}")
        for req in r.get("requests", []):
            url = req.get("url", "")
            host = url.split("/")[2] if "://" in url else ""
            if host not in PL_HOSTS:
                problems.append(f"{rel}: request to {host or '?'} outside the "
                                "audited sources")
            if not re.fullmatch(r"[0-9a-f]{64}", str(req.get("sha256", ""))):
                problems.append(f"{rel}: request without a SHA-256")
        sd = r.get("station_day", {})
        net, sta = (sd.get("station", "..").split(".") + ["", ""])[:2]
        if f"{net}.{sta}" not in PL_STATIONS:
            problems.append(f"{rel}: station {net}.{sta} outside the declared theatre")
        elif sd.get("doi") != PL_NETWORKS[net]:
            problems.append(f"{rel}: {net}.{sta}: network DOI missing or wrong")
        if sd.get("day") != expected:
            problems.append(f"{rel}: station day is not {expected}")
        for ex in sd.get("excerpts", []):
            if ex.get("file") not in registry_files:
                problems.append(f"{rel}: excerpt {ex.get('file')} not manifested")
        pub = r.get("publisher", {})
        for name in ("availability", "extent", "wfcatalog"):
            f = (pub.get(name) or {}).get("file")
            if f is not None and f not in registry_files:
                problems.append(f"{rel}: publisher {name} {f} not manifested")
        ext = pub.get("extent") or {}
        rows = None
        if ext.get("file") in registry_files:
            rows = _pl_table((root / ext["file"]).read_bytes())
            if rows != ext.get("rows"):
                problems.append(f"{rel}: extent rows differ from the committed "
                                "publisher document")
        av = pub.get("availability") or {}
        if av.get("file") in registry_files and \
                _pl_table((root / av["file"]).read_bytes()) != av.get("rows"):
            problems.append(f"{rel}: availability rows differ from the "
                            "committed publisher document")
        re_ = r.get("reingestion", {})
        if rows is not None and prev_rows is not None:
            if re_.get("compared_with") != prev_rel:
                problems.append(f"{rel}: re-ingestion not compared with {prev_rel}")
            got = [(e.get("kind"), e.get("segment")) for e in re_.get("events", [])]
            if got != _pl_reingestion(prev_rows, rows):
                problems.append(f"{rel}: re-ingestion events differ from their "
                                "recomputation")
        elif re_.get("events"):
            problems.append(f"{rel}: re-ingestion events without a comparison")
        if rows is not None:
            prev_rows, prev_rel = rows, rel


SF_SNAP = "syntheticflood/snapshots"
SF_HOST = "eutils.ncbi.nlm.nih.gov"
SF_LISTS = ("fixed", "controls", "pool")
SF_ROW_KEYS = {"list", "word", "term", "url", "status", "bytes", "sha256",
               "count", "file", "error"}


def _sf_url(month: str, word: str | None) -> tuple[str, str]:
    """Independent rebuild of the deterministic esearch count query."""
    from urllib.parse import quote_plus
    if "-" in month:
        year, mm = month.split("-")
        term = f"hasabstract AND {year}/{mm}[dp]"
    else:
        term = f"hasabstract AND {month}[dp]"
    if word:
        term = f"{word}[tiab] AND {term}"
    return term, (f"https://{SF_HOST}/entrez/eutils/esearch.fcgi?db=pubmed"
                  f"&rettype=count&retmode=json&tool=machine-attention"
                  f"&term={quote_plus(term, safe='/[]')}")


def _sf_canonical(count: int) -> bytes:
    return ('{"header":{"type":"esearch","version":"0.3"},'
            '"esearchresult":{"count":"%d"}}\n' % count).encode()


def _sf_row(rel: str, row: dict, month: str, word: str | None,
            registry_files: dict, problems: list[str]) -> None:
    label = word or "cohort total"
    extra = set(row) - SF_ROW_KEYS
    if extra:
        problems.append(f"{rel}: {label}: fields outside counts-only {sorted(extra)}")
    term, url = _sf_url(month, word)
    if row.get("term") != term or row.get("url") != url:
        problems.append(f"{rel}: {label}: query is not the deterministic count query")
    count = row.get("count")
    if count is None:
        if row.get("status") == 200 and row.get("file") not in registry_files:
            problems.append(f"{rel}: {label}: 200 without a count and without bytes")
        return
    if not isinstance(count, int) or count < 0:
        problems.append(f"{rel}: {label}: count is not a non-negative integer")
        return
    if row.get("file") is not None:
        entry = registry_files.get(row["file"])
        if entry is None or entry.get("sha256") != row.get("sha256"):
            problems.append(f"{rel}: {label}: preserved answer not manifested")
    elif hashlib.sha256(_sf_canonical(count)).hexdigest() != row.get("sha256"):
        problems.append(f"{rel}: {label}: count does not match the SHA-256 of "
                        "the answer it claims")


def check_syntheticflood(root: Path, registry_files: dict,
                         problems: list[str]) -> None:
    """Register A cohort readings: counts only, every committed word asked,
    every query rebuilt, every count bound to the hash of its answer, the
    word list an immutable versioned file."""
    for wpath in sorted(root.glob("syntheticflood/wordlists/*.json")):
        rel = wpath.relative_to(root).as_posix()
        doc = load(wpath)
        seen: set[str] = set()
        for name in SF_LISTS:
            for w in doc.get(name) or []:
                if not (isinstance(w, str) and re.fullmatch(r"[a-z]+", w)) or w in seen:
                    problems.append(f"{rel}: {name}: {w!r} malformed or repeated")
                seen.add(w)
        if doc.get("version") != wpath.stem:
            problems.append(f"{rel}: version differs from its file name")
    for rpath in sorted(root.glob("syntheticflood/readings/*/*.json")):
        rel = rpath.relative_to(root).as_posix()
        r = load(rpath)
        if r.get("schema") != "syntheticflood-cohort-v1":
            problems.append(f"{rel}: unknown schema")
            continue
        month = rpath.parent.name
        if r.get("cohort") != month or r.get("date") != rpath.stem \
                or not re.fullmatch(r"\d{4}(-(0[1-9]|1[0-2]))?", month):
            problems.append(f"{rel}: cohort or date differs from its path")
            continue
        # A year cohort (baseline) ends in December.
        n = (int(rpath.stem[:4]) - int(month[:4])) * 12 + \
            int(rpath.stem[5:7]) - (int(month[5:7]) if "-" in month else 12)
        if n < 1 or r.get("lag_months") != n or r.get("value") != (n == 3) \
                or r.get("retrospective") != (n > 3):
            problems.append(f"{rel}: lag, value or retrospective mark is wrong")
        if r.get("source") != SF_HOST:
            problems.append(f"{rel}: source outside the audited host")
        wl = r.get("wordlist") or {}
        wfile = root / str(wl.get("file", ""))
        if not wfile.is_file() or sha256_file(wfile) != wl.get("sha256"):
            problems.append(f"{rel}: word list {wl.get('file')} missing or changed")
            continue
        doc = load(wfile)
        want = [(name, w) for name in SF_LISTS for w in doc.get(name) or []]
        got = [(c.get("list"), c.get("word")) for c in r.get("counts", [])]
        if got != want:
            problems.append(f"{rel}: counts do not cover the word list in order")
        _sf_row(rel, r.get("total") or {}, month, None, registry_files, problems)
        for c in r.get("counts", []):
            _sf_row(rel, c, month, c.get("word"), registry_files, problems)


SF_BASE_YEARS = ("2018", "2019", "2020", "2021", "2022")
SF_BASE_RULES = {"baseline-v1": {"years": list(SF_BASE_YEARS), "min_count": 50,
                                 "max_ratio": 1.5}}


def check_syntheticflood_baseline(root: Path, problems: list[str]) -> None:
    """The stability test of a word list: every number re-derived from the
    committed year readings it names, under a rule that never changes."""
    for bpath in sorted(root.glob("syntheticflood/baseline/*.json")):
        rel = bpath.relative_to(root).as_posix()
        b = load(bpath)
        rule = b.get("rule") or {}
        params = SF_BASE_RULES.get(rule.get("id"))
        if b.get("schema") != "syntheticflood-baseline-v1" or params is None \
                or {k: v for k, v in rule.items() if k != "id"} != params:
            problems.append(f"{rel}: unknown schema or rule changed under its id")
            continue
        wl = b.get("wordlist") or {}
        wfile = root / str(wl.get("file", ""))
        if wl.get("version") != bpath.stem or not wfile.is_file() \
                or sha256_file(wfile) != wl.get("sha256"):
            problems.append(f"{rel}: word list missing, changed or not its name")
            continue
        doc = load(wfile)
        reads, totals = {}, {}
        for y in SF_BASE_YEARS:
            ref = (b.get("readings") or {}).get(y) or {}
            f = str(ref.get("file", ""))
            rp = root / f
            newest = sorted(p for p in (root / "syntheticflood/readings" / y).glob("*.json")
                            if load(p).get("wordlist", {}).get("version") == bpath.stem)
            if not f.startswith(f"syntheticflood/readings/{y}/") or not rp.is_file() \
                    or sha256_file(rp) != ref.get("sha256") or not newest or newest[-1] != rp:
                problems.append(f"{rel}: {y}: not the newest committed year reading")
                break
            reads[y] = load(rp)
            totals[y] = reads[y].get("total", {}).get("count")
        else:
            want_terms = [(n, w) for n in SF_LISTS for w in doc.get(n) or []]
            if b.get("totals") != totals or [(w.get("list"), w.get("word"))
                                             for w in b.get("words", [])] != want_terms:
                problems.append(f"{rel}: totals or words differ from the readings")
                continue
            for i, w in enumerate(b["words"]):
                counts = {y: reads[y]["counts"][i]["count"] for y in SF_BASE_YEARS}
                shares = {y: round(counts[y] / totals[y], 9) for y in SF_BASE_YEARS}
                low, high = min(shares.values()), max(shares.values())
                ratio = round(high / low, 4) if low > 0 else None
                if min(counts.values()) < params["min_count"]:
                    v = "rare"
                elif ratio <= params["max_ratio"]:
                    v = "stable"
                else:
                    up = shares[SF_BASE_YEARS[-1]] > shares[SF_BASE_YEARS[0]]
                    v = "drifting-rising" if up else "drifting-falling"
                if (w.get("counts"), w.get("shares"), w.get("ratio"), w.get("verdict"),
                        w.get("min_count")) != (counts, shares, ratio, v, min(counts.values())):
                    problems.append(f"{rel}: {w.get('word')}: differs from the readings")
            tally: dict = {}
            for w in b["words"]:
                tally.setdefault(w["list"], {}).setdefault(w["verdict"], 0)
                tally[w["list"]][w["verdict"]] += 1
            if b.get("tally") != tally:
                problems.append(f"{rel}: tally differs from the words")


SF_EXCESS_RULES = {"excess-v1": {"min_ratio": 2.0, "min_count": 50, "max_words": 20,
                                 "control_band": 1.5}}


def _sf_expected(shares: dict, cohort: str) -> float:
    """The baseline's least-squares line at the cohort's position, rebuilt
    here independently of practice.syntheticflood.excess."""
    if "-" in cohort:
        y, m = cohort.split("-")
        pos = int(y) + (int(m) - 0.5) / 12 - 0.5
    else:
        pos = float(int(cohort))
    xs = [float(y) for y in shares]
    ys = list(shares.values())
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    slope = sum((x - mx) * (v - my) for x, v in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return (my - slope * mx) + slope * pos


def check_syntheticflood_derived(root: Path, problems: list[str]) -> None:
    """A derived list: every ratio re-derived from the cohort reading and the
    baseline it names by hash, under a rule that never changes."""
    for dpath in sorted(root.glob("syntheticflood/derived/*/*.json")):
        rel = dpath.relative_to(root).as_posix()
        d = load(dpath)
        rule = d.get("rule") or {}
        params = SF_EXCESS_RULES.get(rule.get("id"))
        if d.get("schema") != "syntheticflood-derived-v1" or params is None \
                or {k: v for k, v in rule.items() if k != "id"} != params:
            problems.append(f"{rel}: unknown schema or rule changed under its id")
            continue
        cohort = dpath.parent.name
        if d.get("cohort") != cohort or d.get("date") != dpath.stem \
                or cohort in SF_BASE_YEARS:
            problems.append(f"{rel}: cohort or date is not its path")
            continue
        refs = {}
        for key, want in (("reading", f"syntheticflood/readings/{cohort}/{dpath.stem}.json"),
                          ("baseline", None)):
            ref = d.get(key) or {}
            f = str(ref.get("file", ""))
            if (want and f != want) or not (root / f).is_file() \
                    or sha256_file(root / f) != ref.get("sha256"):
                problems.append(f"{rel}: {key} missing, changed or not the one named")
                break
            refs[key] = load(root / f)
        else:
            r, b = refs["reading"], refs["baseline"]
            if b.get("schema") != "syntheticflood-baseline-v1" \
                    or r.get("wordlist") != b.get("wordlist") \
                    or d.get("wordlist") != b.get("wordlist"):
                problems.append(f"{rel}: reading and baseline on different word lists")
                continue
            total = (r.get("total") or {}).get("count")
            counts = r.get("counts") or []
            if [(c.get("list"), c.get("word")) for c in counts] != \
                    [(w.get("list"), w.get("word")) for w in b.get("words", [])] \
                    or total is None or any(c.get("count") is None for c in counts) \
                    or d.get("total") != total or d.get("value") != r.get("value") \
                    or d.get("lag_months") != r.get("lag_months"):
                problems.append(f"{rel}: reading incomplete or not the baseline's words")
                continue
            rows = []
            for c, w in zip(counts, b["words"]):
                row = {"list": w["list"], "word": w["word"], "count": c["count"]}
                exp = _sf_expected(w["shares"], cohort) if w["verdict"] != "rare" else None
                if exp is None:
                    row["status"] = "rare"
                elif exp <= 0:
                    row["status"] = "no_trend"
                else:
                    obs = c["count"] / total
                    row.update(status="measured", expected=round(exp, 9),
                               observed=round(obs, 9), ratio=round(obs / exp, 4))
                rows.append(row)
            band = params["control_band"]
            breach = [x["word"] for x in rows if x["list"] == "controls"
                      and x["status"] == "measured"
                      and not 1 / band <= x["ratio"] <= band]
            pool = sorted((x for x in rows if x["list"] == "pool"
                           and x["status"] == "measured"
                           and x["ratio"] >= params["min_ratio"]
                           and x["count"] >= params["min_count"]),
                          key=lambda x: (-x["ratio"], x["word"]))
            if d.get("words") != rows:
                problems.append(f"{rel}: words differ from the reading and baseline")
            if d.get("control_breach") != breach \
                    or d.get("derived") != [x["word"] for x in pool[:params["max_words"]]]:
                problems.append(f"{rel}: derived list or control breach differs")


SF_WIKI_URL = ("https://en.wikipedia.org/w/api.php?format=json&formatversion=2"
               "&action=query&list=allcategories"
               "&acprefix=Articles+containing+suspected+AI&acprop=size&aclimit=500")
SF_WIKI_FAMILIES = {
    "Articles containing suspected AI-generated texts": "texts",
    "Articles containing suspected AI-generated sources": "sources"}
SF_WIKI_KEYS = {"schema", "date", "source", "url", "user_agent", "started_at",
                "finished_at", "requests", "http_429", "status", "file",
                "sha256", "error", "complete", "families", "unmatched"}
SF_MONTHS = ("January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December")


def _sf_wiki_derive(data: bytes) -> dict:
    """Independent derivation of a Register B reading from its bytes."""
    doc = json.loads(data)
    fams = {k: {"container": None, "months": {}} for k in SF_WIKI_FAMILIES.values()}
    unmatched = []
    for row in doc["query"]["allcategories"]:
        name, size = row["category"], int(row["size"])
        if name in SF_WIKI_FAMILIES:
            fams[SF_WIKI_FAMILIES[name]]["container"] = {
                "size": size, "pages": int(row["pages"]), "subcats": int(row["subcats"])}
            continue
        head, sep, tail = name.rpartition(" from ")
        parts = tail.split(" ")
        if sep and head in SF_WIKI_FAMILIES and len(parts) == 2 \
                and parts[0] in SF_MONTHS and re.fullmatch(r"\d{4}", parts[1]):
            key = f"{parts[1]}-{SF_MONTHS.index(parts[0]) + 1:02d}"
            fams[SF_WIKI_FAMILIES[head]]["months"][key] = size
        else:
            unmatched.append({"category": name, "size": size})
    for f in fams.values():
        f["months"] = dict(sorted(f["months"].items()))
    return {"complete": "continue" not in doc, "families": fams,
            "unmatched": unmatched}


def check_syntheticflood_categories(root: Path, registry_files: dict,
                                    problems: list[str]) -> None:
    """Register B readings: one fixed request, the answer preserved, every
    number re-derived from the preserved bytes, nothing but category names
    and sizes."""
    for rpath in sorted(root.glob("syntheticflood/categories/*.json")):
        rel = rpath.relative_to(root).as_posix()
        r = load(rpath)
        if r.get("schema") != "syntheticflood-categories-v1":
            problems.append(f"{rel}: unknown schema")
            continue
        if r.get("date") != rpath.stem:
            problems.append(f"{rel}: date differs from its path")
        extra = set(r) - SF_WIKI_KEYS
        if extra:
            problems.append(f"{rel}: fields outside category sizes {sorted(extra)}")
        if r.get("url") != SF_WIKI_URL or r.get("source") != "en.wikipedia.org":
            problems.append(f"{rel}: not the audited allcategories request")
        if r.get("file") is None:
            if "families" in r or not r.get("error"):
                problems.append(f"{rel}: sizes without preserved bytes")
            continue
        entry = registry_files.get(r["file"])
        if entry is None or entry.get("sha256") != r.get("sha256") \
                or not r["file"].startswith(f"{SF_SNAP}/{rpath.stem}-"):
            problems.append(f"{rel}: answer not manifested under its own date")
            continue
        if "families" not in r:
            if not r.get("error"):
                problems.append(f"{rel}: neither sizes nor an error")
            continue
        try:
            want = _sf_wiki_derive((root / r["file"]).read_bytes())
        except (ValueError, KeyError, TypeError):
            problems.append(f"{rel}: preserved answer does not parse")
            continue
        for key in ("complete", "families", "unmatched"):
            if r.get(key) != want[key]:
                problems.append(f"{rel}: {key} differs from the preserved answer")


def check(root: Path) -> list[str]:
    problems: list[str] = []
    registry_files: dict[str, dict] = {}

    check_snapshots(root, "foreknown/snapshots", problems, registry_files, True)
    check_snapshots(root, "foreknown/reaction/snapshots", problems,
                    registry_files, False)
    check_snapshots(root, "darkocean/snapshots", problems, registry_files,
                    False)
    check_snapshots(root, "memoryhole/snapshots", problems, registry_files,
                    False)
    check_snapshots(root, IV_BASE, problems, registry_files, False)
    check_snapshots(root, PL_BASE, problems, registry_files, False)
    check_snapshots(root, PL_SNAP, problems, registry_files, False)
    check_snapshots(root, SF_SNAP, problems, registry_files, False)

    check_retired(root, problems)

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
        # A resolution is a claim about the moment it was written
        # (resolved_at), not a claim that binds the future forever: futures.py
        # already models a closed future reappearing in its own feed later
        # (REAPPEARED, status flips back to OPEN) as a legitimate difference,
        # not an error. So the hole this check watches for is a resolution
        # with no matching closure in history at all — not a future that was
        # genuinely closed at resolved_at and only later came back.
        # "Closed at resolved_at" means the last history event at or before
        # resolved_at is a closure. futures.py and resolve.py each call
        # utc_now() separately, so the closure's ts and resolved_at can differ
        # by a second (50 of 352 committed resolutions do); demanding string
        # equality broke the notary run the first time one of those reappeared.
        closed_at_resolution = _closed_at(future.get("history", []),
                                          resolution.get("resolved_at"))
        if future.get("status") == "OPEN" and not closed_at_resolution:
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
    check_foreknown_reaction_series(root, problems)
    check_darkocean(root, registry_files, problems)
    check_darkocean_continuity(root, registry_files, problems)
    check_memoryhole(root, registry_files, problems)
    check_memoryhole_verdicts(root, problems)
    check_interval(root, problems)
    check_interval_readings(root, problems)
    check_interval_experiment(root, problems)
    check_planetary(root, registry_files, problems)
    check_planetary_experiment(root, problems)
    check_syntheticflood(root, registry_files, problems)
    check_syntheticflood_categories(root, registry_files, problems)
    check_syntheticflood_baseline(root, problems)
    check_syntheticflood_derived(root, problems)
    check_anchors(root, problems)

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
