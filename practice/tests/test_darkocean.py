"""Dark Ocean V0 — Coverage vs Declaration.

The V0 notarizes the act of looking (catalog rows, issuer checksums)
against the act of declaring (one agency AIS sample). These tests hold it
to the audit's conditions: keyless, counts only, outages recorded."""

import json

from practice.darkocean import region, sources
from practice.darkocean.run import run

# A footprint covering roughly one degree square in the central Baltic:
# cell centers at 19.25/19.75 x 57.25/57.75 lie inside.
FOOTPRINT = {"type": "Polygon", "coordinates": [[
    [19.0, 57.0], [20.0, 57.0], [20.0, 58.0], [19.0, 58.0], [19.0, 57.0]]]}

CDSE_PAGE = {"value": [
    {"Name": "S1C_IW_GRDH_1SDV_20260807T041000_20260807T041025_X_SAFE",
     "Id": "aaa", "ContentLength": 1_780_000_000,
     "ContentDate": {"Start": "2026-08-07T04:10:00.000Z",
                     "End": "2026-08-07T04:10:25.000Z"},
     "Checksum": [{"Algorithm": "MD5", "Value": "m1"},
                  {"Algorithm": "BLAKE3", "Value": "b1"}],
     "Online": True, "EvictionDate": "2026-09-07T00:00:00.000Z",
     "GeoFootprint": FOOTPRINT},
    # same acquisition, second catalog format (the SAFE/COG pair seen live)
    {"Name": "S1C_IW_GRDH_1SDV_20260807T041000_20260807T041025_X_COG",
     "Id": "bbb", "ContentLength": 1_220_000_000,
     "ContentDate": {"Start": "2026-08-07T04:10:00.000Z",
                     "End": "2026-08-07T04:10:25.000Z"},
     "Checksum": [{"Algorithm": "BLAKE3", "Value": "b2"}],
     # what the live catalog answers today: online, no eviction date named
     "Online": True, "EvictionDate": "9999-12-31T23:59:59.999999Z",
     "GeoFootprint": FOOTPRINT},
    # a different acquisition, farther north
    {"Name": "S1D_IW_GRDH_1SDV_20260807T165300_20260807T165325_Y",
     "Id": "ccc", "ContentLength": 1_110_000_000,
     "ContentDate": {"Start": "2026-08-07T16:53:00.000Z",
                     "End": "2026-08-07T16:53:25.000Z"},
     "Checksum": [{"Algorithm": "BLAKE3", "Value": "b3"}],
     "GeoFootprint": {"type": "Polygon", "coordinates": [[
         [24.0, 59.0], [25.0, 59.0], [25.0, 59.5], [24.0, 59.5],
         [24.0, 59.0]]]}},
    # not GRD -> ignored
    {"Name": "S1C_IW_SLC__1SDV_20260807T041000_x", "Id": "ddd",
     "ContentDate": {"Start": "2026-08-07T04:10:00.000Z", "End": ""},
     "GeoFootprint": FOOTPRINT},
]}

DIGITRAFFIC = {"type": "FeatureCollection", "features": [
    {"geometry": {"type": "Point", "coordinates": [19.3, 57.3]},
     "properties": {"mmsi": 230111222, "sog": 9.9}},
    {"geometry": {"type": "Point", "coordinates": [19.4, 57.4]},
     "properties": {"mmsi": 230333444}},
    {"geometry": {"type": "Point", "coordinates": [24.9, 60.1]},
     "properties": {"mmsi": 230555666}},
    # outside the region -> counted in feed, not in region
    {"geometry": {"type": "Point", "coordinates": [4.0, 52.0]},
     "properties": {"mmsi": 244777888}},
]}


def test_grid_bins_and_point_in_polygon():
    assert region.cell_id(19.3, 57.3) == "E19.0_N57.0"
    assert region.cell_id(8.9, 57.3) is None          # west of the box
    assert region.covered_cells(FOOTPRINT) == \
        ["E19.0_N57.0", "E19.5_N57.0", "E19.0_N57.5", "E19.5_N57.5"]
    assert region.covered_cells(None) == []


