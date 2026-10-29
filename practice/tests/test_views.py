"""views.build() recomputes the rows of the house's figures from committed
records with the projects' own code. Checked against this repository's own
records, so a change in a reading or register shape that the figures would
silently misdraw fails here first."""

from pathlib import Path

from practice import views
from practice.interval import money

ROOT = Path(__file__).resolve().parents[2]


def test_every_planetary_night_is_carried_with_decoded_excerpts():
    nights = views.planetary(ROOT)
    readings = sorted((ROOT / "planetary" / "readings").glob("*.json"))
    assert len(nights) == len(readings)
    for n in nights:
        assert len(n["excerpts"]) <= 4
        for ex in n["excerpts"]:
            env = ex["envelope"]
            assert env is not None
            assert len(env["min"]) == len(env["max"]) == views.ENVELOPE_BINS
            assert all(lo <= hi for lo, hi in zip(env["min"], env["max"]))


def test_interval_money_matches_the_register_t1():
    for e in views.interval(ROOT):
        start, end = e["window"]
        for name, s in e["money"].items():
            assert list(s["series"]) == [money.add_months(start, i)
                                         for i in range(len(s["series"]))]
            assert list(s["series"])[-1] == end
            if s["status"] == "closed":
                # t1 is the first month from t0 on whose money reaches 2x the baseline
                after = [m for m in s["series"] if m >= e["t0"]]
                first = next(m for m in after if s["series"][m] >= 2 * s["baseline_usd"] - 1)
                assert first == s["t1"]


def test_envelope_refuses_an_excerpt_shorter_than_its_bins():
    assert views.envelope(b"") is None
