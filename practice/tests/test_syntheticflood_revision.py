"""Synthetic Flood V0 increment 3d: the revision between two readings of one
cohort, re-derived by the verifier from the readings it names (no network)."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

from practice.syntheticflood import cohort, pubmed, revision

_spec = importlib.util.spec_from_file_location(
    "sf_increment3_rev", Path(__file__).with_name("test_syntheticflood_baseline.py"))
_b = importlib.util.module_from_spec(_spec)
sys.modules["sf_increment3_rev"] = _b
_spec.loader.exec_module(_b)
client, write, verify, tiny_repo = _b.client, _b.write, _b.verify, _b.tiny_repo


def read(root, day, total, counts):
    answers = {None: pubmed.canonical(total)}
    answers.update({w: pubmed.canonical(c) for w, c in zip(_b.WORDS, counts)})
    write(root, cohort.read(root, "2026-09", day, "wordlist-v1", client(answers)))


def two_readings(tmp_path, later=(1100, (120, 990, 440, 20))):
    """delve, intricate, patients, pivotal; pivotal thin (< 50) at first."""
    root = tiny_repo(tmp_path)
    read(root, "2026-10-19", 1000, (100, 900, 400, 20))
    read(root, "2026-10-22", *later)
    return root


def run_verify(root):
    problems = _b.run_verify(root)
    verify.check_syntheticflood_revisions(root, problems)
    return problems


def write_revision(root):
    revision.main(["--repo-root", str(root), "--cohort", "2026-09",
                   "--earlier", "2026-10-19", "--later", "2026-10-22"])
    return revision.revision_path(root, "2026-09", "2026-10-19", "2026-10-22")


def test_drift_is_share_against_share_and_thin_words_are_not_judged():
    e = {"total": {"count": 1000}, "counts": [
        {"list": "fixed", "word": "a", "count": 100},
        {"list": "controls", "word": "b", "count": 400},
        {"list": "pool", "word": "c", "count": 49},
        {"list": "pool", "word": "only-earlier", "count": 300}]}
    l = {"total": {"count": 1100}, "counts": [
        {"list": "fixed", "word": "a", "count": 110},
        {"list": "controls", "word": "b", "count": 520},
        {"list": "pool", "word": "c", "count": 90}]}
    r = revision.compare(e, l)
    rows = {x["word"]: x for x in r["words"]}
    assert r["total"] == {"earlier": 1000, "later": 1100, "growth": 1.1}
    assert rows["a"]["drift"] == 1.0 and rows["a"]["status"] == "held"
    assert rows["b"]["drift"] == 1.1818 and rows["b"]["status"] == "moved"
    assert rows["c"]["status"] == "thin" and "drift" not in rows["c"]
    assert "only-earlier" not in rows and r["moved"] == ["b"]


def test_revision_file_names_its_readings_and_verifies(tmp_path):
    root = two_readings(tmp_path)
    d = json.loads(write_revision(root).read_text())
    assert d["earlier"]["file"] == "syntheticflood/readings/2026-09/2026-10-19.json"
    assert d["later"]["wordlist"] == "wordlist-v1" and d["rule"]["id"] == "revision-v1"
    assert d["moved"] == []
    assert run_verify(root) == []


def test_a_changed_drift_is_caught(tmp_path):
    root = two_readings(tmp_path)
    path = write_revision(root)
    d = json.loads(path.read_text())
    d["words"][0]["drift"] = 1.5
    path.write_text(json.dumps(d))
    assert any("drift" in p for p in run_verify(root))


def test_a_rule_changed_under_its_id_is_caught(tmp_path):
    root = two_readings(tmp_path)
    path = write_revision(root)
    d = json.loads(path.read_text())
    d["rule"]["band"] = 1.5
    path.write_text(json.dumps(d))
    assert any("rule changed" in p for p in run_verify(root))


def test_a_reading_changed_after_the_revision_is_caught(tmp_path):
    root = two_readings(tmp_path)
    write_revision(root)
    rpath = cohort.reading_path(root, "2026-09", "2026-10-22")
    rpath.write_text(rpath.read_text() + "\n")
    assert any("later reading" in p for p in run_verify(root))


def test_order_and_baseline_years_are_refused(tmp_path):
    root = two_readings(tmp_path)
    with pytest.raises(ValueError):
        revision.build(root, "2026-09", "2026-10-22", "2026-10-19")
    with pytest.raises(ValueError):
        revision.build(root, "2020", "2026-10-19", "2026-10-22")
