"""The verifier's anchor check, proven to bite.

A check that never fires is decoration. Each test here builds a minimal repository in a
temp directory, breaks exactly one thing, and asserts the verifier names it — the same
discipline the stage rebuild is held to.

The proofs are synthesised from the OpenTimestamps header format rather than stamped, so
these tests need no network and no client: magic, one version byte, the SHA-256 op, then
the digest of the file the proof commits to.
"""
from __future__ import annotations

import hashlib
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


def fake_proof(digest_hex: str) -> bytes:
    """A header-valid proof committing to digest_hex. Enough for the byte-level pairing
    check; nothing here claims to be a real Bitcoin attestation."""
    return verify.OTS_MAGIC + bytes([1, verify.OTS_SHA256_OP]) + bytes.fromhex(digest_hex) + b"\x00"


def build(tmp: Path, *, state: str = "complete", evidence: str = "bitcoin block(s) 961744",
          proof_bytes: bytes | None = None, write_proof: bool = True,
          list_in_ledger: bool = True, ledger_digest: str | None = None,
          counts: dict | None = None) -> Path:
    """A repository with one register, one night, one anchor — then whatever is broken."""
    manifest = tmp / "reg" / "snapshots" / "2026-08-07" / "manifest.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps({"entries": [], "run_date": "2026-08-07"}) + "\n")
    digest = hashlib.sha256(manifest.read_bytes()).hexdigest()

    proof = tmp / "anchors" / "reg" / "snapshots" / "2026-08-07" / "manifest.json.ots"
    proof.parent.mkdir(parents=True)
    if write_proof:
        proof.write_bytes(proof_bytes if proof_bytes is not None else fake_proof(digest))

    entries = []
    if list_in_ledger:
        entries.append({"manifest": "reg/snapshots/2026-08-07/manifest.json",
                        "sha256": ledger_digest or digest,
                        "proof": "anchors/reg/snapshots/2026-08-07/manifest.json.ots",
                        "state": state, "evidence": evidence})
    resolved = counts or {"complete": sum(e["state"] == "complete" for e in entries),
                          "pending": sum(e["state"] == "pending" for e in entries)}
    (tmp / "anchors" / "ledger.json").write_text(
        json.dumps({"counts": resolved, "failures": [], "anchors": entries}) + "\n")
    return tmp


def problems_for(tmp: Path) -> list[str]:
    found: list[str] = []
    verify.check_anchors(tmp, found)
    return found


def test_a_sound_anchor_raises_nothing():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        assert problems_for(build(Path(d))) == []


def test_no_anchors_directory_is_not_a_hole():
    """A register that has not been anchored yet must not fail the chain."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "reg" / "snapshots" / "2026-08-07").mkdir(parents=True)
        (Path(d) / "reg" / "snapshots" / "2026-08-07" / "manifest.json").write_text("{}")
        assert problems_for(Path(d)) == []


def test_it_catches_a_ledger_digest_that_no_longer_matches_the_bytes():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        found = problems_for(build(Path(d), ledger_digest="00" * 32))
        assert any("ledger digest diverges from the bytes" in p for p in found), found


def test_it_catches_a_proof_committing_to_something_else():
    """The heart of it: a proof for a different file must not pass as this night's anchor."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        found = problems_for(build(Path(d), proof_bytes=fake_proof("ab" * 32)))
        assert any("proof commits to" in p for p in found), found


def test_it_catches_a_missing_proof_file():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        found = problems_for(build(Path(d), write_proof=False))
        assert any("proof" in p and "missing" in p for p in found), found


def test_it_catches_a_file_that_is_not_an_ots_proof_at_all():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        found = problems_for(build(Path(d), proof_bytes=b"not a proof"))
        assert any("is not an OpenTimestamps proof" in p for p in found), found


def test_it_catches_a_night_the_ledger_omits():
    """An unstamped night is legitimate; a night missing from the ledger is not."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        found = problems_for(build(Path(d), list_in_ledger=False))
        assert any("ledger omits" in p for p in found), found


def test_it_catches_complete_without_a_named_block():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        found = problems_for(build(Path(d), evidence="bitcoin attestation present"))
        assert any("complete without a named Bitcoin block" in p for p in found), found


def test_it_catches_counts_that_disagree_with_the_entries():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        found = problems_for(build(Path(d), counts={"complete": 7, "pending": 0}))
        assert any("ledger counts complete=7" in p for p in found), found


def test_it_catches_an_orphan_proof_and_a_committed_client_backup():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        tmp = build(Path(d))
        stray = tmp / "anchors" / "reg" / "snapshots" / "2026-08-06" / "manifest.json.ots"
        stray.parent.mkdir(parents=True)
        stray.write_bytes(fake_proof("cd" * 32))
        (tmp / "anchors" / "reg" / "snapshots" / "2026-08-07" / "manifest.json.ots.bak").write_bytes(b"x")
        found = problems_for(tmp)
        assert any("orphan proof" in p for p in found), found
        assert any("client backup committed" in p for p in found), found
