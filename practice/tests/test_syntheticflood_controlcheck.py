"""Register A, rule control-check-v1. Pure, no network."""

import json
from pathlib import Path

import pytest

from practice.syntheticflood import controlcheck, wordlist

ROOT = Path(__file__).resolve().parents[2]
BASE = ("2018", "2019", "2020", "2021", "2022")


def entry(word, shares, verdict="stable"):
    return {"word": word, "verdict": verdict, "shares": dict(zip(BASE, shares))}


def flat_counts(share, total=1_000_000):
    return ({y: round(share * total) for y in controlcheck.CHECK_YEARS},
            {y: total for y in controlcheck.CHECK_YEARS})


def test_the_committed_reduced_counts_fail_the_check_but_pass_the_use_band():
    # baseline entry and the six probe counts of 2026-11-03, all committed
    base = json.loads((ROOT / "syntheticflood/baseline/wordlist-v2.json").read_text())
    reduced = next(w for w in base["words"] if w["word"] == "reduced")
    probes = ROOT / "syntheticflood/probes/2026-11-03/pubmed"
    read = lambda f: int(json.loads((probes / f).read_text())["esearchresult"]["count"])
    counts = {y: read(f"{y}-reduced.json") for y in controlcheck.CHECK_YEARS}
    totals = {y: read(f"{y}-cohort.json") for y in controlcheck.CHECK_YEARS}
    r = controlcheck.check(reduced, counts, totals)
    ratios = [r["years"][y]["ratio"] for y in controlcheck.CHECK_YEARS]
    assert ratios == pytest.approx([1.0247, 1.1266, 1.4445], abs=1e-4)
    assert r["pass"] is False and r["reason"] == "outside_band"
    assert all(1 / 1.5 <= x <= 1.5 for x in ratios)   # excess-v1's band would pass it


def test_a_word_on_its_line_passes_and_a_rising_line_is_followed():
    rising = entry("rising", [0.10, 0.11, 0.12, 0.13, 0.14])
    counts = {"2023": 150_000, "2024": 160_000, "2025": 170_000}
    totals = {y: 1_000_000 for y in counts}
    r = controlcheck.check(rising, counts, totals)
    assert r["pass"] is True
    assert [r["years"][y]["ratio"] for y in counts] == pytest.approx([1.0, 1.0, 1.0])


@pytest.mark.parametrize("share, reason", [(0.0125, "outside_band"),
                                           (0.0079, "outside_band"),
                                           (0.00004, "rare")])
def test_band_and_floor(share, reason):
    w = entry("w", [0.01] * 5) if reason != "rare" else entry("w", [0.00004] * 5)
    r = controlcheck.check(w, *flat_counts(share))
    assert r["pass"] is False and r["reason"] == reason


def test_unread_years_and_unstable_baselines_never_pass():
    w = entry("w", [0.01] * 5)
    counts, totals = flat_counts(0.01)
    del counts["2024"]
    assert controlcheck.check(w, counts, totals)["reason"] == "unread"
    drifting = entry("d", [0.01, 0.012, 0.014, 0.016, 0.018], "drifting-rising")
    assert controlcheck.check(drifting, *flat_counts(0.02))["reason"] == "baseline_not_stable"


def test_compose_keeps_order_strikes_reduced_and_fills_from_candidates():
    controls = [f"c{i:02d}" for i in range(19)] + ["reduced"]
    results = {c: {"pass": True} for c in controls}
    results["c03"] = {"pass": False}
    results["samples"] = {"pass": False}
    results["groups"] = {"pass": True}
    results["cases"] = {"pass": True}
    results["performed"] = {"pass": True}
    r = controlcheck.compose(controls, results)
    assert r["struck"] == ["reduced"] and r["dropped"] == ["c03"]
    assert r["added"] == ["groups", "cases"]          # back to 20, in committed order
    assert len(r["controls"]) == 20 and r["controls"][:3] == ["c00", "c01", "c02"]


def test_compose_refuses_a_list_that_is_too_short():
    controls = [f"c{i:02d}" for i in range(20)]
    results = {c: {"pass": i < 10} for i, c in enumerate(controls)}
    r = controlcheck.compose(controls, results)
    assert r["controls"] is None and len(r["kept"]) == 10


def test_candidates_are_valid_words_on_no_list_of_wordlist_v2():
    doc, _, _ = wordlist.load(ROOT, "wordlist-v2")
    on_lists = {w for _, w in wordlist.terms(doc)}
    probe = {**doc, "controls": list(controlcheck.CANDIDATES)}
    probe["fixed"] = [w for w in doc["fixed"]]
    assert not set(controlcheck.CANDIDATES) & on_lists
    assert wordlist.validate(probe) == []
    assert set(controlcheck.STRUCK) <= set(doc["controls"])
