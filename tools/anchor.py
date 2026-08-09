#!/usr/bin/env python3
"""anchor — notarize the registers' daily manifests to Bitcoin via OpenTimestamps.

Why (decision D2 of the portfolio audit, Frank's GO 2026-08-09 for Dark Ocean and
The Foreknown): every register's claim has a date in it — "held before eviction",
"notarized what was knowable, when" — and until now the only evidence for those
dates was this repository's git history. Commit dates are self-asserted: set by the
committer's clock, rewritable, force-pushable. Git proves order and content, not time.
An OpenTimestamps proof puts the manifest's hash into a Bitcoin block, after which the
date holds without this repository, without GitHub, and without trusting our clock.

What it anchors: every `*/snapshots/<date>/manifest.json`. A manifest already carries
the SHA-256 of every preserved byte of that night, so ONE stamp per manifest covers the
night's whole material. New registers are picked up by the glob, not by a list.

Two phases, because a fresh proof is not yet a proof:

  stamp    the calendars return promises ("PendingAttestation") in ~2 seconds
  upgrade  later, once their aggregating transaction has confirmed, the Merkle path
           down to a Bitcoin block is baked into the .ots and the file stands alone

Measured 2026-08-09: a transaction appeared within ~50 minutes; the calendar then
waits for 6 confirmations before serving the completed path. So this tool must run
repeatedly over the same files and only stop touching one once it is complete.

Deliberately NOT part of the practice substrate:

  * `practice/` stays dependency-free and keyless. This tool shells out to the `ots`
    client, installed by the workflow, and lives outside the substrate.
  * It runs as its own job, AFTER the registers have committed. Anchoring must never
    be able to break a register: if every calendar is down, the night's reading still
    lands and this tool records the failure.

Honest limits, restated where the code is: an anchor proves the bytes existed no later
than a block — not that they are true, not that they came from the publisher they name,
and not that they did not exist earlier. Verifying the Bitcoin side needs a Bitcoin node;
a block explorer is a third party, which is the trust an anchor exists to remove.
See docs/2026-08-09-opentimestamps-examination.md.

Usage:
  python3 tools/anchor.py                 # stamp new manifests, upgrade incomplete ones
  python3 tools/anchor.py --no-network    # ledger only, from the files on disk
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Proofs live OUTSIDE the append-only record trees, mirroring their paths.
# Reason, found the hard way: `ots upgrade` REWRITES the .ots file when the Bitcoin
# path arrives, and CI's I3 guard rightly refuses modifications under
# */snapshots/. A proof is not an append-only record — it is expected to change
# exactly once, from promise to proof — so it does not belong in a tree that must
# never change. The manifest it commits to stays untouched either way.
PROOFS = ROOT / "anchors"
LEDGER = PROOFS / "ledger.json"
# The mark of a finished proof: the client prints this attestation type once the
# Merkle path reaches a block header. Parsing `ots info` is more robust than the
# exit codes, which report "Failed! Timestamp not complete" as a normal outcome.
COMPLETE_MARK = "BitcoinBlockHeaderAttestation"
PENDING_MARK = "PendingAttestation"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def manifests() -> list[Path]:
    """Every register's day manifests, path-sorted. The glob is the register list, so a
    new register is anchored the night it starts writing snapshots — no list to update.
    The proof tree is skipped: it holds .ots files, not records."""
    found = {p for p in ROOT.glob("**/snapshots/*/manifest.json") if PROOFS not in p.parents}
    return sorted(found)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def proof_for(manifest: Path) -> Path:
    """anchors/<the manifest's own path>.ots — the mirror keeps the pairing obvious."""
    rel = manifest.relative_to(ROOT)
    return PROOFS / rel.parent / (rel.name + ".ots")


