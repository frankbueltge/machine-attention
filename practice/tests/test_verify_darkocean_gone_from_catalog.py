"""verify.py's darkocean-continuity check, proven to recompute gone_from_catalog too.

Before this test, check_darkocean_continuity's own docstring promised a
record "cannot claim a divergence the bytes do not show — nor quietly drop
one they do", but its recomputation only ever covered catches of kind
"changed": a product the catalog's look-back simply never answered for was
never independently reconstructed, and a record could have invented or
dropped a gone_from_catalog catch with nothing to catch it. This first
fired for real on 2026-09-03 (darkocean/continuity/2026-09-03.json,
foreknown/proposals/obs-2026-09-05-1.json) with no check on it at all.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def load_verify():
    spec = importlib.util.spec_from_file_location("verifymod", REPO / "verify.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verifymod"] = mod
    spec.loader.exec_module(mod)
    return mod


verify = load_verify()

FOOTPRINT = {"type": "Polygon", "coordinates": [[
    [19.0, 57.0], [20.0, 57.0], [20.0, 58.0], [19.0, 58.0], [19.0, 57.0]]]}

CDSE_PAGE = {"value": [
    {"Name": "S1C_IW_GRDH_1SDV_20260807T041000_20260807T041025_X_COG",
     "Id": "bbb", "ContentLength": 1_220_000_000,
     "ContentDate": {"Start": "2026-08-07T04:10:00.000Z",
                     "End": "2026-08-07T04:10:25.000Z"},
     "Checksum": [{"Algorithm": "BLAKE3", "Value": "b2"}],
     "Online": True, "EvictionDate": "9999-12-31T23:59:59.999999Z",
     "GeoFootprint": FOOTPRINT},
    {"Name": "S1D_IW_GRDH_1SDV_20260807T165300_20260807T165325_Y",
     "Id": "ccc", "ContentLength": 1_110_000_000,
     "ContentDate": {"Start": "2026-08-07T16:53:00.000Z",
                     "End": "2026-08-07T16:53:25.000Z"},
     "Checksum": [{"Algorithm": "BLAKE3", "Value": "b3"}],
     "GeoFootprint": {"type": "Polygon", "coordinates": [[
         [24.0, 59.0], [25.0, 59.0], [25.0, 59.5], [24.0, 59.5],
         [24.0, 59.0]]]}},
]}

DIGITRAFFIC = {"type": "FeatureCollection", "features": []}


class FakeClient:
    requests = 0
    http_429 = 0

    def fetch(self, url, headers=None):
        self.requests += 1
        from practice.darkocean import sources
        if url.startswith(sources.CDSE_BASE):
            return json.dumps(CDSE_PAGE).encode(), 200
        if url == sources.DIGITRAFFIC_URL:
            return json.dumps(DIGITRAFFIC).encode(), 200
        return b"", 404


class FakeLookbackClient:
    """The catalog's look-back answer with "ccc" gone from the response."""
    requests = 0
    http_429 = 0

    def fetch(self, url, headers=None):
        self.requests += 1
        moved = [dict(p) for p in CDSE_PAGE["value"] if p["Id"] != "ccc"]
        return json.dumps({"value": moved}).encode(), 200


def _dma_outage():
    from practice.darkocean import sources
    return {"url": sources.DMA_URL, "state": "outage: URLError",
            "note": sources.DMA_NOTE}


def _seed(tmp_path):
    from practice.darkocean.continuity import run as continuity_run
    from practice.darkocean.run import run as reading_run

    reading_run(tmp_path, "2026-08-07", FakeClient(), dma_probe=_dma_outage)
    return continuity_run(tmp_path, "2026-08-08", FakeLookbackClient())


def _verify_problems(tmp_path):
    problems: list[str] = []
    registry_files: dict[str, dict] = {}
    verify.check_snapshots(tmp_path, "darkocean/snapshots", problems,
                           registry_files, False)
    verify.check_darkocean_continuity(tmp_path, registry_files, problems)
    return problems


def test_a_genuine_gone_from_catalog_catch_passes(tmp_path):
    record = _seed(tmp_path)
    assert {c["id"] for c in record["catches"] if c["kind"] == "gone_from_catalog"} == {"ccc"}

    problems = _verify_problems(tmp_path)
    assert problems == []


def test_a_dropped_gone_from_catalog_catch_is_caught(tmp_path):
    """A record that quietly omits a catch the bytes prove is due."""
    _seed(tmp_path)
    record_path = tmp_path / "darkocean/continuity/2026-08-08.json"
    record = json.loads(record_path.read_text())
    record["catches"] = [c for c in record["catches"]
                         if c["kind"] != "gone_from_catalog"]
    record_path.write_text(json.dumps(record))

    problems = _verify_problems(tmp_path)
    assert any("catalog-absences do not match" in p for p in problems)


def test_an_invented_gone_from_catalog_catch_is_caught(tmp_path):
    """A record claiming a product vanished when the look-back answered it."""
    _seed(tmp_path)
    record_path = tmp_path / "darkocean/continuity/2026-08-08.json"
    record = json.loads(record_path.read_text())
    record["catches"].append({"kind": "gone_from_catalog", "id": "bbb",
                              "name": "invented", "first_seen": "2026-08-07",
                              "preserved": {}, "current": None})
    record_path.write_text(json.dumps(record))

    problems = _verify_problems(tmp_path)
    assert any("catalog-absences do not match" in p for p in problems)


def test_a_reconciled_gone_from_catalog_preserved_value_is_caught(tmp_path):
    """group N forbids reporting a preserved value the register never held."""
    _seed(tmp_path)
    record_path = tmp_path / "darkocean/continuity/2026-08-08.json"
    record = json.loads(record_path.read_text())
    for catch in record["catches"]:
        if catch["kind"] == "gone_from_catalog":
            catch["preserved"] = {"online": False}
    record_path.write_text(json.dumps(record))

    problems = _verify_problems(tmp_path)
    assert any("reconciliation, which group N forbids" in p for p in problems)


def test_a_failed_batch_excuses_the_absence_it_caused(tmp_path):
    """The one historical case (darkocean/continuity/2026-08-25.json,
    batch 8 HTTP 400) must not be flagged: an unanswered batch is a
    failure, never evidence of a vanished product."""
    _seed(tmp_path)
    record_path = tmp_path / "darkocean/continuity/2026-08-08.json"
    record = json.loads(record_path.read_text())
    record["catches"] = [c for c in record["catches"]
                         if c["kind"] != "gone_from_catalog"]
    record["failures"] = [{"scope": "darkocean:CDSE-lookback",
                           "error": "HTTP 400", "batch": 1}]
    record_path.write_text(json.dumps(record))

    problems = _verify_problems(tmp_path)
    assert not any("catalog-absences do not match" in p for p in problems)
