"""The reaction-series check, proven to bite.

A resolution may claim what money and attention did while a warning ran only
as far as the committed reaction readings say so. Each test builds a minimal
tree, breaks exactly one thing, and asserts the verifier names it — a check
that never fires is decoration. (Added 2026-08-22 with the join itself, after
the E1 review found the series had never been written into a resolution.)
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def load_verify():
    spec = importlib.util.spec_from_file_location("verifyseries", REPO / "verify.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verifyseries"] = mod
    spec.loader.exec_module(mod)
    return mod


verify = load_verify()

FID = "gdacs-dr-1017863"


def _entry(articles: int, ratio: float, funded: int) -> dict:
    return {"attention": {"articles": articles, "ratio_to_baseline": ratio},
            "money": {"has_fts_plan_match": True, "plans": [1516],
                      "plan_requirements_usd": 900, "plan_funded_usd": funded}}


def _tree(root: Path, nights: list[dict], measured: dict | None = None) -> None:
    readings = root / "foreknown" / "reaction" / "readings"
    readings.mkdir(parents=True, exist_ok=True)
    (readings / "2026-08-08.json").write_text(json.dumps(
        {"date": "2026-08-08", "attention_day": "2026-08-06",
         "futures": {FID: _entry(300, 1.1, 10)}}), encoding="utf-8")
    (readings / "2026-08-09.json").write_text(json.dumps(
        {"date": "2026-08-09", "attention_day": "2026-08-07",
         "futures": {FID: _entry(900, 2.6, 45)}}), encoding="utf-8")
    resolutions = root / "foreknown" / "resolutions"
    resolutions.mkdir(parents=True, exist_ok=True)
    (resolutions / f"{FID}.json").write_text(json.dumps(
        {"future": FID, "verdict": "EPISODE_ENDED",
         "resolved_at": "2026-08-10T06:00:00+00:00",
         "reaction": {"nights": nights,
                      "measured": measured if measured is not None else {
                          "nights_watched": len(nights),
                          "attention_peak": {"date": "2026-08-09",
                                             "articles": 900,
                                             "ratio_to_baseline": 2.6},
                          "money_funded_first_usd": 10,
                          "money_funded_last_usd": 45,
                          "money_funded_delta_usd": 35,
                          "money_requirements_last_usd": 900},
                      "limits": ["the money figures are the plans' own"]}}),
        encoding="utf-8")


def _honest_nights() -> list[dict]:
    return [
        {"date": "2026-08-08", "attention_day": "2026-08-06", "articles": 300,
         "ratio_to_baseline": 1.1, "has_fts_plan_match": True,
         "plan_requirements_usd": 900, "plan_funded_usd": 10},
        {"date": "2026-08-09", "attention_day": "2026-08-07", "articles": 900,
         "ratio_to_baseline": 2.6, "has_fts_plan_match": True,
         "plan_requirements_usd": 900, "plan_funded_usd": 45},
    ]


def test_an_honest_series_passes(tmp_path: Path):
    _tree(tmp_path, _honest_nights())
    problems: list[str] = []
    verify.check_foreknown_reaction_series(tmp_path, problems)
    assert problems == []


def test_a_retyped_number_is_caught(tmp_path: Path):
    nights = _honest_nights()
    nights[1]["articles"] = 9000
    _tree(tmp_path, nights)
    problems: list[str] = []
    verify.check_foreknown_reaction_series(tmp_path, problems)
    assert any("articles" in p for p in problems)


def test_a_dropped_night_is_caught(tmp_path: Path):
    nights = _honest_nights()[:1]
    _tree(tmp_path, nights, measured={
        "nights_watched": 1,
        "attention_peak": {"date": "2026-08-08", "articles": 300,
                           "ratio_to_baseline": 1.1},
        "money_funded_first_usd": 10, "money_funded_last_usd": 10,
        "money_funded_delta_usd": 0, "money_requirements_last_usd": 900})
    problems: list[str] = []
    verify.check_foreknown_reaction_series(tmp_path, problems)
    assert any("do not match the committed readings" in p for p in problems)


def test_a_flattered_money_delta_is_caught(tmp_path: Path):
    measured = {"nights_watched": 2,
                "attention_peak": {"date": "2026-08-09", "articles": 900,
                                   "ratio_to_baseline": 2.6},
                "money_funded_first_usd": 10, "money_funded_last_usd": 45,
                "money_funded_delta_usd": 3500,
                "money_requirements_last_usd": 900}
    _tree(tmp_path, _honest_nights(), measured=measured)
    problems: list[str] = []
    verify.check_foreknown_reaction_series(tmp_path, problems)
    assert any("money delta" in p for p in problems)


def test_a_series_without_its_limits_is_caught(tmp_path: Path):
    _tree(tmp_path, _honest_nights())
    path = tmp_path / "foreknown" / "resolutions" / f"{FID}.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc["reaction"]["limits"] = []
    path.write_text(json.dumps(doc), encoding="utf-8")
    problems: list[str] = []
    verify.check_foreknown_reaction_series(tmp_path, problems)
    assert any("limits" in p for p in problems)


def test_a_night_after_the_resolution_is_not_demanded(tmp_path: Path):
    """A future may REAPPEAR and re-enter the readings. An append-only
    resolution cannot grow with it, so the verifier must not demand that it
    does — otherwise a legal event turns into a permanently red gate."""
    _tree(tmp_path, _honest_nights())
    readings = tmp_path / "foreknown" / "reaction" / "readings"
    (readings / "2026-08-14.json").write_text(json.dumps(
        {"date": "2026-08-14", "attention_day": "2026-08-12",
         "futures": {FID: _entry(120, 0.8, 45)}}), encoding="utf-8")
    problems: list[str] = []
    verify.check_foreknown_reaction_series(tmp_path, problems)
    assert problems == []
