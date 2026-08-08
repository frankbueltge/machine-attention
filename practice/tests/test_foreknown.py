import json
from pathlib import Path

import pytest

from practice.foreknown import sources
from practice.foreknown.futures import update_registry, is_overdue
from practice.foreknown.run import run
from practice.preserve import read_json


GDACS_FIXTURE = {"features": [
    {"properties": {"eventid": 1001297, "eventtype": "TC", "alertlevel": "Orange",
                    "name": "Tropical Cyclone DOLPHIN-26",
                    "country": "Marshall Islands, Japan",
                    "affectedcountries": [{"iso3": "MHL"}, {"iso3": "JPN"}],
                    "fromdate": "2026-07-27T00:00:00",
                    "todate": "2026-08-08T12:00:00",
                    "url": {"report": "https://www.gdacs.org/report?eventid=1001297"}}},
    {"properties": {"eventid": 1027450, "eventtype": "DR", "alertlevel": "Orange",
                    "name": "Drought in Ethiopia, Kenya, Somalia",
                    "country": "Ethiopia, Kenya, Somalia",
                    "affectedcountries": [{"iso3": "ETH"}, {"iso3": "KEN"}],
                    "fromdate": "2026-04-21T00:00:00",
                    "todate": "2026-08-06T00:00:00", "url": "plain-string"}},
]}


def test_gdacs_extraction_is_deterministic_and_org_level():
    futures = sources.gdacs_futures(GDACS_FIXTURE)
    assert [f["id"] for f in futures] == ["gdacs-tc-1001297", "gdacs-dr-1027450"]
    tc = futures[0]
    assert tc["kind"] == "ALERT_EPISODE" and tc["hazard"] == "tropical cyclone"
    assert tc["window"]["to"] == "2026-08-08T12:00:00"
    assert tc["iso3"] == ["JPN", "MHL"]


def test_nhc_empty_list_is_the_honest_quiet_state():
    assert sources.nhc_futures({"activeStorms": []}) == []


def test_registry_notarize_revise_close_lifecycle():
    registry = {"futures": {}}
    observed = sources.gdacs_futures(GDACS_FIXTURE)
    anchors = {"GDACS": "foreknown/snapshots/2026-08-08/gdacs.json"}

    summary = update_registry(registry, observed, anchors)
    assert len(summary["notarized"]) == 2
    tc = registry["futures"]["gdacs-tc-1001297"]
    announced_at = tc["announced_at"]
    assert tc["history"][0]["event"] == "NOTARIZED"

    # night 2: the cyclone's window is extended → REVISED, announced_at fixed
    revised = json.loads(json.dumps(GDACS_FIXTURE))
    revised["features"][0]["properties"]["todate"] = "2026-08-10T12:00:00"
    summary = update_registry(registry, sources.gdacs_futures(revised), anchors)
    assert summary["revised"] == ["gdacs-tc-1001297"]
    tc = registry["futures"]["gdacs-tc-1001297"]
    assert tc["announced_at"] == announced_at
    changes = tc["history"][-1]["changes"]
    assert changes["window"]["from"]["to"] == "2026-08-08T12:00:00"

    # night 3: the cyclone leaves the feed → CLOSED_BY_SOURCE
    only_drought = {"features": [GDACS_FIXTURE["features"][1]]}
    summary = update_registry(registry, sources.gdacs_futures(only_drought), anchors)
    assert summary["closed"] == ["gdacs-tc-1001297"]
    assert registry["futures"]["gdacs-tc-1001297"]["status"] == "CLOSED_BY_SOURCE"


def test_absent_source_closes_nothing():
    """A source outage proves nothing (I4): its futures stay OPEN."""
    registry = {"futures": {}}
    update_registry(registry, sources.gdacs_futures(GDACS_FIXTURE),
                    {"GDACS": "a"})
    summary = update_registry(registry, [], {})  # nothing observed, no anchors
    assert summary["closed"] == []
    assert registry["futures"]["gdacs-tc-1001297"]["status"] == "OPEN"


def test_overdue_is_a_flag_not_a_closure():
    registry = {"futures": {}}
    update_registry(registry, sources.gdacs_futures(GDACS_FIXTURE), {"GDACS": "a"})
    drought = registry["futures"]["gdacs-dr-1027450"]
    assert is_overdue(drought, "2026-08-08T00:00:00+00:00")
    assert drought["status"] == "OPEN"


class FakeClient:
    def __init__(self, responses):
        self._responses = responses
        self.requests = 0
        self.http_429 = 0

    def fetch(self, url):
        self.requests += 1
        return self._responses.get(url, (b"", 404))


def test_notary_run_end_to_end(tmp_path: Path):
    responses = {
        sources.GDACS_URL: (json.dumps(GDACS_FIXTURE).encode(), 200),
        sources.NHC_URL: (json.dumps({"activeStorms": []}).encode(), 200),
        sources.FTS_PLANS_URL: (json.dumps({"data": []}).encode(), 200),
    }
    summary = run(tmp_path, "2026-08-08", FakeClient(responses))
    assert summary["notarized"] == 2 and summary["failures"] == 0

    manifest = read_json(tmp_path / "foreknown/snapshots/2026-08-08/manifest.json")
    assert len(manifest["entries"]) == 3
    registry = read_json(tmp_path / "foreknown/registry.json")
    anchor = registry["futures"]["gdacs-tc-1001297"]["history"][0]["snapshot"]
    assert anchor == "foreknown/snapshots/2026-08-08/gdacs.json"
    log = (tmp_path / "autonomy/log.jsonl").read_text().strip().splitlines()
    assert json.loads(log[-1])["step"] == "foreknown-notary-run"

    with pytest.raises(SystemExit):
        run(tmp_path, "2026-08-08", FakeClient(responses))
