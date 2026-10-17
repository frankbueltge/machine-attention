"""The Interval E-experiment: the tally counts what readings show, and
verify.py holds the committed criteria to their window."""

import json
from pathlib import Path

from practice.interval import experiment, money, sources
from practice.preserve import sha256, write_json

from .test_interval_register import verifier

REPO = Path(__file__).resolve().parents[2]
WEEKS = ["2026-10-19", "2026-10-26", "2026-11-02", "2026-11-09"]


def reading(day, frozen_basis="2026-10-12", outcome="unchanged", ipc="unchanged",
            http_429=0, extra=()):
    queries = [{"country": "AFG", "t0": "2021-10", "set": "fsc",
                "decision": "frozen", "basis_day": frozen_basis},
               {"country": "SOM", "t0": "2026-01", "set": "total",
                "decision": "fetch", "basis_day": "2026-10-12",
                "outcome": outcome}]
    queries += [{"country": c, "t0": t, "set": "fsc", "decision": "fetch",
                 "basis_day": None, "outcome": "preserved"} for c, t in extra]
    return {"date": day, "ipc": {"status": ipc}, "queries": queries,
            "http_429": http_429, "episodes": 2 + len(extra)}


def plan():
    return {"window": {"weeks": WEEKS, "closes": "2026-11-15"},
            "criteria": {"A2_max_failed_readings": 1}}


def test_a_clean_window_tallies_clean():
    rs = [reading("2026-10-13")] + [reading(w) for w in WEEKS]
    out = experiment.tally(plan(), rs, "2026-11-16")
    assert out["closed"] and out["weeks_due"] == 4
    assert out["A1_missing_weeks"] == [] and out["A2_pass"]
    assert out["A3_http_429"] == [] and out["B1_frozen_moves"] == []
    assert out["B2_episode_changes"] == []


def test_gap_failures_throttle_and_new_episode_are_counted():
    rs = [reading("2026-10-13"), reading("2026-10-21", outcome="incomplete"),
          reading("2026-11-02", ipc="unavailable", http_429=2,
                  extra=[("NGA", "2026-03")])]
    out = experiment.tally(plan(), rs, "2026-11-10")
    assert out["A1_missing_weeks"] == ["2026-10-26", "2026-11-09"]
    assert sorted(out["A2_readings_with_failures"]) == ["2026-10-21",
                                                        "2026-11-02"]
    assert not out["A2_pass"]
    assert out["A3_http_429"] == ["2026-11-02"]
    assert out["B2_episode_changes"] == ["2026-11-02: + NGA 2026-03"]


def test_a_frozen_query_that_moves_is_caught():
    rs = [reading("2026-10-13"), reading("2026-10-19"),
          reading("2026-10-26", frozen_basis="2026-10-26")]
    moves = experiment.tally(plan(), rs, "2026-10-27")["B1_frozen_moves"]
    assert moves == ["2026-10-26: AFG 2021-10 fsc frozen on 2026-10-12, "
                     "now frozen on 2026-10-26"]


def test_sources_never_name_the_fews_net_warehouse():
    text = Path(sources.__file__).read_text(encoding="utf-8")
    assert "fews.net" not in text.lower()


def committed_tree(tmp_path, **override):
    doc = tmp_path / "docs" / "k.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("criteria\n", encoding="utf-8")
    write_json(tmp_path / "interval" / "readings" / "2026-10-13.json", {})
    e = {"schema": "interval-experiment-v1", "committed": "2026-10-14",
         "document": "docs/k.md", "document_sha256": sha256(doc.read_bytes()),
         "pre_window_readings": ["2026-10-13"],
         "window": {"weeks": WEEKS, "closes": "2026-11-15",
                    "review_from": "2026-11-16"},
         "criteria": {"A1_weeks_required": 4}}
    e.update(override)
    write_json(tmp_path / experiment.EXPERIMENT, e)
    return tmp_path


def check(root):
    problems = []
    verifier().check_interval_experiment(root, problems)
    return problems


