"""The Interval warning series and t0: constructed tables, no network."""

import pytest

from practice.interval import warning

HEADER = ("Date of analysis,Country,Total country population,Validity period,"
          "From,To,Phase,Number,Percentage\n")


def block(date, country, period, analysed, p4, p5, pop=1000):
    rows = [("all", analysed), ("3+", p4 + p5), ("1", 0), ("2", 0),
            ("3", 0), ("4", p4), ("5", p5)]
    return "".join(f"{date},{country},{pop},{period},2020-01-01,2020-02-01,"
                   f"{ph},{n},0\n" for ph, n in rows)


def series_of(*ws, country="XXX", start=(2021, 1), step=3):
    """Points with the given W, one analysis every `step` months."""
    y, m = start
    out = []
    for w in ws:
        out.append(warning.Point(country, f"{y:04d}-{m:02d}", w, w, None,
                                 False, 1.0, 1))
        m += step
        y, m = y + (m - 1) // 12, (m - 1) % 12 + 1
    return out


def test_analysis_month_and_distance():
    assert warning.analysis_month("Oct 2025") == "2025-10"
    assert warning.months_between("2024-11", "2025-05") == 6


def test_share_is_against_country_population_not_analysed():
    text = HEADER + block("Jan 2026", "SDN", "first projection", 200, 40, 2)
    (p,) = warning.warning_series(warning.parse_blocks(text), "SDN")
    assert p.w == pytest.approx(42 / 1000)
    assert p.coverage == pytest.approx(0.2)
    assert p.phase5_projected


def test_w_is_max_of_projections_and_current_is_ignored():
    text = HEADER + (block("Jan 2026", "A", "current", 1000, 900, 0)
                     + block("Jan 2026", "A", "first projection", 1000, 30, 0)
                     + block("Jan 2026", "A", "second projection", 1000, 80, 0))
    (p,) = warning.warning_series(warning.parse_blocks(text), "A")
    assert (p.w_first, p.w_second, p.w) == (0.03, 0.08, 0.08)


def test_analysis_without_projection_has_no_w():
    text = HEADER + block("Jan 2026", "A", "current", 1000, 900, 0)
    (p,) = warning.warning_series(warning.parse_blocks(text), "A")
    assert p.w is None and not p.phase5_projected


def test_duplicate_blocks_are_not_summed_largest_kept():
    text = HEADER + (block("May 2021", "ETH", "first projection", 500, 40, 5)
                     + block("May 2021", "ETH", "first projection", 90, 30, 5))
    (p,) = warning.warning_series(warning.parse_blocks(text), "ETH")
    assert p.w == pytest.approx(45 / 1000)
    assert p.blocks == 2


def test_onset_after_six_quiet_months():
    s = series_of(0.01, 0.02, 0.03, 0.12)       # below Jan..Jul, above Oct
    assert warning.onsets(s, 0.10) == ["2021-10"]
    assert not warning.left_censored(s, 0.10)


def test_short_quiet_run_is_no_new_onset():
    s = series_of(0.01, 0.01, 0.01, 0.12, 0.04, 0.12)   # dip of 3 months
    assert warning.onsets(s, 0.10) == ["2021-10"]


def test_quiet_run_too_short_from_series_start():
    s = series_of(0.01, 0.12)                   # only 3 months below
    assert warning.onsets(s, 0.10) == []


def test_chronic_phase4_triggers_no_onset():
    s = series_of(0.30, 0.28, 0.31, 0.27, 0.33, 0.29, 0.30, 0.32)
    for theta in warning.THETAS:
        assert warning.onsets(s, theta) == []
        assert warning.left_censored(s, theta)


def test_points_without_w_are_neither_above_nor_below():
    s = series_of(0.01, None, None, 0.12, step=2)   # Jan below, Jul above
    assert warning.onsets(s, 0.10) == ["2021-07"]


def test_two_episodes_after_recovery():
    s = series_of(0.01, 0.01, 0.01, 0.20, 0.01, 0.01, 0.01, 0.20)
    assert warning.onsets(s, 0.10) == ["2021-10", "2022-10"]


def test_phase_row_before_all_is_an_error():
    with pytest.raises(ValueError):
        warning.parse_blocks(HEADER + "Jan 2026,A,1,current,x,y,4,1,0\n")
