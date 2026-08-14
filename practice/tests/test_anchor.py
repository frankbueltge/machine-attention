"""The anchoring tool, tested without touching the network.

The tool lives in tools/ rather than in the practice package, because the substrate is
deliberately dependency-free and anchoring shells out to the `ots` client. It is loaded
here by path so it still runs inside the one pytest invocation CI already performs.

What is worth asserting offline: that proofs never land inside an append-only record tree
(the reason they live apart at all), that the register list is a glob rather than a list,
and that the ledger's own numbers survive being recomputed from the files it names.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
APPEND_ONLY = ("snapshots", "readings", "resolutions", "attention")


def load_anchor():
    spec = importlib.util.spec_from_file_location("anchor", REPO / "tools" / "anchor.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["anchor"] = mod
    spec.loader.exec_module(mod)
    return mod


anchor = load_anchor()


def test_every_manifest_found_is_a_real_manifest_outside_the_proof_tree():
    found = anchor.manifests()
    assert found, "no manifests found — the glob has stopped matching the registers"
    for m in found:
        assert m.name == "manifest.json"
        assert m.is_file()
        assert anchor.PROOFS not in m.parents


def test_the_glob_finds_both_registers_and_nested_ones():
    """A list would have to be maintained; a glob picks up a new register on its first night."""
    rel = {str(m.relative_to(REPO)) for m in anchor.manifests()}
    assert any(p.startswith("darkocean/snapshots/") for p in rel)
    assert any(p.startswith("foreknown/snapshots/") for p in rel)
    assert any(p.startswith("foreknown/reaction/snapshots/") for p in rel), "nested registers must be reached too"


def test_proofs_never_land_inside_an_append_only_tree():
    """The invariant behind the anchors/ mirror: `ots upgrade` rewrites a proof exactly once,
    and CI's I3 guard refuses modifications under the record trees. A proof stored beside its
    manifest would make the upgrade an illegal change to an immutable record."""
    for m in anchor.manifests():
        proof = anchor.proof_for(m)
        assert anchor.PROOFS in proof.parents
        parts = proof.relative_to(anchor.PROOFS).parts
        assert any(seg in APPEND_ONLY for seg in parts), "the mirror should keep the record path"
        assert not any(seg in APPEND_ONLY for seg in proof.relative_to(REPO).parts[:1])
        assert proof.name.endswith(".json.ots")


def test_no_orphan_proof_without_the_manifest_it_commits_to():
    known = {anchor.proof_for(m) for m in anchor.manifests()}
    for proof in anchor.PROOFS.rglob("*.ots"):
        assert proof in known, f"{proof} commits to a manifest that is no longer in the register"


def test_no_client_backup_files_are_kept():
    """`ots upgrade` leaves a .bak; it is the client's convenience, not part of the record."""
    assert list(anchor.PROOFS.rglob("*.bak")) == []


@pytest.mark.skipif(not (REPO / "anchors" / "ledger.json").exists(), reason="no ledger committed yet")
def test_the_ledger_recomputes_from_the_files_it_names():
    ledger = json.loads((REPO / "anchors" / "ledger.json").read_text())
    entries = ledger["anchors"]
    counts = ledger["counts"]
    assert counts["manifests"] == len(entries)
    assert counts["complete"] == sum(e["state"] == "complete" for e in entries)
    assert counts["pending"] == sum(e["state"] == "pending" for e in entries)
    assert counts["failures"] == len(ledger["failures"])
    for e in entries:
        m = REPO / e["manifest"]
        assert m.is_file(), f"ledger names a manifest that is gone: {e['manifest']}"
        # the digest is the whole point — recompute it rather than trust the record
        assert anchor.sha256(m) == e["sha256"]
        if e["state"] in {"pending", "complete"}:
            assert (REPO / e["proof"]).is_file()
    # the honest-limits statement is part of the artefact, not decoration
    assert "no later than" in ledger["proves"]
    assert "Bitcoin node" in ledger["verify"]


@pytest.mark.skipif(not (REPO / "anchors" / "ledger.json").exists(), reason="no ledger committed yet")
def test_a_complete_anchor_names_the_blocks_a_reader_can_check():
    """A finished proof must say WHICH blocks carry it. "bitcoin attestation present" is an
    assertion; a height is something a reader checks against a chain instead of against us.
    (The first version read the height off a whitespace split and always lost it — the
    client prints it inside the attestation name.)"""
    ledger = json.loads((REPO / "anchors" / "ledger.json").read_text())
    for e in ledger["anchors"]:
        if e["state"] != "complete":
            continue
        assert re.search(r"bitcoin block\(s\) \d{6,}", e["evidence"]), e


