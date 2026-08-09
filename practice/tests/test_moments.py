import json
from pathlib import Path

from practice import moments as practice_moments
from practice.foreknown.moments import moments


def _repo(tmp_path: Path, futures: dict, run_dates=("2026-08-08",
                                                    "2026-08-09")) -> Path:
    registry = tmp_path / "foreknown" / "registry.json"
    registry.parent.mkdir(parents=True)
    registry.write_text(json.dumps({"futures": futures}), encoding="utf-8")
    for date in run_dates:
        night = tmp_path / "foreknown" / "snapshots" / date
        night.mkdir(parents=True)
        (night / "run.json").write_text(json.dumps({"date": date}),
                                        encoding="utf-8")
    return tmp_path


def _future(fid: str, announced_at: str, window_to: str,
            history: list[dict]) -> dict:
    return {"id": fid, "what": f"Warning {fid}", "where": "Somewhere",
            "hazard": "flood", "severity": "Orange", "source": "GDACS",
            "kind": "ALERT_EPISODE", "status": "OPEN", "iso3": ["KEN"],
            "announced_at": announced_at,
            "window": {"from": "2026-08-01T00:00:00", "to": window_to},
            "history": history}


def test_the_founding_import_is_baseline_not_a_moment(tmp_path):
    root = _repo(tmp_path, {"a": _future(
        "a", "2026-08-08T17:00:00+00:00", "2026-08-06T00:00:00",
        [{"ts": "2026-08-08T17:00:00+00:00", "event": "NOTARIZED",
          "snapshot": "foreknown/snapshots/2026-08-08/gdacs.json"}])})
    assert moments(root) == []


def test_a_revision_becomes_a_moment_with_the_measured_span(tmp_path):
    root = _repo(tmp_path, {"a": _future(
        "a", "2026-08-08T17:00:00+00:00", "2026-08-06T00:00:00",
        [{"ts": "2026-08-08T17:00:00+00:00", "event": "NOTARIZED",
          "snapshot": "s1"},
         {"ts": "2026-08-09T06:00:00+00:00", "event": "REVISED",
          "changes": {"severity": {"from": "Orange", "to": "Red"}},
          "snapshot": "foreknown/snapshots/2026-08-09/gdacs.json"}])})
    got = moments(root)
    assert len(got) == 1
    moment = got[0]
    assert moment["mode"] == "revision"
    assert moment["statement"] == ("A warning changed 13 hours after it was "
                                   "first preserved.")
    assert moment["subject"] == "Warning a"
    assert moment["enter"] == "/attention/future/a.html"
    assert moment["evidence"] == "foreknown/snapshots/2026-08-09/gdacs.json"


def test_a_late_cold_start_notarization_stays_off_the_stage(tmp_path):
    # Seen for the first time on night 2, window already past: baseline.
    cold = _future("cold", "2026-08-09T06:00:00+00:00", "2026-08-01T00:00:00",
                   [{"ts": "2026-08-09T06:00:00+00:00", "event": "NOTARIZED",
                     "snapshot": "s"}])
    # Seen for the first time on night 2, window still open: a real moment.
    fresh = _future("fresh", "2026-08-09T06:00:00+00:00",
                    "2026-08-20T00:00:00",
                    [{"ts": "2026-08-09T06:00:00+00:00", "event": "NOTARIZED",
                      "snapshot": "s"}])
    root = _repo(tmp_path, {"cold": cold, "fresh": fresh})
    got = moments(root)
    assert [m["enter"] for m in got] == ["/attention/future/fresh.html"]
    assert got[0]["statement"] == "A new announced future entered the record."


def test_corrections_and_closures_are_moments_newest_first(tmp_path):
    root = _repo(tmp_path, {"a": _future(
        "a", "2026-08-08T17:00:00+00:00", "2026-08-06T00:00:00",
        [{"ts": "2026-08-08T17:00:00+00:00", "event": "NOTARIZED",
          "snapshot": "s1"},
         {"ts": "2026-08-09T06:00:00+00:00", "event": "CORRECTED",
          "corrections": {"iso3": {"from": ["KEN"], "to": ["KEN", "SOM"]}},
          "snapshot": "s2"},
         {"ts": "2026-08-09T07:00:00+00:00", "event": "CLOSED_BY_SOURCE"}])})
    got = moments(root)
    assert [m["mode"] for m in got] == ["closure", "correction"]
    assert got[1]["statement"] == ("The machine corrected its own record — "
                                   "the feed had said it all along.")
    # An event without a snapshot anchor still names its register.
    assert got[0]["evidence"] == "foreknown/registry.json"


def test_the_practice_file_carries_the_contract_and_is_deterministic(tmp_path):
    root = _repo(tmp_path, {"a": _future(
        "a", "2026-08-08T17:00:00+00:00", "2026-08-06T00:00:00",
        [{"ts": "2026-08-08T17:00:00+00:00", "event": "NOTARIZED",
          "snapshot": "s1"},
         {"ts": "2026-08-09T06:00:00+00:00", "event": "REVISED",
          "changes": {"severity": {"from": "Orange", "to": "Red"}},
          "snapshot": "s2"}])})
    payload = practice_moments.build(root)
    assert payload["$contract"] == "stage-moments/1"
    assert payload["practice"]["id"] == "machine-attention"
    assert len(payload["moments"]) == 1
    assert payload == practice_moments.build(root)
