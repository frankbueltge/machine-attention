"""The Interval money series and t1: constructed flows, no network."""

import json
from pathlib import Path

import pytest

from practice.interval import money

REPO = Path(__file__).resolve().parents[2]


def flow(id, date, amount, *, status="paid", boundary="incoming",
         reported=None, version=1, flow_type="Standard"):
    return {"id": id, "versionId": version, "amountUSD": amount,
            "status": status, "boundary": boundary, "flowType": flow_type,
            "date": f"{date}-15T00:00:00Z",
            "firstReportedDate": f"{reported or date}-15T00:00:00Z"}


def page(*flows):
    return json.dumps({"data": {"flows": list(flows)}, "meta": {}})


def steady(t0, per_month=10, before=12):
    """One counted flow of `per_month` in each of the months before t0."""
    return [flow(f"b{i}", money.add_months(t0, -i), per_month)
            for i in range(1, before + 1)]


def test_window_and_boundary_years_are_a_comma_list():
    assert money.window("2022-03") == ("2021-03", "2023-02")
    assert money.boundary_years("2022-03") == "2021,2022,2023"
    # January 2011: the window spans 2010 and 2011, never a single year.
    assert money.boundary_years("2011-01") == "2010,2011"
    assert "-" not in money.boundary_years("2019-12")


def test_add_months_crosses_years():
    assert money.add_months("2022-11", 3) == "2023-02"
    assert money.add_months("2022-01", -1) == "2021-12"
    assert money.add_months("2022-01", -13) == "2020-12"


def test_only_incoming_paid_or_commitment_counts():
    flows = money.parse_flows([page(
        flow("1", "2022-03", 100),
        flow("2", "2022-03", 50, status="commitment", flow_type="Parked"),
        flow("3", "2022-03", 1000, status="pledge"),
        flow("4", "2022-03", 1000, boundary="internal"),
        flow("5", "2022-03", 1000, boundary="outgoing"))])
    m = money.money_series(flows, "date", "2022-03", "2022-03")
    assert m == {"2022-03": 150.0}


def test_duplicate_id_counts_once_at_highest_version():
    flows = money.parse_flows([page(flow("7", "2022-03", 10, version=1)),
                               page(flow("7", "2022-04", 30, version=2))])
    assert len(flows) == 1
    m = money.money_series(flows, "date", "2022-03", "2022-04")
    assert m == {"2022-03": 0.0, "2022-04": 30.0}


def test_two_time_axes_and_zero_months():
    flows = money.parse_flows([page(
        flow("1", "2022-01", 40, reported="2022-06"))])
    by_date = money.money_series(flows, "date", "2022-01", "2022-06")
    by_known = money.money_series(flows, "firstReportedDate", "2022-01",
                                  "2022-06")
    assert by_date["2022-01"] == 40 and by_date["2022-06"] == 0
    assert by_known["2022-01"] == 0 and by_known["2022-06"] == 40
    assert len(by_date) == 6
    with pytest.raises(ValueError):
        money.money_series(flows, "createdAt", "2022-01", "2022-06")


def test_t1_is_first_month_at_k_times_baseline_median():
    t0 = "2022-03"
    flows = money.parse_flows([page(
        *steady(t0),
        flow("a", "2022-03", 15),          # 1.5x: no response
        flow("b", "2022-05", 25),          # 2.5x: k=2 answers here
        flow("c", "2022-07", 35))])        # 3.5x: k=3 answers here
    r2 = money.response(flows, t0, 2, "date", as_of="2023-06")
    r3 = money.response(flows, t0, 3, "date", as_of="2023-06")
    assert r2.baseline == 10
    assert (r2.t1, r2.gap, r2.status) == ("2022-05", 2, "closed")
    assert (r3.t1, r3.gap, r3.status) == ("2022-07", 4, "closed")


def test_response_in_the_onset_month_is_gap_zero():
    t0 = "2023-06"
    flows = money.parse_flows([page(*steady(t0), flow("w", t0, 500))])
    r = money.response(flows, t0, 3, "date", as_of="2024-12")
    assert (r.t1, r.gap) == (t0, 0)


def test_known_axis_can_lag_the_moved_axis():
    t0 = "2022-03"
    flows = money.parse_flows([page(
        *steady(t0), flow("late", "2022-04", 100, reported="2022-09"))])
    # the baseline flows are reported in their own month on both axes
    moved = money.response(flows, t0, 2, "date", as_of="2023-06")
    known = money.response(flows, t0, 2, "firstReportedDate", as_of="2023-06")
    assert moved.gap == 1 and known.gap == 6


def test_open_clock_runs_to_as_of_not_the_wall_clock():
    t0 = "2026-01"
    flows = money.parse_flows([page(*steady(t0))])
    r = money.response(flows, t0, 2, "date", as_of="2026-09")
    assert (r.status, r.open_months, r.t1) == ("open", 8, None)
    assert r.half_month is None   # the horizon is not complete


def test_no_response_within_a_complete_horizon():
    t0 = "2022-03"
    flows = money.parse_flows([page(*steady(t0),
                                    *[flow(f"x{i}", money.add_months(t0, i),
                                           10) for i in range(12)])])
    r = money.response(flows, t0, 2, "date", as_of="2026-09")
    assert r.status == "none_in_horizon" and r.gap is None
    assert r.half_month == "2022-08"   # 60 of 120 reached in the sixth month


def test_zero_baseline_has_no_t1():
    t0 = "2022-03"
    flows = money.parse_flows([page(*steady(t0, before=5),
                                    flow("big", t0, 1000))])
    r = money.response(flows, t0, 2, "date", as_of="2026-09")
    assert (r.baseline, r.status, r.t1) == (0, "baseline_zero", None)
    assert r.half_month == t0


def test_grid_has_every_k_and_axis():
    t0 = "2022-03"
    flows = money.parse_flows([page(*steady(t0))])
    cells = money.grid(flows, t0, as_of="2026-09")
    assert {(c.k, c.axis) for c in cells} == {
        (k, a) for k in money.KS for a in money.AXES}


def test_committed_sudan_snapshot_counts_what_fts_counts():
    # 2026-10-09 snapshot, Sudan 2024 FSC: every incoming flow is paid or
    # commitment, as FTS's own flowCount says (175).
    base = REPO / "interval/snapshots/2026-10-09/fts/SDN"
    pages = [p.read_bytes() for p in sorted(base.glob("fsc-2024-p*.json"))]
    if not pages:
        pytest.skip("snapshot not present")
    flows = money.parse_flows(pages)
    incoming = [f for f in flows if money.counted(f)]
    assert len(incoming) == json.loads(pages[0])["data"]["incoming"][
        "flowCount"] == 175
