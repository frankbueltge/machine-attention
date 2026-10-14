"""Planetary Listening spike: requests, licence filter, storage model.
A fake client serves one committed excerpt as every day file. No network."""

import json
from pathlib import Path

from practice.planetary import mseed, spike

ROOT = Path(__file__).resolve().parents[2]
EXCERPT = ROOT / "planetary/probes/2026-10-14/GE.RUE.HHZ/20261008T073232.mseed"


class FakeClient:
    def __init__(self, data):
        self.data = data
        self.calls = []

    def fetch(self, url, headers=None):
        self.calls.append(url)
        if "dataselect" in url:
            return self.data, 200
        if "isc.ac.uk" in url:
            return b"", 204
        return b'{"type":"FeatureCollection","features":[]}', 200


def test_requests_are_literal_per_node():
    ge = spike.dataselect_url("GE", "RUE", "HHZ", "a", "b")
    gr = spike.dataselect_url("GR", "KAST", "HHZ", "a", "b")
    assert ge.startswith("https://geofon.gfz.de/") and "loc=--" in ge
    assert gr.startswith("https://eida.bgr.de/") and "location=--" in gr


def test_only_licence_filtered_networks_no_citizen_stations():
    assert set(spike.NETWORKS) == {"GE", "GR"}
    assert all(n["licence"] == "CC-BY-4.0" and n["doi"] for n in spike.NETWORKS.values())


def test_run_keeps_ledger_and_record_aligned_excerpts_only(tmp_path, monkeypatch):
    monkeypatch.setattr(spike, "RUE_DAYS", ["2026-10-08"])
    monkeypatch.setattr(spike, "GESEKE_DECLARED", [])
    monkeypatch.setattr(spike, "GESEKE_CONTROL", [])
    data = EXCERPT.read_bytes()
    reading = spike.run(tmp_path, client=FakeClient(data), today="2026-10-14")
    (day,) = reading["pairing_a"]["days"]
    assert day["licence"] == "CC-BY-4.0" and day["doi"] == "10.14470/TR560404"
    assert len(day["excerpts"]) <= spike.MAX_EXCERPTS
    assert all(e["committed"] is False for e in reading["requests"])
    manifest = json.loads((tmp_path / spike.BASE / "2026-10-14/manifest.json").read_text())
    for entry in manifest["entries"]:
        cut = (tmp_path / entry["file"]).read_bytes()
        assert cut in data                      # a subset of the publisher's bytes
        assert len(cut) % 512 == 0 and mseed.records(cut)
    assert {c["rows"] for c in reading["catalogues"]} == {0}
    assert "index" not in json.dumps(reading).lower()   # no loudness index (audit cond. 5)
