"""Register A, rule excess-v1: excess against the baseline trend. Pure, no network."""

import json
from pathlib import Path

import pytest

from practice.syntheticflood import excess, wordlist

ROOT = Path(__file__).resolve().parents[2]
YEARS = ("2018", "2019", "2020", "2021", "2022")


def word(name, lst, shares, verdict="stable"):
    return {"list": lst, "word": name, "verdict": verdict,
            "shares": dict(zip(YEARS, shares))}


def test_position_puts_a_year_at_its_middle():
    assert excess.position("2022") == 2022.0
    months = [excess.position(f"2022-{m:02d}") for m in range(1, 13)]
    assert sum(months) / 12 == pytest.approx(2022.0)


def test_a_word_that_already_rose_is_measured_against_its_line_not_its_level():
    # delve-like: doubles 2018->2022; at the trend's 2023 value it is no excess
    rising = word("rising", "pool", [1e-4, 1.25e-4, 1.5e-4, 1.75e-4, 2e-4],
                  "drifting-rising")
    m = excess.measure(rising, count=225, total=1_000_000, cohort="2023")
    assert m["expected"] == pytest.approx(2.25e-4)
    assert m["ratio"] == pytest.approx(1.0)
    flat_mean = sum(rising["shares"].values()) / 5
    assert 2.25e-4 / flat_mean > 1.4   # a level baseline would have counted it


def test_derived_list_threshold_order_cap_and_count_floor():
    flat = [1e-3] * 5
    words = [word("control", "controls", flat)]
    words += [word(f"w{i:02d}", "pool", flat) for i in range(25)]
    words += [word("thin", "pool", [1e-5] * 5), word("rare", "pool", flat, "rare")]
    counts = {"control": 1000, "thin": 49, "rare": 10_000}
    counts.update({f"w{i:02d}": 2000 + 10 * i for i in range(25)})
    r = excess.derive({"words": words}, counts, total=1_000_000, cohort="2024-05")
    assert r["control_breach"] == []
    assert r["derived"] == [f"w{i:02d}" for i in range(24, 4, -1)]   # 20, highest first
    assert "thin" not in r["derived"]      # ratio 4.9, but under MIN_COUNT
    assert {w["word"]: w["status"] for w in r["words"]}["rare"] == "rare"


def test_a_control_outside_its_band_marks_the_month():
    words = [word("control", "controls", [1e-3] * 5)]
    r = excess.derive({"words": words}, {"control": 1600}, 1_000_000, "2024")
    assert r["control_breach"] == ["control"]


def test_a_falling_word_whose_line_reaches_zero_is_not_extrapolated():
    falling = word("falling", "pool", [5e-5, 4e-5, 3e-5, 2e-5, 1e-5], "drifting-falling")
    assert excess.measure(falling, 100, 1_000_000, "2026-09")["status"] == "no_trend"


def test_wordlist_v2_replaces_only_the_stopword_control():
    v1, _, _ = wordlist.load(ROOT, "wordlist-v1")
    v2, _, _ = wordlist.load(ROOT, "wordlist-v2")
    assert v2["fixed"] == v1["fixed"] and v2["pool"] == v1["pool"]
    assert set(v1["controls"]) - set(v2["controls"]) == {"significantly"}
    assert set(v2["controls"]) - set(v1["controls"]) == {"reduced"}
    zero = [w for w in json.loads((ROOT / "syntheticflood/baseline/wordlist-v1.json")
                                  .read_text())["words"] if w["word"] == "significantly"]
    assert zero[0]["min_count"] == 0 and max(zero[0]["counts"].values()) == 0