def test_catalog_extraction_keeps_issuer_checksums_and_dedupes_visibly():
    scenes = sources.cdse_scenes([CDSE_PAGE])
    assert len(scenes) == 3                            # SLC dropped
    safe = next(s for s in scenes if s["name"].endswith("_SAFE"))
    assert safe["checksums"] == {"md5": "m1", "blake3": "b1"}
    assert safe["eviction_date"] == "2026-09-07T00:00:00.000Z"

    acquisitions = sources.acquisitions(scenes)
    assert len(acquisitions) == 2                      # SAFE/COG pair folded
    assert acquisitions[0]["cells"] == region.covered_cells(FOOTPRINT)


def test_declared_sample_is_counts_only():
    sample = sources.declared_sample(DIGITRAFFIC)
    assert sample == {"cells": {"E19.0_N57.0": 2, "E24.5_N60.0": 1},
                      "vessels_in_feed": 4, "vessels_in_region": 3}
    assert "mmsi" not in json.dumps(sample)


class FakeClient:
    requests = 0
    http_429 = 0

    def __init__(self, digitraffic_status=200):
        self._digitraffic_status = digitraffic_status

    def fetch(self, url, headers=None):
        self.requests += 1
        if url.startswith(sources.CDSE_BASE):
            return json.dumps(CDSE_PAGE).encode(), 200
        if url == sources.DIGITRAFFIC_URL:
            assert headers == {"Accept-Encoding": "gzip"}
            return json.dumps(DIGITRAFFIC).encode(), self._digitraffic_status
        return b"", 404


def _dma_outage():
    return {"url": sources.DMA_URL, "state": "outage: URLError",
            "note": sources.DMA_NOTE}


def test_reading_end_to_end_counts_both_axes_and_records_the_outage(tmp_path):
    summary = run(tmp_path, "2026-08-07", FakeClient(),
                  dma_probe=_dma_outage)
    assert summary["catalog_products"] == 3
    assert summary["acquisitions"] == 2
    assert summary["declared_in_region"] == 3

    reading = json.loads(
        (tmp_path / "darkocean/readings/2026-08-07.json").read_text())
    assert reading["cells"]["E19.0_N57.0"] == \
        {"observed_passes": 1, "declared_sample": 2}
    assert reading["coverage"]["cells_observed_silent_in_sample"] == 5
    assert reading["coverage"]["cells_declared_unobserved_today"] == 1
    assert reading["moment_axis"]["dma_probe"]["state"].startswith("outage")
    assert "never backfilled" in " ".join(reading["notes"])
    # ethics as a property of the artifact, not a promise
    assert "mmsi" not in json.dumps(reading).lower()
    # provenance: both sources preserved and manifested
    manifest = json.loads(
        (tmp_path / "darkocean/snapshots/2026-08-07/manifest.json").read_text())
    assert len(manifest["entries"]) == 2

    log_lines = (tmp_path / "autonomy/log.jsonl").read_text().splitlines()
    assert json.loads(log_lines[-1])["step"] == "darkocean-run"


def test_reading_refuses_to_overwrite_and_records_source_failures(tmp_path):
    run(tmp_path, "2026-08-07", FakeClient(), dma_probe=_dma_outage)
    try:
        run(tmp_path, "2026-08-07", FakeClient(), dma_probe=_dma_outage)
    except SystemExit as err:
        assert "append-only" in str(err)
    else:
        raise AssertionError("a second reading for the same day must be refused")

    summary = run(tmp_path, "2026-08-08", FakeClient(digitraffic_status=503),
                  dma_probe=_dma_outage)
    assert summary["declared_in_region"] is None
    assert any(f["scope"] == "darkocean:Digitraffic"
               for f in summary["failures"])
    reading = json.loads(
        (tmp_path / "darkocean/readings/2026-08-08.json").read_text())
    assert reading["declared_axis"] is None            # absent, not invented


# --- criteria group N: the continuity probe -----------------------------

