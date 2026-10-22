"""Synthetic Flood V0 increment 3c: the derived list as a file, re-derived by
the verifier from the reading and baseline it names (no network)."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from practice.syntheticflood import baseline, cohort, derived, pubmed

_spec = importlib.util.spec_from_file_location(
    "sf_increment3", Path(__file__).with_name("test_syntheticflood_baseline.py"))
_b = importlib.util.module_from_spec(_spec)
sys.modules["sf_increment3"] = _b
_spec.loader.exec_module(_b)
client, write, verify, year_repo = _b.client, _b.write, _b.verify, _b.year_repo


def month_repo(tmp_path, counts=(1500, 120, 900, 440, 200)):
    """Baseline years from the increment-3 fixture, then one month cohort:
    total, delve, intricate, patients (control), pivotal (pool, rare)."""
    root = year_repo(tmp_path)
    baseline.main(["--repo-root", str(root)])
    total, *rest = counts
    answers = {None: pubmed.canonical(total)}
    answers.update({w: pubmed.canonical(c) for w, c in zip(_b.WORDS, rest)})
    write(root, cohort.read(root, "2026-09", "2026-10-22", "wordlist-v1", client(answers)))
    return root


def run_verify(root):
    problems = _b.run_verify(root)
    verify.check_syntheticflood_derived(root, problems)
    return problems


def write_derived(root):
    derived.main(["--repo-root", str(root), "--cohort", "2026-09",
                  "--date", "2026-10-22", "--wordlist", "wordlist-v1"])
    return derived.derived_path(root, "2026-09", "2026-10-22")


def test_derived_file_names_its_inputs_and_verifies(tmp_path):
    root = month_repo(tmp_path)
    path = write_derived(root)
    d = json.loads(path.read_text())
    assert d["reading"]["file"] == "syntheticflood/readings/2026-09/2026-10-22.json"
    assert d["baseline"]["file"] == "syntheticflood/baseline/wordlist-v1.json"
    assert d["rule"]["id"] == "excess-v1" and d["value"] is False
    assert {w["word"]: w["status"] for w in d["words"]}["pivotal"] == "rare"
    assert run_verify(root) == []


def test_a_changed_ratio_is_caught(tmp_path):
    root = month_repo(tmp_path)
    path = write_derived(root)
    d = json.loads(path.read_text())
    row = next(w for w in d["words"] if w["status"] == "measured")
    row["ratio"] = round(row["ratio"] + 0.5, 4)
    path.write_text(json.dumps(d))
    assert any("words differ" in p for p in run_verify(root))


def test_a_list_entry_not_earned_is_caught(tmp_path):
    root = month_repo(tmp_path)
    path = write_derived(root)
    d = json.loads(path.read_text())
    d["derived"] = ["pivotal"]
    path.write_text(json.dumps(d))
    assert any("derived list" in p for p in run_verify(root))


def test_a_rule_parameter_changed_under_its_id_is_caught(tmp_path):
    root = month_repo(tmp_path)
    path = write_derived(root)
    d = json.loads(path.read_text())
    d["rule"]["min_ratio"] = 1.5
    path.write_text(json.dumps(d))
    assert any("rule changed" in p for p in run_verify(root))


def test_an_edited_reading_breaks_the_hash(tmp_path):
    root = month_repo(tmp_path)
    write_derived(root)
    rpath = cohort.reading_path(root, "2026-09", "2026-10-22")
    rpath.write_text(rpath.read_text().replace('"2026-09"', '"2026-09" '))
    assert any("reading missing, changed" in p for p in run_verify(root))


def test_control_breach_is_reported(tmp_path):
    # patients far above its stable ~30 % line
    root = month_repo(tmp_path, counts=(1500, 120, 900, 1400, 200))
    d = json.loads(write_derived(root).read_text())
    assert d["control_breach"] == ["patients"]
    assert run_verify(root) == []


def test_a_baseline_year_or_an_incomplete_reading_is_refused(tmp_path):
    root = month_repo(tmp_path)
    with pytest.raises(ValueError):
        derived.build(root, "2020", "2026-10-21", "wordlist-v1")
    rpath = cohort.reading_path(root, "2026-09", "2026-10-22")
    r = json.loads(rpath.read_text())
    r["counts"][0]["count"] = None
    rpath.write_text(json.dumps(r))
    with pytest.raises(ValueError):
        derived.build(root, "2026-09", "2026-10-22", "wordlist-v1")
