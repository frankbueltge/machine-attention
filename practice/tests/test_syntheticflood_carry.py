"""Synthetic Flood: the baseline of wordlist-v3 under baseline-carry-v1
(2026-11-07) — composed from committed counts only, re-derived, and the
verifier proven to bite."""
from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest

from practice.syntheticflood import baseline, carry

REPO = Path(__file__).resolve().parents[2]
CHECK = "syntheticflood/controlcheck/2026-11-06.json"
V3 = REPO / "syntheticflood/baseline/wordlist-v3.json"


def load_verify():
    spec = importlib.util.spec_from_file_location("verifymod_sfcarry", REPO / "verify.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verifymod_sfcarry"] = mod
    spec.loader.exec_module(mod)
    return mod


verify = load_verify()


def committed() -> dict:
    return json.loads(V3.read_text(encoding="utf-8"))


def run_verify(root: Path) -> list[str]:
    problems: list[str] = []
    verify.check_syntheticflood_baseline(root, problems)
    return [p for p in problems if "wordlist-v3" in p]


def tree(tmp_path) -> Path:
    for sub in ("wordlists", "baseline", "controlcheck"):
        shutil.copytree(REPO / "syntheticflood" / sub, tmp_path / "syntheticflood" / sub)
    for year in baseline.YEARS:
        shutil.copytree(REPO / "syntheticflood/readings" / year,
                        tmp_path / "syntheticflood/readings" / year)
    return tmp_path


def test_the_committed_baseline_re_derives_without_a_request():
    assert carry.derive(REPO, "wordlist-v3", "wordlist-v2", CHECK) == committed()


def test_carried_words_keep_their_predecessor_entry_exactly():
    v2 = {w["word"]: w for w in json.loads(
        (REPO / "syntheticflood/baseline/wordlist-v2.json").read_text())["words"]}
    for w in committed()["words"]:
        if w["source"] == "carried":
            old = {k: v for k, v in v2[w["word"]].items()}
            assert {k: v for k, v in w.items() if k != "source"} == old


def test_added_words_are_the_control_checks_candidate_baseline():
    rec = json.loads((REPO / CHECK).read_text())
    added = [w for w in committed()["words"] if w["source"] == "added"]
    assert [w["word"] for w in added] == ["samples", "groups", "cases", "performed"]
    for w in added:
        cb = rec["candidate_baseline"][w["word"]]
        assert (w["shares"], w["ratio"], w["verdict"]) == (cb["shares"], cb["ratio"], cb["verdict"])
        assert w["list"] == "controls"


def test_every_control_of_v3_is_stable_on_2018_2022():
    assert committed()["tally"]["controls"] == {"stable": 20}


def test_a_word_in_neither_source_refuses_the_baseline(tmp_path):
    root = tree(tmp_path)
    w = root / "syntheticflood/wordlists/wordlist-v3.json"
    d = json.loads(w.read_text())
    d["pool"].append("unseenword")
    w.write_text(json.dumps(d))
    with pytest.raises(ValueError, match="unseenword"):
        carry.derive(root, "wordlist-v3", "wordlist-v2", CHECK)


def test_verify_holds_the_committed_baseline():
    assert run_verify(REPO) == []


def test_verify_bites_on_a_changed_carried_count(tmp_path):
    root = tree(tmp_path)
    d = committed()
    d["words"][0]["counts"]["2020"] += 1
    (root / "syntheticflood/baseline/wordlist-v3.json").write_text(json.dumps(d))
    assert any("differs from its source" in x for x in run_verify(root))


def test_verify_bites_on_an_added_word_relabelled_as_carried(tmp_path):
    root = tree(tmp_path)
    d = committed()
    for w in d["words"]:
        if w["word"] == "samples":
            w["source"] = "carried"
    (root / "syntheticflood/baseline/wordlist-v3.json").write_text(json.dumps(d))
    assert any("samples" in x for x in run_verify(root))


def test_verify_bites_on_a_changed_source(tmp_path):
    root = tree(tmp_path)
    p = root / CHECK
    rec = json.loads(p.read_text())
    rec["http_429"] += 1
    p.write_text(json.dumps(rec))
    assert any("source added" in x for x in run_verify(root))
