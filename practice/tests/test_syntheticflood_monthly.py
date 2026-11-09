"""Synthetic Flood V0 increment 4: the monthly run reads each month cohort once
at M+1, M+2 and M+3 on the current word list, derives and revises from the
committed files, never repeats a request, and its workflow runs it through the
shared handshake (no network)."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from practice.syntheticflood import monthly, pubmed

_spec = importlib.util.spec_from_file_location(
    "sf_increment3c", Path(__file__).with_name("test_syntheticflood_derived.py"))
_d = importlib.util.module_from_spec(_spec)
sys.modules["sf_increment3c"] = _d
_spec.loader.exec_module(_d)
_b = _d._b

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "syntheticflood.yml"
V = "wordlist-v1"


def answers(total=1500, counts=(120, 900, 440, 200)):
    a = {None: pubmed.canonical(total)}
    a.update({w: pubmed.canonical(c) for w, c in zip(_b.WORDS, counts)})
    return a


def run_verify(root):
    problems = _d.run_verify(root)
    _b.verify.check_syntheticflood_revisions(root, problems)
    return problems


def test_month_minus_crosses_the_year():
    assert monthly.month_minus("2026-11-09", 1) == "2026-10"
    assert monthly.month_minus("2027-01-03", 3) == "2026-10"
    assert monthly.month_minus("2027-01-03", 1) == "2026-12"


def test_due_tonight_on_the_committed_tree():
    """On the committed record: 2026-09 has its M+2 on wordlist-v3
    (2026-11-08), 2026-08 lies before the first cohort, so only 2026-10 at
    M+1 is due in November; in December all three lags fall due."""
    assert monthly.due(ROOT, "2026-11-09") in (["2026-10"], [])
    assert monthly.due(ROOT, "2026-12-03")[:1] == ["2026-09"]


def test_due_skips_baseline_years_and_cohorts_before_the_first(tmp_path):
    root = _b.year_repo(tmp_path)
    assert monthly.due(root, "2026-10-21", V) == ["2026-09"]
    assert monthly.due(root, "2026-12-01", V) == ["2026-09", "2026-10", "2026-11"]


def test_first_run_reads_and_derives_and_verifies(tmp_path):
    root = _b.year_repo(tmp_path)
    _b.baseline.main(["--repo-root", str(root)])
    done = monthly.run(root, "2026-10-22", V, client=_b.client(answers()))
    assert [r["cohort"] for r in done] == ["2026-09"]
    assert done[0]["lag_months"] == 1 and done[0]["missing"] == 0
    assert done[0]["files"] == ["syntheticflood/readings/2026-09/2026-10-22.json",
                                "syntheticflood/derived/2026-09/2026-10-22.json"]
    assert run_verify(root) == []


def test_a_second_run_in_the_same_month_asks_nothing(tmp_path):
    root = _b.year_repo(tmp_path)
    _b.baseline.main(["--repo-root", str(root)])
    monthly.run(root, "2026-10-22", V, client=_b.client(answers()))
    c = _b.client(answers())
    assert monthly.run(root, "2026-10-29", V, client=c) == []
    assert c.requests == 0


def test_next_month_revises_against_the_earlier_reading(tmp_path):
    root = _b.year_repo(tmp_path)
    _b.baseline.main(["--repo-root", str(root)])
    monthly.run(root, "2026-10-22", V, client=_b.client(answers()))
    done = monthly.run(root, "2026-11-03", V,
                       client=_b.client(answers(1530, (122, 918, 449, 204))))
    assert [r["cohort"] for r in done] == ["2026-09", "2026-10"]
    rev = "syntheticflood/revisions/2026-09/2026-10-22_2026-11-03.json"
    assert rev in done[0]["files"]
    assert json.loads((root / rev).read_text())["earlier"]["lag_months"] == 1
    assert run_verify(root) == []


def test_an_incomplete_reading_is_kept_not_derived_and_not_repeated(tmp_path):
    root = _b.year_repo(tmp_path)
    _b.baseline.main(["--repo-root", str(root)])
    broken = answers()
    broken["intricate"] = b'{"esearchresult":{"ERROR":"busy"}}'
    done = monthly.run(root, "2026-10-22", V, client=_b.client(broken))
    assert done[0]["missing"] == 1 and len(done[0]["files"]) == 1
    assert not (root / "syntheticflood/derived/2026-09/2026-10-22.json").exists()
    assert monthly.due(root, "2026-10-30", V) == []


def test_workflow_runs_the_monthly_reading_and_the_handshake():
    text = WORKFLOW.read_text(encoding="utf-8")
    steps = ["pip install --quiet -e ./practice",
             "python -m practice.syntheticflood.monthly --repo-root .",
             "python tools/anchor.py --register",
             "python verify.py --repo-root .",
             "tools/commit-and-push.sh"]
    positions = [text.index(s) for s in steps]
    assert positions == sorted(positions), "install, read, register, verify, commit"
    assert 'cron: "' in text and "workflow_dispatch" in text


def test_workflow_is_admitted_only_after_a_reading_by_its_command():
    """The admission path: a workflow only once V0 has a committed reading made
    by the command the job runs."""
    lines = [json.loads(l) for l in
             (ROOT / "autonomy" / "log.jsonl").read_text(encoding="utf-8").splitlines() if l]
    runs = [l for l in lines if l["step"] == "syntheticflood-monthly"
            and any(c["missing"] == 0 for c in l["detail"]["cohorts"])]
    assert runs, "no committed monthly run yet"
    for c in runs[0]["detail"]["cohorts"]:
        for f in c["files"]:
            assert (ROOT / f).exists(), f
