"""Synthetic Flood V0 increment 1: the word list, the count query, the cohort
reader (no network), and the verifier checks proven to bite."""
from __future__ import annotations

import copy
import importlib.util
import io
import json
import shutil
import sys
import urllib.parse
from pathlib import Path

import pytest

from practice.fetch import Client
from practice.syntheticflood import cohort, pubmed, wordlist

REPO = Path(__file__).resolve().parents[2]
PROBES = REPO / "syntheticflood/probes/2026-10-18"


def load_verify():
    spec = importlib.util.spec_from_file_location("verifymod_sf", REPO / "verify.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verifymod_sf"] = mod
    spec.loader.exec_module(mod)
    return mod


verify = load_verify()


class Resp(io.BytesIO):
    def __init__(self, data, status=200):
        super().__init__(data)
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def fake_opener(answers):
    """Answer each count query with canonical bytes; overrides by word."""
    def opener(req, timeout=None):
        term = urllib.parse.parse_qs(urllib.parse.urlsplit(req.full_url).query)["term"][0]
        word = term.split("[tiab]")[0] if "[tiab]" in term else None
        data = answers.get(word, pubmed.canonical(len(word or "") * 10 + 7))
        return Resp(data)
    return opener


def client(answers=None):
    return Client(opener=fake_opener(answers or {}), sleep=lambda s: None)


def tiny_repo(tmp: Path) -> Path:
    d = tmp / "syntheticflood/wordlists"
    d.mkdir(parents=True)
    (d / "wordlist-v1.json").write_text(json.dumps({
        "schema": "syntheticflood-wordlist-v1", "version": "wordlist-v1",
        "fixed": ["delve", "intricate"], "controls": ["patients"],
        "pool": ["pivotal"]}), encoding="utf-8")
    return tmp


def run_verify(root: Path) -> list[str]:
    problems: list[str] = []
    registry: dict = {}
    verify.check_snapshots(root, verify.SF_SNAP, problems, registry, False)
    verify.check_syntheticflood(root, registry, problems)
    return problems


def write(root, reading):
    path = cohort.reading_path(root, reading["cohort"], reading["date"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(reading), encoding="utf-8")


# --- the query and the answer shape ------------------------------------------

def test_count_url_is_the_audited_probe_url():
    manifest = json.loads((PROBES / "manifest.json").read_text())
    urls = {e["name"]: e["url"] for e in manifest["entries"] if e["source"] == "pubmed"}
    assert pubmed.count_url(pubmed.cohort_term("2026-09", "delve")) == urls["delve-2026-09"]
    assert pubmed.count_url(pubmed.cohort_term("2024-03")) == urls["cohort-2024-03"]


@pytest.mark.parametrize("name", ["cohort-2019-03", "delve-2024-03", "control-patients-2024-03"])
def test_probe_answers_are_canonical(name):
    data = (PROBES / "pubmed" / f"{name}.json").read_bytes()
    assert pubmed.canonical(pubmed.parse_count(data)) == data


def test_committed_wordlist_is_valid_and_disjoint():
    doc, rel, sha = wordlist.load(REPO, "wordlist-v1")
    assert rel == "syntheticflood/wordlists/wordlist-v1.json"
    assert "delve" in doc["fixed"] and "patients" in doc["controls"]
    assert len(sha) == 64


def test_wordlist_rejects_overlap():
    assert wordlist.validate({"fixed": ["delve"], "controls": ["delve"], "pool": ["x"]})


def test_lag():
    assert cohort.lag("2026-09", "2026-10-19") == 1
    assert cohort.lag("2025-11", "2026-02-01") == 3


# --- the reader ---------------------------------------------------------------

def test_read_counts_every_word_and_verifies(tmp_path):
    root = tiny_repo(tmp_path)
    r = cohort.read(root, "2026-09", "2026-10-19", "wordlist-v1", client())
    assert [c["word"] for c in r["counts"]] == ["delve", "intricate", "patients", "pivotal"]
    assert r["lag_months"] == 1 and r["value"] is False and r["retrospective"] is False
    assert not (root / cohort.SNAP_BASE).exists()      # canonical answers keep no bytes
    write(root, r)
    assert run_verify(root) == []


def test_incomplete_cohort_is_refused(tmp_path):
    with pytest.raises(ValueError):
        cohort.read(tiny_repo(tmp_path), "2026-10", "2026-10-19", "wordlist-v1", client())


def test_odd_answer_is_preserved_and_verifies(tmp_path):
    root = tiny_repo(tmp_path)
    odd = b'{"header":{"type":"esearch","version":"0.4"},"esearchresult":{"count":"5"}}'
    r = cohort.read(root, "2026-09", "2026-10-19", "wordlist-v1", client({"delve": odd}))
    row = r["counts"][0]
    assert row["count"] == 5 and row["file"].startswith(cohort.SNAP_BASE)
    write(root, r)
    assert run_verify(root) == []


# --- the verifier bites ---------------------------------------------------------

@pytest.fixture
def good(tmp_path):
    root = tiny_repo(tmp_path)
    return root, cohort.read(root, "2026-09", "2026-10-19", "wordlist-v1", client())


def bites(root, reading, needle):
    write(root, reading)
    problems = run_verify(root)
    assert any(needle in p for p in problems), problems


def test_changed_count_is_caught(good):
    root, r = good
    r = copy.deepcopy(r)
    r["counts"][0]["count"] += 1
    bites(root, r, "does not match the SHA-256")


def test_stored_text_is_caught(good):
    root, r = good
    r["counts"][1]["abstract"] = "some publisher text"
    bites(root, r, "outside counts-only")


def test_dropped_word_is_caught(good):
    root, r = good
    del r["counts"][2]
    bites(root, r, "do not cover the word list")


def test_foreign_query_is_caught(good):
    root, r = good
    r["counts"][0]["url"] = r["counts"][0]["url"].replace("rettype=count", "rettype=abstract")
    bites(root, r, "deterministic count query")


def test_changed_wordlist_is_caught(good):
    root, r = good
    write(root, r)
    wl = root / "syntheticflood/wordlists/wordlist-v1.json"
    wl.write_text(wl.read_text().replace("pivotal", "realm"))
    assert any("missing or changed" in p for p in run_verify(root))


def test_wrong_lag_is_caught(good):
    root, r = good
    r["value"] = True
    bites(root, r, "lag, value or retrospective")