def test_a_missing_client_is_a_recorded_failure_not_a_crash(monkeypatch, tmp_path):
    """If the ots client or a calendar is unavailable, the run must still finish: the
    registers have already committed, and anchoring may never be able to break them."""
    monkeypatch.setattr(anchor, "ots", lambda *a, **k: (127, "ots client not installed"))
    out = tmp_path / "ledger.json"
    rc = anchor.main(["--ledger", str(out)])
    assert rc == 0
    written = json.loads(out.read_text())
    # nothing was stamped or read, and every manifest says so on the record: an
    # existing proof becomes "unreadable", a missing one "unstamped" — never silence.
    assert written["counts"]["stamped_this_run"] == 0
    assert written["counts"]["upgraded_this_run"] == 0
    assert written["counts"]["complete"] == 0
    assert {e["state"] for e in written["anchors"]} <= {"unstamped", "unreadable"}
    assert written["counts"]["failures"] == len(written["anchors"])


def test_the_tool_runs_offline_end_to_end_without_touching_the_real_ledger(tmp_path):
    """--ledger is mandatory here on purpose. An earlier version of this test ran the tool
    with the default path and overwrote the committed ledger with the state of a machine
    that had no client installed. A test may never rewrite the record it checks."""
    real = REPO / "anchors" / "ledger.json"
    before = real.read_bytes() if real.exists() else None
    out = tmp_path / "ledger.json"
    p = subprocess.run([sys.executable, str(REPO / "tools" / "anchor.py"),
                        "--no-network", "--ledger", str(out)],
                       capture_output=True, text=True, timeout=120)
    assert p.returncode == 0, p.stderr
    assert "manifests" in p.stdout
    assert out.is_file()
    assert (real.read_bytes() if real.exists() else None) == before, "the committed ledger was modified"


def test_register_lists_every_night_the_ledger_does_not_know(tmp_path):
    """The notary jobs' half of the anchoring handshake (the deadlock of 2026-08-10..12):
    a fresh night can never already be stamped, but it can and must be LISTED. From an
    empty ledger, register mode lists every register night as "unstamped" — the disclosed
    state the verifier already accepts as legitimate, never as a hole."""
    out = tmp_path / "ledger.json"
    rc = anchor.main(["--register", "--ledger", str(out)])
    assert rc == 0
    written = json.loads(out.read_text())
    rels = [e["manifest"] for e in written["anchors"]]
    assert rels == sorted(str(m.relative_to(REPO)) for m in anchor.manifests())
    for e in written["anchors"]:
        assert e["state"] == "unstamped"
        assert e["sha256"] == anchor.sha256(REPO / e["manifest"])
    assert written["counts"]["manifests"] == len(rels)
    assert written["counts"]["complete"] == 0


def test_register_never_rewrites_an_existing_row(tmp_path):
    """Register mode may only append. A completed Bitcoin proof's row — digest, state,
    evidence — is the record of an act already performed; the night job holds no client
    and must not touch it, and recorded failures stay on the record too."""
    out = tmp_path / "ledger.json"
    ms = anchor.manifests()
    first = str(ms[0].relative_to(REPO))
    seeded = {"anchors": [{"manifest": first, "sha256": "seeded-digest",
                           "state": "complete", "proof": "anchors/x.ots",
                           "evidence": "bitcoin block(s) 961744"}],
              "failures": [{"manifest": first, "step": "stamp", "at": "t", "detail": "kept"}]}
    out.write_text(json.dumps(seeded))
    rc = anchor.main(["--register", "--ledger", str(out)])
    assert rc == 0
    written = json.loads(out.read_text())
    kept = [e for e in written["anchors"] if e["manifest"] == first]
    assert kept == seeded["anchors"], "the existing row must survive byte for byte"
    assert written["failures"] == seeded["failures"]
    assert len(written["anchors"]) == len(ms)
    assert all(e["state"] == "unstamped"
               for e in written["anchors"] if e["manifest"] != first)


def test_register_with_nothing_new_leaves_the_ledger_bytes_alone(tmp_path):
    """A run that learns nothing must change nothing: a generated_at-only diff is the
    kind of empty commit the record does not need (main, 2026-08-11, moved exactly one
    timestamp and nothing else)."""
    out = tmp_path / "ledger.json"
    assert anchor.main(["--register", "--ledger", str(out)]) == 0
    before = out.read_bytes()
    assert anchor.main(["--register", "--ledger", str(out)]) == 0
    assert out.read_bytes() == before


def test_the_stamping_job_rebuilds_and_commits_the_stage_it_outdates():
    """Stamping changes what verify.html renders, so the same job must rebuild it.

    2026-08-14: the anchor run of the night before upgraded two nights to complete
    and left public/verify.html rendering the old counts and blocks. verify.py's
    deterministic-rebuild check (I1) failed from that commit onward, and the first
    scheduled job to say so was darkocean the next morning — a project the stage does
    not even name, since it renders foreknown/ anchors only. The hole belonged here,
    so the guard does too: whatever this job commits, the rebuilt stage travels with it.
    """
    workflow = (REPO / ".github" / "workflows" / "anchor.yml").read_text(encoding="utf-8")
    assert "stage/generate.py" in workflow, "the stamping job must rebuild the stage"
    added = re.findall(r"^\s*git add (.+)$", workflow, re.MULTILINE)
    assert added, "this job commits, so it has a git add to check"
    assert all("public" in line for line in added), \
        "the rebuilt stage belongs in the same commit as the ledger it renders"
