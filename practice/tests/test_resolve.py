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
        {"ts": "2026-08-08T05:46:00+00:00", "event": "REVISED",
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
    run(tmp_path, "2026-08-08", FakeClient(night1))
    summary = run(tmp_path, "2026-08-10", FakeClient(night2))
    assert summary["closed"] == 1 and summary["resolved"] == 1

    resolution = read_json(tmp_path / "foreknown/resolutions/nhc-al052026.json")
    assert resolution["verdict"] == "MATERIALIZED_AS_ALERT"
    assert resolution["measured"]["matched"] == "gdacs-tc-1001297"
    run_record = read_json(tmp_path / "foreknown/snapshots/2026-08-10/run.json")
    assert run_record["resolved"] == ["nhc-al052026"]


def _reaction_reading(day: str, futures: dict, attention_day: str) -> dict:
    return {"date": day, "attention_day": attention_day, "futures": futures}


def _write_readings(root: Path, readings: list[dict]) -> None:
    directory = root / "foreknown" / "reaction" / "readings"
    directory.mkdir(parents=True, exist_ok=True)
    for reading in readings:
        (directory / f"{reading['date']}.json").write_text(
            json.dumps(reading), encoding="utf-8")


def _entry(articles: int, ratio: float, funded: int, requirements: int) -> dict:
    return {"attention": {"articles": articles, "ratio_to_baseline": ratio,
                          "baseline_median_articles": 100.0,
                          "share_per_10k": 1.0},
            "money": {"has_fts_plan_match": True, "plans": [1516],
                      "plan_requirements_usd": requirements,
                      "plan_funded_usd": funded},
            "iso3": ["KEN"], "fips": ["KE"], "unmapped_iso3": []}


def test_reaction_series_reads_only_the_nights_that_carried_the_future(tmp_path: Path):
    fid = "gdacs-dr-1017863"
    _write_readings(tmp_path, [
        _reaction_reading("2026-08-08", {fid: _entry(800, 1.2, 100, 900)}, "2026-08-06"),
        _reaction_reading("2026-08-09", {"other": _entry(1, 1.0, 0, 0)}, "2026-08-07"),
        _reaction_reading("2026-08-10", {fid: _entry(2400, 3.4, 160, 900)}, "2026-08-08"),
    ])
    series = resolve.reaction_series(tmp_path, fid)
    assert [night["date"] for night in series["nights"]] == ["2026-08-08",
                                                             "2026-08-10"]
    assert series["nights"][0]["attention_day"] == "2026-08-06"
    assert series["measured"]["nights_watched"] == 2
    # The peak is the loudest night against the country's own baseline, not
    # the night with the most articles in absolute terms.
    assert series["measured"]["attention_peak"]["date"] == "2026-08-10"
    assert series["measured"]["money_funded_delta_usd"] == 60
    assert series["measured"]["money_requirements_last_usd"] == 900
    assert series["limits"], "a series without its limits is a claim"


def test_reaction_series_is_absent_not_empty_for_an_unwatched_future(tmp_path: Path):
    _write_readings(tmp_path, [
        _reaction_reading("2026-08-08", {"other": _entry(1, 1.0, 0, 0)}, "2026-08-06"),
    ])
    assert resolve.reaction_series(tmp_path, "gdacs-tc-1001297") is None


def test_reaction_series_says_so_when_no_plan_lists_the_countries(tmp_path: Path):
    fid = "gdacs-eq-1494848"
    entry = _entry(50, 0.9, 0, 0)
    entry["money"] = {"has_fts_plan_match": False, "plans": [],
                      "plan_requirements_usd": 0, "plan_funded_usd": 0}
    _write_readings(tmp_path, [_reaction_reading("2026-08-08", {fid: entry},
                                                 "2026-08-06")])
    series = resolve.reaction_series(tmp_path, fid)
    assert series["measured"]["money_plan_match"] is False
    assert "money_funded_delta_usd" not in series["measured"]


def test_resolution_carries_what_moved_while_the_clock_ran(tmp_path: Path):
    future = _tc_future()
    fid = future["id"]
    registry = {"futures": {fid: future}}
    (tmp_path / "foreknown").mkdir(parents=True, exist_ok=True)
    _write_readings(tmp_path, [
        _reaction_reading("2026-08-08", {fid: _entry(300, 1.1, 10, 500)}, "2026-08-06"),
        _reaction_reading("2026-08-09", {fid: _entry(900, 2.6, 45, 500)}, "2026-08-07"),
    ])
    resolutions = resolve.resolve_pending(tmp_path, registry)
    assert len(resolutions) == 1
    written = read_json(tmp_path / "foreknown" / "resolutions" / f"{fid}.json")
    assert written["reaction"]["measured"]["money_funded_delta_usd"] == 35
    assert written["reaction"]["measured"]["attention_peak"]["ratio_to_baseline"] == 2.6
