"""Synthetic Flood: the check reading of control-check-v1 (2026-11-06), its
re-derivation, the successor word list, and the verifier checks proven to bite."""
from __future__ import annotations

import copy
import importlib.util
import io
import json
import shutil
import sys
import urllib.parse
from pathlib import Path

from practice.fetch import Client
from practice.syntheticflood import controlcheck, controlread, pubmed, wordlist

REPO = Path(__file__).resolve().parents[2]


def load_verify():
    spec = importlib.util.spec_from_file_location("verifymod_sfcr", REPO / "verify.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verifymod_sfcr"] = mod
    spec.loader.exec_module(mod)
    return mod


verify = load_verify()


class Resp(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def fake_opener(total: int):
    """Canonical count answers: the cohort total, or a word-dependent count."""
    def opener(req, timeout=None):
        term = urllib.parse.parse_qs(urllib.parse.urlsplit(req.full_url).query)["term"][0]
        word = term.split("[tiab]")[0] if "[tiab]" in term else None
        return Resp(pubmed.canonical(total if word is None else len(word) * 10 + 7))
    return opener

RECORD = REPO / "syntheticflood/controlcheck/2026-11-06.json"


def committed():
    return json.loads(RECORD.read_text(encoding="utf-8"))


def base_and_doc():
    doc, _, _ = wordlist.load(REPO, "wordlist-v2")
    base = json.loads((REPO / "syntheticflood/baseline/wordlist-v2.json").read_text(encoding="utf-8"))
    return base, doc


def test_the_plan_is_the_rules_113_counts():
    _, doc = base_and_doc()
    rows = controlread.plan(doc["controls"])
    assert len(rows) == 8 + 19 * 3 + 6 * 8 == 113
    assert ("2023", "reduced") not in rows


def test_the_committed_record_re_derives_from_its_rows():
    rec = committed()
    base, doc = base_and_doc()
    again = controlread.evaluate(base, doc["controls"], controlread.counts_from_rows(rec["rows"]))
    assert again["results"] == rec["results"]
    assert again["composition"] == rec["composition"]
    assert rec["composition"]["dropped"] == ["effect", "levels", "observed"]
    assert rec["composition"]["added"] == ["samples", "groups", "cases", "performed"]


def test_the_word_total_is_never_the_cohort_total():
    """The defect of the first evaluation on 2026-11-06: the candidate word
    `total` overwrote the cohort total, and every control fell at ratio ~6.5."""
    rec = committed()
    counts = controlread.counts_from_rows(rec["rows"])
    assert counts["2023"][None] != counts["2023"]["total"]
    r = rec["results"]["data"]["years"]["2023"]
    assert r["observed"] == round(r["count"] / counts["2023"][None], 9)


def test_wordlist_v3_is_the_composition_and_carries_the_rest():
    rec = committed()
    v2, _, _ = wordlist.load(REPO, "wordlist-v2")
    v3, _, _ = wordlist.load(REPO, "wordlist-v3")
    assert v3["controls"] == rec["composition"]["controls"]
    assert len(v3["controls"]) == controlcheck.TARGET
    assert v3["fixed"] == v2["fixed"] and v3["pool"] == v2["pool"]


def test_a_reading_without_network_writes_every_planned_row(tmp_path):
    for sub in ("wordlists", "baseline"):
        shutil.copytree(REPO / "syntheticflood" / sub, tmp_path / "syntheticflood" / sub)
    client = Client(opener=fake_opener(1000), sleep=lambda s: None)
    rec = controlread.read(tmp_path, "2026-11-06", "wordlist-v2", client)
    assert len(rec["rows"]) == 113 and all(r["count"] is not None for r in rec["rows"])


def run_verify(root: Path) -> list[str]:
    problems: list[str] = []
    verify.check_syntheticflood_controlcheck(root, {}, problems)
    return problems


def tree(tmp_path) -> Path:
    for sub in ("wordlists", "baseline", "controlcheck"):
        shutil.copytree(REPO / "syntheticflood" / sub, tmp_path / "syntheticflood" / sub)
    return tmp_path


def test_verify_holds_the_committed_record():
    assert run_verify(REPO) == []


def test_verify_bites_on_a_changed_count(tmp_path):
    root = tree(tmp_path)
    p = root / "syntheticflood/controlcheck/2026-11-06.json"
    d = json.loads(p.read_text())
    d["rows"][10]["count"] += 1
    p.write_text(json.dumps(d))
    assert any("SHA-256" in x for x in run_verify(root))


def test_verify_bites_on_a_changed_verdict_or_composition(tmp_path):
    root = tree(tmp_path)
    p = root / "syntheticflood/controlcheck/2026-11-06.json"
    d = json.loads(p.read_text())
    e = copy.deepcopy(d)
    e["results"]["effect"]["pass"] = True
    e["composition"]["kept"].append("effect")
    p.write_text(json.dumps(e))
    probs = run_verify(root)
    assert any("'effect'" in x for x in probs) and any("composition" in x for x in probs)


def test_verify_bites_on_a_successor_that_is_not_the_composition(tmp_path):
    root = tree(tmp_path)
    w = root / "syntheticflood/wordlists/wordlist-v3.json"
    d = json.loads(w.read_text())
    d["controls"][-1] = "age"
    w.write_text(json.dumps(d))
    assert any("not the composition" in x for x in run_verify(root))