def test_verify_accepts_criteria_committed_before_the_window(tmp_path):
    assert check(committed_tree(tmp_path)) == []


def test_verify_rejects_late_criteria_and_edited_prose(tmp_path):
    root = committed_tree(tmp_path, committed="2026-10-19")
    (root / "docs" / "k.md").write_text("criteria, softened\n", encoding="utf-8")
    problems = check(root)
    assert any("not before the window" in p for p in problems)
    assert any("changed without its hash" in p for p in problems)


def test_verify_rejects_a_short_or_gapped_window(tmp_path):
    root = committed_tree(tmp_path, window={
        "weeks": ["2026-10-19", "2026-10-26", "2026-11-09"],
        "closes": "2026-11-15", "review_from": "2026-11-16"})
    assert any("consecutive Mondays" in p for p in check(root))


def test_the_committed_experiment_is_clean():
    assert check(REPO) == []
    e = json.loads((REPO / experiment.EXPERIMENT).read_text(encoding="utf-8"))
    assert e["window"]["weeks"] == WEEKS


def test_verify_holds_an_addendum_to_its_date_and_hash(tmp_path):
    def tree(base, day, text):
        root = committed_tree(base)
        add = root / "docs" / "n.md"
        add.write_text("addendum\n", encoding="utf-8")
        e = json.loads((root / experiment.EXPERIMENT).read_text(encoding="utf-8"))
        e["addenda"] = [{"date": day, "document": "docs/n.md",
                         "document_sha256": sha256(add.read_bytes())}]
        write_json(root / experiment.EXPERIMENT, e)
        add.write_text(text, encoding="utf-8")
        return root
    assert check(tree(tmp_path / "ok", "2026-10-17", "addendum\n")) == []
    problems = check(tree(tmp_path / "late", "2026-10-19",
                          "addendum, softened\n"))
    assert any("not between the criteria and the window" in p
               for p in problems)
    assert any("changed without its hash" in p for p in problems)


def flow_page(flows):
    return {"data": {"flows": [
        {"id": str(i), "versionId": 1, "amountUSD": amt, "status": "paid",
         "boundary": "incoming", "flowType": "Standard", "date": f"{m}-15",
         "firstReportedDate": f"{m}-15"} for i, (m, amt) in enumerate(flows)]}}


def test_base_rate_counts_placebo_months_against_the_onset(tmp_path):
    # 10 a month in 2020 and 2022, 100 a month in 2021. A month of 2021
    # closes at once while at least seven of its twelve baseline months are
    # 2020's tens (median 10): 2021-01 to 2021-06, the onset among them.
    flows = [(f"2020-{m:02d}", 10.0) for m in range(1, 13)]
    flows += [(f"2021-{m:02d}", 100.0) for m in range(1, 13)]
    flows += [(f"2022-{m:02d}", 10.0) for m in range(1, 13)]
    page = tmp_path / "p.json"
    write_json(page, flow_page(flows))
    side = {"status": "read", "boundary_years": "2020,2021,2022",
            "as_of": "2026-10", "pages": ["p.json"]}
    short = {"status": "read", "boundary_years": "2025,2026",
             "as_of": "2026-10", "pages": ["p.json"]}
    register = {"episodes": [
        {"t0": "2021-06", "money": {"fsc": side}},
        {"t0": "2026-01", "money": {"fsc": short}}]}
    out = experiment.base_rate(tmp_path, register)
    assert out["max_gap_months"] == 1
    assert len(out["cells"]) == len(money.AXES) * len(money.KS)
    c = out["cells"]["fsc date k=2"]
    assert (c["onset_short"], c["onset_n"]) == (1, 1)
    assert c["placebo_n"] == 11
    assert c["placebo_short"] == 5


def test_the_committed_experiment_reports_b6():
    e = json.loads((REPO / experiment.EXPERIMENT).read_text(encoding="utf-8"))
    assert "B6" in e["reported"]
    assert [a["date"] for a in e["addenda"]] == ["2026-10-17"]
