"""The verdicts check, proven to bite.

Verdict files annotate a committed reading with model estimates delivered by
the discovery pass (the routine channel, Frank's decision of 2026-08-15).
Each test builds a minimal memoryhole tree in a temp directory, breaks exactly
one thing, and asserts the verifier names it — a check that never fires is
decoration.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def load_verify():
    spec = importlib.util.spec_from_file_location("verifymod", REPO / "verify.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verifymod"] = mod
    spec.loader.exec_module(mod)
    return mod


verify = load_verify()

DAY = "2026-08-14"
SHA = "a" * 64


def build(tmp: Path, *, verdicts: dict | None = None,
          write_reading: bool = True) -> Path:
    (tmp / "memoryhole" / "readings").mkdir(parents=True)
    (tmp / "memoryhole" / "verdicts").mkdir(parents=True)
    if write_reading:
        reading = {
            "date": DAY,
            "entries": [{"url": "https://example.org/page",
                         "abstentions": [{"before_sha256": SHA,
                                          "salience": 12}]}],
        }
        (tmp / "memoryhole" / "readings" / f"{DAY}.json").write_text(
            json.dumps(reading), encoding="utf-8")
    if verdicts is None:
        verdicts = {
            "date": DAY,
            "source_reading": f"memoryhole/readings/{DAY}.json",
            "model": "claude-sonnet-5",
            "prompt_version": "memoryhole-classify-routine-v1",
            "cap": 40,
            "estimated": True,
            "unclassified_at_cap": 0,
            "verdicts": [{"before_sha256": SHA, "type": "number_revised",
                          "confidence": "medium", "estimated": True}],
        }
    (tmp / "memoryhole" / "verdicts" / f"{DAY}.json").write_text(
        json.dumps(verdicts), encoding="utf-8")
    return tmp


def problems_for(tmp: Path) -> list[str]:
    problems: list[str] = []
    verify.check_memoryhole_verdicts(tmp, problems)
    return problems


def test_clean_verdicts_pass(tmp_path):
    build(tmp_path)
    assert problems_for(tmp_path) == []


def test_verdict_without_matching_abstention_is_named(tmp_path):
    build(tmp_path)
    block = json.loads((tmp_path / "memoryhole" / "verdicts" / f"{DAY}.json")
                       .read_text(encoding="utf-8"))
    block["verdicts"][0]["before_sha256"] = "b" * 64
    (tmp_path / "memoryhole" / "verdicts" / f"{DAY}.json").write_text(
        json.dumps(block), encoding="utf-8")
    assert any("no matching abstention" in p for p in problems_for(tmp_path))


def test_unknown_type_is_named(tmp_path):
    build(tmp_path)
    block = json.loads((tmp_path / "memoryhole" / "verdicts" / f"{DAY}.json")
                       .read_text(encoding="utf-8"))
    block["verdicts"][0]["type"] = "coverup_detected"
    (tmp_path / "memoryhole" / "verdicts" / f"{DAY}.json").write_text(
        json.dumps(block), encoding="utf-8")
    assert any("unknown type" in p for p in problems_for(tmp_path))


def test_missing_estimated_flag_is_named(tmp_path):
    build(tmp_path)
    block = json.loads((tmp_path / "memoryhole" / "verdicts" / f"{DAY}.json")
                       .read_text(encoding="utf-8"))
    block["estimated"] = False
    block["verdicts"][0].pop("estimated")
    (tmp_path / "memoryhole" / "verdicts" / f"{DAY}.json").write_text(
        json.dumps(block), encoding="utf-8")
    problems = problems_for(tmp_path)
    assert any(f"verdicts {DAY}: not labelled estimated" in p
               for p in problems)
    assert any(f"verdicts {DAY}[0]: not labelled estimated" in p
               for p in problems)


def test_over_cap_is_named(tmp_path):
    verdict = {"before_sha256": SHA, "type": "number_revised",
               "confidence": "low", "estimated": True}
    build(tmp_path, verdicts={
        "date": DAY, "source_reading": f"memoryhole/readings/{DAY}.json",
        "model": "claude-sonnet-5",
        "prompt_version": "memoryhole-classify-routine-v1",
        "cap": 2, "estimated": True, "unclassified_at_cap": 0,
        "verdicts": [dict(verdict) for _ in range(3)],
    })
    assert any("against cap" in p for p in problems_for(tmp_path))


def test_verdicts_without_reading_are_named(tmp_path):
    build(tmp_path, write_reading=False)
    assert any("no reading to annotate" in p for p in problems_for(tmp_path))


def test_date_mismatch_is_named(tmp_path):
    build(tmp_path)
    block = json.loads((tmp_path / "memoryhole" / "verdicts" / f"{DAY}.json")
                       .read_text(encoding="utf-8"))
    block["date"] = "2026-08-13"
    (tmp_path / "memoryhole" / "verdicts" / f"{DAY}.json").write_text(
        json.dumps(block), encoding="utf-8")
    assert any("disagrees with filename" in p for p in problems_for(tmp_path))
