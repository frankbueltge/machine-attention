"""Synthetic Flood V0 increment 3: year cohorts and the stability test of a
word list against 2018–2022 (no network), and the verifier proven to bite."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from practice.syntheticflood import baseline, cohort, pubmed

# The increment-1 helpers (fake opener, tiny repo, verifier) are reused as they are.
_spec = importlib.util.spec_from_file_location(
    "sf_increment1", Path(__file__).with_name("test_syntheticflood.py"))
_sf = importlib.util.module_from_spec(_spec)
sys.modules["sf_increment1"] = _sf
_spec.loader.exec_module(_sf)
client, tiny_repo, verify, write = _sf.client, _sf.tiny_repo, _sf.verify, _sf.write

# Shares per year: delve stable, intricate rising, patients stable, pivotal rare.
COUNTS = {"2018": (1000, 100, 50, 300, 10), "2019": (1100, 110, 60, 320, 10),
          "2020": (1200, 115, 80, 360, 12), "2021": (1300, 125, 100, 390, 30),
          "2022": (1400, 140, 140, 420, 60)}
WORDS = ("delve", "intricate", "patients", "pivotal")


def year_repo(tmp_path):
    root = tiny_repo(tmp_path)
    for year, (total, *counts) in COUNTS.items():
        answers = {None: pubmed.canonical(total)}
        answers.update({w: pubmed.canonical(c) for w, c in zip(WORDS, counts)})
        write(root, cohort.read(root, year, "2026-10-21", "wordlist-v1", client(answers)))
    return root


def run_verify(root):
    problems: list[str] = []
    registry: dict = {}
    verify.check_snapshots(root, verify.SF_SNAP, problems, registry, False)
    verify.check_syntheticflood(root, registry, problems)
    verify.check_syntheticflood_baseline(root, problems)
    return problems


def test_year_term_and_lag():
    assert pubmed.cohort_term("2019") == "hasabstract AND 2019[dp]"
    assert pubmed.cohort_term("2019", "delve") == "delve[tiab] AND hasabstract AND 2019[dp]"
    assert cohort.lag("2022", "2026-10-21") == 46
    assert cohort.lag("2026", "2026-10-21") < 1


def test_year_reading_verifies_as_retrospective(tmp_path):
    root = year_repo(tmp_path)
    r = json.loads(cohort.reading_path(root, "2018", "2026-10-21").read_text())
    assert r["retrospective"] is True and r["value"] is False
    assert run_verify(root) == []


def test_verdicts(tmp_path):
    root = year_repo(tmp_path)
    b = baseline.derive(root, "wordlist-v1")
    got = {w["word"]: w["verdict"] for w in b["words"]}
    assert got == {"delve": "stable", "intricate": "drifting-rising",
                   "patients": "stable", "pivotal": "rare"}
    assert b["tally"] == {"controls": {"stable": 1}, "fixed": {"drifting-rising": 1,
                          "stable": 1}, "pool": {"rare": 1}}
    baseline.main(["--repo-root", str(root)])
    assert run_verify(root) == []


def test_missing_year_is_refused(tmp_path):
    root = year_repo(tmp_path)
    for p in (root / "syntheticflood/readings/2020").glob("*.json"):
        p.unlink()
    with pytest.raises(ValueError):
        baseline.derive(root, "wordlist-v1")


@pytest.fixture
def derived(tmp_path):
    root = year_repo(tmp_path)
    baseline.main(["--repo-root", str(root)])
    path = baseline.baseline_path(root, "wordlist-v1")
    return root, path, json.loads(path.read_text())


def bites(root, path, doc, needle):
    path.write_text(json.dumps(doc))
    problems = run_verify(root)
    assert any(needle in p for p in problems), problems


def test_changed_verdict_is_caught(derived):
    root, path, doc = derived
    doc["words"][1]["verdict"] = "stable"
    bites(root, path, doc, "differs from the readings")


def test_rule_changed_under_its_id_is_caught(derived):
    root, path, doc = derived
    doc["rule"]["max_ratio"] = 3.0
    bites(root, path, doc, "rule changed under its id")


def test_older_reading_is_caught(derived):
    root, path, doc = derived
    newer = cohort.reading_path(root, "2019", "2026-10-22")
    newer.write_text(cohort.reading_path(root, "2019", "2026-10-21").read_text()
                     .replace('"date": "2026-10-21"', '"date": "2026-10-22"'))
    bites(root, path, doc, "not the newest committed year reading")


def test_changed_tally_is_caught(derived):
    root, path, doc = derived
    doc["tally"]["pool"] = {"stable": 1}
    bites(root, path, doc, "tally differs")
