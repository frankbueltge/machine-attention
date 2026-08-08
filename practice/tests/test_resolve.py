import json
from pathlib import Path

from practice.foreknown import resolve, sources
from practice.foreknown.run import run
from practice.preserve import read_json

from .test_foreknown import GDACS_FIXTURE, FakeClient


def _tc_future(**overrides):
    base = {
        "id": "gdacs-tc-1001297", "kind": "ALERT_EPISODE", "source": "GDACS",
        "hazard": "tropical cyclone", "what": "Tropical Cyclone DOLPHIN-26",
        "where": "Marshall Islands, Japan", "iso3": ["JPN", "MHL"],
        "severity": "Orange", "status": "CLOSED_BY_SOURCE",
        "announced_at": "2026-08-08T05:46:00+00:00",
        "window": {"from": "2026-07-27T00:00:00", "to": "2026-08-08T12:00:00"},
        "history": [
            {"ts": "2026-08-08T05:46:00+00:00", "event": "NOTARIZED",
             "snapshot": "foreknown/snapshots/2026-08-08/gdacs.json"},
        ],
    }
    base.update(overrides)
    return base


def test_storm_token_extraction():
    assert resolve.storm_token("Tropical Cyclone DOLPHIN-26") == "DOLPHIN"
    assert resolve.storm_token("DOLPHIN (Hurricane)") == "DOLPHIN"
    assert resolve.storm_token("Tropical Storm") is None


def test_episode_verdict_measures_duration_revisions_and_escalation():
    future = _tc_future(history=[
        {"ts": "2026-08-08T05:46:00+00:00", "event": "NOTARIZED", "snapshot": "a"},
        {"ts": "2026-08-09T05:46:00+00:00", "event": "REVISED",
         "changes": {"severity": {"from": "Orange", "to": "Red"}}, "snapshot": "b"},
        {"ts": "2026-08-10T05:46:00+00:00", "event": "CLOSED_BY_SOURCE"},
    ])
    resolution = resolve.resolve_future(future, {future["id"]: future},
                                        "2026-08-08")
    assert resolution["verdict"] == "EPISODE_ENDED"
    assert resolution["measured"]["revisions"] == 1
    assert resolution["measured"]["severity_path"] == ["Orange", "Red"]
    assert resolution["measured"]["escalated"] is True
    assert resolution["measured"]["episode_days"] == 12.5
    assert resolution["cold_start"] is True
    assert resolution["evidence"] == ["a", "b"]


def test_forecast_materializes_against_the_registry_with_lead_time():
    storm = {
        "id": "nhc-al052026", "kind": "FORECAST", "source": "NHC",
        "hazard": "tropical cyclone", "what": "DOLPHIN (Hurricane)",
        "where": "AT5", "severity": "hurricane", "status": "DISSIPATED",
        "announced_at": "2026-07-25T00:00:00+00:00",
        "window": {"from": "2026-07-25T00:00:00", "to": None},
        "history": [{"ts": "2026-07-25T00:00:00+00:00", "event": "NOTARIZED",
                     "snapshot": "n"}],
    }
    episode = _tc_future()
    resolution = resolve.resolve_future(storm, {storm["id"]: storm,
                                                episode["id"]: episode},
                                        "2026-07-25")
    assert resolution["verdict"] == "MATERIALIZED_AS_ALERT"
    assert resolution["measured"]["matched"] == "gdacs-tc-1001297"
    assert resolution["measured"]["lead_time_hours"] == 48.0
    assert set(resolution["evidence"]) == {"n",
        "foreknown/snapshots/2026-08-08/gdacs.json"}


def test_forecast_without_match_stays_a_statement_about_the_record():
    storm = {
        "id": "nhc-ep012026", "kind": "FORECAST", "source": "NHC",
        "hazard": "tropical cyclone", "what": "QUIETONE (Tropical Storm)",
        "where": "EP1", "severity": "storm", "status": "DISSIPATED",
        "announced_at": "2026-08-01T00:00:00+00:00", "window": {},
        "history": [{"ts": "2026-08-01T00:00:00+00:00", "event": "NOTARIZED",
                     "snapshot": "n"}],
    }
    resolution = resolve.resolve_future(storm, {storm["id"]: storm}, "2026-08-01")
    assert resolution["verdict"] == "NO_ALERT_MATCH"
    assert "about the record" in resolution["note"]


def test_resolve_pending_is_idempotent_and_skips_open(tmp_path: Path):
    episode = _tc_future()
    open_one = _tc_future(id="gdacs-dr-1", status="OPEN")
    registry = {"futures": {episode["id"]: episode, open_one["id"]: open_one}}
    first = resolve.resolve_pending(tmp_path, registry)
    assert [r["future"] for r in first] == [episode["id"]]
    assert (tmp_path / "foreknown/resolutions/gdacs-tc-1001297.json").exists()
    assert resolve.resolve_pending(tmp_path, registry) == []


NHC_STORM = {"activeStorms": [{"id": "al052026", "name": "DOLPHIN",
                               "classification": "Hurricane",
                               "intensity": "85", "binNumber": "AT5",
                               "lastUpdate": "2026-08-07T21:00:00.000Z"}]}


def test_nightly_run_resolves_a_dissipated_forecast(tmp_path: Path):
    night1 = {
        sources.GDACS_URL: (json.dumps(GDACS_FIXTURE).encode(), 200),
        sources.NHC_URL: (json.dumps(NHC_STORM).encode(), 200),
        sources.FTS_PLANS_URL: (json.dumps({"data": []}).encode(), 200),
    }
    night2 = {
        sources.GDACS_URL: (json.dumps(GDACS_FIXTURE).encode(), 200),
        sources.NHC_URL: (json.dumps({"activeStorms": []}).encode(), 200),
        sources.FTS_PLANS_URL: (json.dumps({"data": []}).encode(), 200),
    }
    run(tmp_path, "2026-08-09", FakeClient(night1))
    summary = run(tmp_path, "2026-08-10", FakeClient(night2))
    assert summary["closed"] == 1 and summary["resolved"] == 1

    resolution = read_json(tmp_path / "foreknown/resolutions/nhc-al052026.json")
    assert resolution["verdict"] == "MATERIALIZED_AS_ALERT"
    assert resolution["measured"]["matched"] == "gdacs-tc-1001297"
    run_record = read_json(tmp_path / "foreknown/snapshots/2026-08-10/run.json")
    assert run_record["resolved"] == ["nhc-al052026"]
