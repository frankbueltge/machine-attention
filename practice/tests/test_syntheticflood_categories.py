"""Synthetic Flood V0 increment 2: Register B, the dated category sizes — the
fixed request, the parser against the audit's preserved answer, the reader
(no network), and the verifier checks proven to bite."""
from __future__ import annotations

import importlib.util
import io
import json
import sys
import urllib.error
from pathlib import Path

import pytest

from practice.fetch import Client
from practice.syntheticflood import categories, wikipedia

REPO = Path(__file__).resolve().parents[2]
PROBES = REPO / "syntheticflood/probes/2026-10-18"
ANSWER = (PROBES / "mediawiki/allcategories-ai.json").read_bytes()



def load_verify():
    spec = importlib.util.spec_from_file_location("verifymod_sfc", REPO / "verify.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verifymod_sfc"] = mod
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


def client(data=ANSWER, seen=None):
    def opener(req, timeout=None):
        if seen is not None:
            seen.append(req)
        return Resp(data)
    return Client(opener=opener, sleep=lambda s: None)


def run_verify(root: Path) -> list[str]:
    problems: list[str] = []
    registry: dict = {}
    verify.check_snapshots(root, verify.SF_SNAP, problems, registry, False)
    verify.check_syntheticflood_categories(root, registry, problems)
    return problems


def write(root, reading):
    path = categories.reading_path(root, reading["date"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(reading), encoding="utf-8")


# --- the request and the answer ---------------------------------------------

def test_url_is_the_audited_probe_url():
    manifest = json.loads((PROBES / "manifest.json").read_text())
    probe = next(e for e in manifest["entries"] if e["name"] == "allcategories-ai")
    assert wikipedia.URL == probe["url"] == verify.SF_WIKI_URL
    assert wikipedia.USER_AGENT == probe["user_agent"]


def test_parse_matches_the_audit_table():
    r = wikipedia.parse(ANSWER)
    texts = r["families"]["texts"]
    assert texts["months"]["2026-10"] == 3504 and texts["months"]["2025-05"] == 1
    # May 2025 to October 2026: the container counts exactly its dated months.
    assert texts["container"] == {"size": 18, "pages": 0, "subcats": 18}
    assert len(texts["months"]) == 18 and list(texts["months"]) == sorted(texts["months"])
    assert r["families"]["sources"]["months"]["2024-11"] == 83
    assert r["complete"] is True and r["unmatched"] == []


def test_parser_and_verifier_agree():
    assert wikipedia.parse(ANSWER) == verify._sf_wiki_derive(ANSWER)


def test_odd_category_is_kept_unmatched():
    data = json.dumps({"query": {"allcategories": [
        {"category": "Articles containing suspected AI-generated texts from Smarch 2026",
         "size": 4, "pages": 4, "files": 0, "subcats": 0}]},
        "continue": {"accontinue": "x"}}).encode()
    r = wikipedia.parse(data)
    assert r["unmatched"][0]["size"] == 4 and r["complete"] is False
    assert r == verify._sf_wiki_derive(data)


# --- the reader ---------------------------------------------------------------

def test_read_preserves_and_verifies(tmp_path):
    seen = []
    r = categories.read(tmp_path, "2026-10-20", client(seen=seen))
    assert len(seen) == 1 and seen[0].get_header("User-agent") == wikipedia.USER_AGENT
    assert r["status"] == 200 and r["requests"] == 1
    assert r["file"] == "syntheticflood/snapshots/2026-10-20-categories/allcategories.json"
    write(tmp_path, r)
    assert run_verify(tmp_path) == []


def test_outage_is_recorded_not_invented(tmp_path):
    def opener(req, timeout=None):
        raise urllib.error.URLError("down")
    c = Client(opener=opener, sleep=lambda s: None, backoff=())
    r = categories.read(tmp_path, "2026-10-20", c)
    assert "families" not in r and r["error"] and "file" not in r
    write(tmp_path, r)
    assert run_verify(tmp_path) == []


# --- the verifier bites ---------------------------------------------------------

@pytest.fixture
def good(tmp_path):
    return tmp_path, categories.read(tmp_path, "2026-10-20", client())


def bites(root, reading, needle):
    write(root, reading)
    problems = run_verify(root)
    assert any(needle in p for p in problems), problems


def test_changed_size_is_caught(good):
    root, r = good
    r["families"]["texts"]["months"]["2026-10"] += 1
    bites(root, r, "families differs")


def test_stored_title_is_caught(good):
    root, r = good
    r["pages"] = ["Some article"]
    bites(root, r, "outside category sizes")


def test_foreign_request_is_caught(good):
    root, r = good
    r["url"] = r["url"].replace("allcategories", "categorymembers")
    bites(root, r, "not the audited")


def test_sizes_without_bytes_are_caught(good):
    root, r = good
    del r["file"]
    bites(root, r, "without preserved bytes")


def test_answer_from_another_day_is_caught(good):
    root, r = good
    r["date"] = "2026-10-21"
    write(root, r)
    problems = run_verify(root)
    assert any("under its own date" in p for p in problems), problems
