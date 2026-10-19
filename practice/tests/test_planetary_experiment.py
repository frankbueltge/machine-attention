"""Planetary Listening E-experiment: the tally counts what nightly readings
show, the clock test reads a shift only from both sides, and verify.py holds
the committed criteria to their window."""

import datetime as dt
import json
from pathlib import Path

from practice.planetary import detect, experiment
from practice.preserve import sha256, write_json

from .test_interval_register import verifier

REPO = Path(__file__).resolve().parents[2]
FIRST = "2026-10-21"


def plan(nights=14):
    return {"window": {"first": FIRST, "nights": nights, "closes": "2026-11-03"},
            "criteria": {"A1_min_nights": 13, "A1_max_consecutive_missing": 1,
                         "A2_max_failed_nights": 1,
                         "A4_max_night_bytes": 409600,
                         "B6_detector": detect.parameters(),
                         "B6_strong_ratio": 50.0, "B6_max_excerpts": 4},
            "clock_test": {"shift_day": "2026-10-25", "tolerance_min": 10,
                           "min_days_each_side": 2}}


def reading(date, onset="07:31:40", attest=200, day_status=200, extent=200,
            isc=204, http=200, events=(), detector=None, word=None):
    day = (dt.date.fromisoformat(date) - dt.timedelta(days=1)).isoformat()
    strong = [] if onset is None else [
        {"onset": f"{day}T{onset}.000000+00:00", "peak_ratio": 120.0}]
    r = {"date": date, "day": day, "detector": detector or detect.parameters(),
         "strong_ratio": 50.0, "max_excerpts_per_station_day": 4,
         "station_day": {"http_status": day_status, "outage": day_status != 200,
                         "strong": strong},
         "publisher": {"availability": {"http_status": attest},
                       "extent": {"http_status": extent},
                       "wfcatalog": {"http_status": attest}},
         "reingestion": {"events": list(events)},
         "catalogues": [{"catalogue": "ISC", "http_status": isc, "rows": 0},
                        {"catalogue": "USGS", "http_status": 200, "rows": 0}],
         "requests": [{"url": "https://geofon.gfz.de/x", "http_status": http}]}
    if word:
        r["site"] = word
    return r


def window_dates(n=14):
    first = dt.date.fromisoformat(FIRST)
    return [(first + dt.timedelta(days=i)).isoformat() for i in range(n)]


def test_a_clean_window_tallies_clean():
    rs = [reading(d) for d in window_dates()]
    out = experiment.tally(plan(), rs, "2026-11-04")
    assert out["closed"] and out["nights_due"] == 14
    assert out["A1_missing_nights"] == [] and out["A1_pass"] and out["A2_pass"]
    assert out["A3_http_429"] == [] and out["B6_detector_changes"] == []
    assert out["B1_attest_missing"] == [] and out["C_class_words"] == {}
    assert len(out["B3_B5_calendar"]) == 14


def test_two_missing_nights_in_a_row_fail_a1_even_above_the_minimum():
    dates = window_dates()
    rs = [reading(d) for d in dates if d not in dates[3:5]]
    out = experiment.tally(plan(15), rs, "2026-11-05")
    assert out["A1_missing_nights"] == dates[3:5] + ["2026-11-04"]
    assert not out["A1_pass"]


def test_failures_throttle_budget_detector_and_words_are_counted():
    d = window_dates()
    rs = [reading(d[0], day_status=500), reading(d[1], isc=503),
          reading(d[2], http=429), reading(d[3], attest=204),
          reading(d[4], detector={"version": "stalta-v2"}),
          reading(d[5], word="Quarry")]
    out = experiment.tally(plan(), rs, "2026-11-04", sizes={d[6]: 500_000})
    assert sorted(out["A2_nights_with_failures"]) == d[:2]
    assert not out["A2_pass"]
    assert out["A3_http_429"] == [d[2]]
    assert out["A4_nights_over_budget"] == {d[6]: 500_000}
    assert out["B1_attest_missing"] == [d[3]]
    assert out["B6_detector_changes"] == [d[4]]
    assert out["C_class_words"] == {d[5]: ["quarry"]}


def clock(after_onset):
    # Days read: Wed 10-14 and Thu 10-15 before; Mon 10-26, Tue 10-27 after;
    # Sat 10-24 (weekend) never counts.
    rs = [reading("2026-10-15"), reading("2026-10-16"),
          reading("2026-10-25", onset="11:00:00"),
          reading("2026-10-27", onset=after_onset),
          reading("2026-10-28", onset=after_onset)]
    return experiment.clock_test(rs, plan()["clock_test"])


def test_the_clock_test_tells_local_from_utc_from_neither():
    assert clock("08:31:40")["verdict"] == "local"
    assert clock("07:33:00")["verdict"] == "utc"
    assert clock("10:00:00")["verdict"] == "neither"
    one_side = experiment.clock_test([reading("2026-10-15")],
                                     plan()["clock_test"])
    assert one_side["verdict"] == "undetermined"


def committed_tree(tmp_path, **override):
    doc = tmp_path / "docs" / "k.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("criteria\n", encoding="utf-8")
    write_json(tmp_path / "planetary" / "readings" / "2026-10-15.json", {})
    e = {"schema": "planetary-experiment-v1", "committed": "2026-10-19",
         "document": "docs/k.md", "document_sha256": sha256(doc.read_bytes()),
         "pre_window_readings": ["2026-10-15"],
         "window": {"first": FIRST, "nights": 14, "closes": "2026-11-03",
                    "review_from": "2026-11-04"},
         "criteria": {"A1_min_nights": 13, "A4_max_night_bytes": 409600}}
    e.update(override)
    write_json(tmp_path / experiment.EXPERIMENT, e)
    return tmp_path


def check(root):
    problems = []
    verifier().check_planetary_experiment(root, problems)
    return problems


def test_verify_accepts_criteria_committed_before_the_window(tmp_path):
    assert check(committed_tree(tmp_path)) == []


def test_verify_rejects_late_criteria_and_edited_prose(tmp_path):
    root = committed_tree(tmp_path, committed="2026-10-21")
    (root / "docs" / "k.md").write_text("criteria, softened\n", encoding="utf-8")
    problems = check(root)
    assert any("not before the first night" in p for p in problems)
    assert any("changed without its hash" in p for p in problems)


def test_verify_rejects_a_short_window_and_a_loose_budget(tmp_path):
    root = committed_tree(tmp_path, window={
        "first": FIRST, "nights": 7, "closes": "2026-10-27",
        "review_from": "2026-10-28"},
        criteria={"A1_min_nights": 7, "A4_max_night_bytes": 10**6})
    problems = check(root)
    assert any("14 nights" in p for p in problems)
    assert any("400 KB" in p for p in problems)


def test_the_committed_experiment_is_clean():
    assert check(REPO) == []
    e = json.loads((REPO / experiment.EXPERIMENT).read_text(encoding="utf-8"))
    assert e["window"]["first"] == FIRST and e["window"]["nights"] == 14
    assert e["criteria"]["B6_detector"] == detect.parameters()


def test_the_committed_readings_tally_without_error():
    out = experiment.full_tally(REPO, "2026-10-19")
    assert out["nights_due"] == 0 and out["C_class_words"] == {}