class FakeLookbackClient:
    """Answers the look-back with a catalog that has moved on: the product
    the register recorded for the folded SAFE/COG pair has gone offline, has
    gained a real eviction date and no longer carries the BLAKE3 that was
    preserved — and the northern acquisition is gone from the catalog."""

    requests = 0
    http_429 = 0

    def __init__(self, status=200, drop_ids=("ccc",)):
        self._status = status
        self._drop = set(drop_ids)

    def fetch(self, url, headers=None):
        self.requests += 1
        if self._status != 200:
            return b"", self._status
        moved = []
        for product in CDSE_PAGE["value"]:
            pid = product.get("Id")
            if "GRD" not in product.get("Name", "") or pid in self._drop:
                continue
            answer = dict(product)
            answer["ModificationDate"] = "2026-08-09T00:00:00.000Z"
            # "bbb" is the product the dedupe keeps for that acquisition —
            # the register holds it, so it is the one worth moving.
            if pid == "bbb":
                answer["Online"] = False
                answer["EvictionDate"] = "2026-08-20T00:00:00.000Z"
                answer["Checksum"] = [{"Algorithm": "BLAKE3",
                                       "Value": "b2-DIFFERENT"}]
            moved.append(answer)
        return json.dumps({"value": moved}).encode(), 200


def _seed_reading(tmp_path):
    run(tmp_path, "2026-08-07", FakeClient(), dma_probe=_dma_outage)


def test_continuity_catches_divergence_and_never_reconciles_it(tmp_path):
    from practice.darkocean.continuity import run as continuity_run

    _seed_reading(tmp_path)
    record = continuity_run(tmp_path, "2026-08-08", FakeLookbackClient())

    kinds = {(c["kind"], c.get("field")) for c in record["catches"]}
    assert ("changed", "online") in kinds
    assert ("changed", "eviction_date") in kinds
    assert ("changed", "checksums") in kinds
    assert ("gone_from_catalog", None) in kinds

    checksum_catch = next(c for c in record["catches"]
                          if c.get("field") == "checksums")
    assert checksum_catch["preserved"] == {"blake3": "b2"}
    assert checksum_catch["current"] == {"blake3": "b2-DIFFERENT"}

    # the reading it came from is untouched: nothing is reconciled
    reading = json.loads(
        (tmp_path / "darkocean/readings/2026-08-07.json").read_text())
    preserved = {a["id"]: a for a in reading["acquisitions"]}
    assert preserved["bbb"]["online"] is True
    assert preserved["bbb"]["eviction_date"] == "9999-12-31T23:59:59.999999Z"

    log_lines = (tmp_path / "autonomy/log.jsonl").read_text().splitlines()
    assert json.loads(log_lines[-1])["step"] == "darkocean-continuity"


def test_continuity_establishes_a_missing_baseline_instead_of_claiming_unchanged(
        tmp_path):
    """Readings written before 2026-08-09 carry no modification_date. The
    probe may not report 'unchanged' for a value it never held."""
    from practice.darkocean.continuity import run as continuity_run

    _seed_reading(tmp_path)
    reading_path = tmp_path / "darkocean/readings/2026-08-07.json"
    reading = json.loads(reading_path.read_text())
    for acquisition in reading["acquisitions"]:
        acquisition.pop("modification_date", None)
    reading_path.write_text(json.dumps(reading))

    record = continuity_run(tmp_path, "2026-08-08",
                            FakeLookbackClient(drop_ids=()))
    established = {(b["id"], b["field"]) for b in record["baselines_established"]}
    assert ("bbb", "modification_date") in established
    assert not any(c.get("field") == "modification_date"
                   for c in record["catches"])

    # a later night compares against the baseline the first probe established
    later = continuity_run(tmp_path, "2026-08-09",
                           FakeLookbackClient(drop_ids=()))
    assert not later["baselines_established"]


def test_continuity_treats_a_failed_batch_as_a_failure_not_a_vanished_product(
        tmp_path):
    from practice.darkocean.continuity import run as continuity_run

    _seed_reading(tmp_path)
    record = continuity_run(tmp_path, "2026-08-08",
                            FakeLookbackClient(status=503))
    assert record["catches"] == []                     # nothing is claimed
    assert record["failures"][0]["error"] == "HTTP 503"
    assert record["answered"] == 0
