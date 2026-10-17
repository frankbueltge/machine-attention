"""Planetary Listening nightly T+1 reading: storage model, publisher documents,
re-ingestion as a compared event. A fake client serves committed bytes. No network."""

import json
from pathlib import Path

from practice.planetary import mseed, nightly

ROOT = Path(__file__).resolve().parents[2]
EXCERPT = ROOT / "planetary/probes/2026-10-14/GE.RUE.HHZ/20261008T073232.mseed"
SNAP = ROOT / "planetary/snapshots/2026-10-15/GE.RUE.HHZ"


class FakeClient:
    def __init__(self, extent: bytes):
        self.extent = extent
        self.calls = []

    def fetch(self, url, headers=None):
        self.calls.append(url)
        if "dataselect" in url:
            return EXCERPT.read_bytes(), 200
        if "availability/1/query" in url:
            return (SNAP / "availability-2026-10-14.txt").read_bytes(), 200
        if "availability/1/extent" in url:
            return self.extent, 200
        if "wfcatalog" in url:
            return (SNAP / "wfcatalog-2026-10-14.json").read_bytes(), 200
        if "isc.ac.uk" in url:
            return b"", 204
        return b'{"type":"FeatureCollection","features":[]}', 200


def rewrite_closed_segment(extent: bytes) -> bytes:
    return extent.replace(b"2022-07-28T05:00:57Z", b"2026-10-16T03:00:00Z")


def test_reading_is_t_plus_one_with_publisher_documents(tmp_path):
    extent = (SNAP / "extent.txt").read_bytes()
    r = nightly.run(tmp_path, client=FakeClient(extent), today="2026-10-15")
    assert r["schema"] == "planetary-reading-v1" and r["day"] == "2026-10-14"
    assert r["station_day"]["doi"] == "10.14470/TR560404"
    assert r["reingestion"] == {"compared_with": None, "events": [], "baseline": True}
    pub = r["publisher"]
    assert pub["availability"]["rows"][0]["Updated"] == "2026-10-15T05:14:43Z"
    assert len(pub["extent"]["rows"]) == 5
    assert pub["wfcatalog"]["day"]["num_records"] == 22048
    manifest = json.loads((tmp_path / nightly.BASE / "2026-10-15/manifest.json").read_text())
    for entry in manifest["entries"]:
        data = (tmp_path / entry["file"]).read_bytes()
        if entry["file"].endswith(".mseed"):
            assert data in EXCERPT.read_bytes() and mseed.records(data)
    day_file = r["requests"][0]
    assert "dataselect" in day_file["url"] and day_file["committed"] is False
    assert "index" not in json.dumps(r).lower()   # no loudness index (audit cond. 5)


def test_rewritten_closed_segment_is_an_event_the_open_one_is_not(tmp_path):
    extent = (SNAP / "extent.txt").read_bytes()
    nightly.run(tmp_path, client=FakeClient(extent), today="2026-10-15")
    # the open segment moves every night by appending: not an event
    grown = extent.replace(b"2026-10-15T05:14:43Z", b"2026-10-16T05:10:00Z") \
                  .replace(b"2026-10-15T00:00:00.000000Z", b"2026-10-16T00:00:00.000000Z")
    r = nightly.run(tmp_path, client=FakeClient(grown), today="2026-10-16")
    assert r["reingestion"]["compared_with"] == "planetary/readings/2026-10-15.json"
    assert r["reingestion"]["events"] == []
    r = nightly.run(tmp_path, client=FakeClient(rewrite_closed_segment(grown)),
                    today="2026-10-17")
    (event,) = r["reingestion"]["events"]
    assert event["kind"] == "segment_rewritten"
    assert event["updated_before"] == "2022-07-28T05:00:57Z"


def test_a_second_run_on_the_same_date_leaves_the_stamped_night_alone(tmp_path):
    # The first scheduled run (2026-10-16) re-fetched a night the practice's own session had
    # already read and committed that morning, rewrote its manifest and broke the anchor
    # ledger's digest. A night that has a reading is never read again.
    extent = (SNAP / "extent.txt").read_bytes()
    first = nightly.run(tmp_path, client=FakeClient(extent), today="2026-10-15")
    manifest = tmp_path / nightly.BASE / "2026-10-15/manifest.json"
    before = manifest.read_bytes()
    again = FakeClient(extent)
    second = nightly.run(tmp_path, client=again, today="2026-10-15")
    assert again.calls == []
    assert manifest.read_bytes() == before
    assert second == first


def test_inserted_and_vanished_segments():
    prev = nightly.parse_table((SNAP / "extent.txt").read_bytes())
    cur = [row for row in prev if row["Earliest"] != prev[1]["Earliest"]]
    assert [e["kind"] for e in nightly.reingestion(prev, cur)] == ["segment_gone"]
    assert [e["kind"] for e in nightly.reingestion(cur, prev)] == ["segment_inserted"]
    assert nightly.reingestion(None, prev) == []


def test_outage_is_recorded_not_invented(tmp_path):
    class Down(FakeClient):
        def fetch(self, url, headers=None):
            if "extent" in url or "dataselect" in url:
                return b"", 503
            return super().fetch(url, headers)
    r = nightly.run(tmp_path, client=Down(b""), today="2026-10-15")
    assert r["station_day"]["outage"] is True
    assert r["publisher"]["extent"]["file"] is None
    assert r["reingestion"]["unverifiable"]


def test_verifier_recomputes_reingestion_events(tmp_path):
    import importlib.util
    import sys
    spec = importlib.util.spec_from_file_location("verifymod_pln", ROOT / "verify.py")
    verify = importlib.util.module_from_spec(spec)
    sys.modules["verifymod_pln"] = verify
    spec.loader.exec_module(verify)

    extent = (SNAP / "extent.txt").read_bytes()
    nightly.run(tmp_path, client=FakeClient(extent), today="2026-10-15")
    nightly.run(tmp_path, client=FakeClient(rewrite_closed_segment(extent)),
                today="2026-10-16")

    def problems():
        registry: dict = {}
        verify.check_snapshots(tmp_path, nightly.BASE, [], registry, False)
        out: list[str] = []
        verify.check_planetary_readings(tmp_path, registry, out)
        return out

    assert problems() == []
    path = tmp_path / nightly.READINGS / "2026-10-16.json"
    reading = json.loads(path.read_text())
    reading["reingestion"]["events"] = []      # a rewrite silently dropped
    path.write_text(json.dumps(reading))
    assert any("recomputation" in p for p in problems())