def ots(*args: str, timeout: int = 180) -> tuple[int, str]:
    """Run the client. Returns (returncode, combined output) — never raises on failure:
    a calendar that does not answer is a recorded outage, not a crash."""
    try:
        p = subprocess.run(("ots", *args), capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError:
        return 127, "ots client not installed"
    except subprocess.TimeoutExpired:
        return 124, f"ots {' '.join(args)} timed out after {timeout}s"


def state_of(proof: Path) -> tuple[str, str]:
    """(state, evidence) for an existing .ots: complete / pending / unreadable."""
    rc, out = ots("info", str(proof))
    if rc != 0 and COMPLETE_MARK not in out and PENDING_MARK not in out:
        return "unreadable", out.strip()[:400]
    if COMPLETE_MARK in out:
        # keep the block heights: they are the actual evidence of the date
        blocks = sorted({w for line in out.splitlines() if COMPLETE_MARK in line for w in line.split() if w.isdigit()})
        return "complete", f"bitcoin block(s) {', '.join(blocks)}" if blocks else "bitcoin attestation present"
    return "pending", f"{out.count(PENDING_MARK)} calendar promise(s), no block yet"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-network", action="store_true", help="only re-read the files on disk")
    args = ap.parse_args(argv)

    entries, failures = [], []
    stamped = upgraded = complete = pending = 0

    for m in manifests():
        proof = proof_for(m)
        rel = str(m.relative_to(ROOT))
        entry: dict = {"manifest": rel, "sha256": sha256(m)}

        if not proof.exists():
            if args.no_network:
                entry["state"] = "unstamped"
                entries.append(entry)
                continue
            rc, out = ots("stamp", str(m))
            beside = m.with_suffix(m.suffix + ".ots")  # the client writes next to the file
            if beside.exists():
                proof.parent.mkdir(parents=True, exist_ok=True)
                beside.replace(proof)
            if rc != 0 or not proof.exists():
                # An unstamped night is a disclosed gap, exactly like a source outage.
                failures.append({"manifest": rel, "step": "stamp", "at": now(), "detail": out.strip()[:400]})
                entry["state"] = "unstamped"
                entries.append(entry)
                continue
            entry["stamped_at"] = now()
            stamped += 1

        state, evidence = state_of(proof)
        if state == "pending" and not args.no_network:
            rc, out = ots("upgrade", str(proof))
            bak = proof.with_suffix(proof.suffix + ".bak")
            if bak.exists():
                bak.unlink()  # the client's backup is not part of the record
            state, evidence = state_of(proof)
            if state == "complete":
                entry["upgraded_at"] = now()
                upgraded += 1
            elif "not complete" not in out and rc not in (0, 1):
                failures.append({"manifest": rel, "step": "upgrade", "at": now(), "detail": out.strip()[:400]})

        entry["proof"] = str(proof.relative_to(ROOT))
        entry["state"] = state
        entry["evidence"] = evidence
        if state == "unreadable":
            # A proof the client cannot read is an outage, not a quietly odd row: it means
            # either the client is missing or the file is damaged, and both must be visible.
            failures.append({"manifest": rel, "step": "read", "at": now(), "detail": evidence})
        complete += state == "complete"
        pending += state == "pending"
        entries.append(entry)

    ledger = {
        "generated_at": now(),
        "what": "OpenTimestamps anchors for the registers' day manifests. Each manifest "
                "carries the SHA-256 of every preserved byte of its night, so one anchor "
                "covers the night. Proofs are pending until upgraded; a pending proof is a "
                "calendar's promise, a complete one stands on a Bitcoin block alone.",
        "proves": "the manifest's bytes existed no later than the attested block — not that "
                  "they are true, not that they came from the publisher they name, and not "
                  "that they did not exist earlier",
        "verify": "ots verify -f <manifest> <proof> — the -f is required because the proof "
                  "is stored apart from the file it commits to. The Bitcoin side needs a "
                  "Bitcoin node (--bitcoin-node); a block explorer is a third party, which "
                  "is the trust an anchor exists to remove",
        "why_proofs_live_apart": "an .ots is rewritten once, by `ots upgrade`, when the "
                                 "Bitcoin path arrives — so it cannot live inside the "
                                 "append-only record trees the I3 guard protects",
        "method": "docs/2026-08-09-opentimestamps-examination.md",
        "counts": {"manifests": len(entries), "complete": complete, "pending": pending,
                   "stamped_this_run": stamped, "upgraded_this_run": upgraded,
                   "failures": len(failures)},
        "failures": failures,
        "anchors": entries,
    }
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(ledger, indent=1, ensure_ascii=False) + "\n")

    print(f"anchors: {len(entries)} manifests · {complete} complete · {pending} pending "
          f"· +{stamped} stamped · +{upgraded} upgraded · {len(failures)} failure(s)")
    for f in failures:
        print(f"  ! {f['manifest']} ({f['step']}): {f['detail'].splitlines()[0] if f['detail'] else '—'}", file=sys.stderr)
    # A failed calendar is not a failed run: the registers are untouched either way.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
