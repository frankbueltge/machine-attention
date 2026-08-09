# OpenTimestamps for the registers — examined, with a live stamp

**Date:** 2026-08-09 · **Decision:** D2 of the portfolio audit
(`frankbueltge.de/docs/design/2026-08-09-portfolio-audit.md` §7) — *"examine as a
build: a bare git history is a weaker evidentiary claim than a Bitcoin-anchored hash
of the publisher's checksums; cost ~zero, keyless, fits the ethic."*
**Status: examined and tested, not yet wired into any nightly run** — the scope
question in §6 is Frank's.

## 1. Why the question exists

Dark Ocean's claim is evidentiary: it preserves an archive's own checksummed
observation claims *on the day they were still online*, against an archive that
evicts. The strength of that claim rests entirely on **when** the preservation
happened — and today the only evidence of "when" is the repository's own git history.

Git commit dates are self-asserted. They are set by the committer's clock, can be
written to any value, and the whole history can be rewritten and force-pushed. What
git actually proves is **order and content**, not time. For a register whose point is
"we held this before it disappeared", that is the weak joint.

## 2. What OpenTimestamps is, verified live today

Verified by running it, not by reading about it. Client:
`opentimestamps-client` v0.7.2 from PyPI (`pip install opentimestamps-client`).

Target: a real Dark Ocean day manifest,
`darkocean/snapshots/2026-08-07/manifest.json`
(SHA-256 `e18dca3057a08f6a64e431a61e8249316c106a1e96771b82c2d056df5839f82b`).

```
$ ots stamp manifest.json
Submitting to remote calendar https://a.pool.opentimestamps.org
Submitting to remote calendar https://b.pool.opentimestamps.org
Submitting to remote calendar https://a.pool.eternitywall.com
Submitting to remote calendar https://ots.btc.catallaxy.com
→ manifest.json.ots, 665 bytes, 2.0 s wall clock
```

Measured properties:

- **Keyless and accountless.** No registration, no API key, no secret to store in
  Actions. Nothing to leak into a public archive.
- **Free.** The calendar servers aggregate many submissions into one Bitcoin
  transaction and pay the fee; no cost reaches the submitter. Both public OTS
  calendars answered and are healthy (v0.7.1, a few thousand pending commitments each).
- **Small and additive.** 665 bytes per stamp, sitting next to the file it commits to.
  Nothing about the register changes; nothing existing is rewritten.
- **Redundant by default.** Four independent calendars in one call — three operators,
  so one operator's disappearance does not destroy the proof.

## 3. The catch, measured

Immediately after stamping, the proof is **not yet a Bitcoin proof**:

```
$ ots verify manifest.json.ots
Calendar bob.btc.calendar.opentimestamps.org:   Pending confirmation in Bitcoin blockchain
Calendar finney.calendar.eternitywall.com:      Pending confirmation in Bitcoin blockchain
Calendar btc.calendar.catallaxy.com:            Pending confirmation in Bitcoin blockchain
Calendar alice.btc.calendar.opentimestamps.org: Pending confirmation in Bitcoin blockchain

$ ots upgrade manifest.json.ots
Failed! Timestamp not complete
```

A fresh `.ots` contains four *promises*. Until the calendars' aggregating transactions
confirm, the file's evidentiary value is "four independent services say they received
this hash" — better than nothing, and worse than Bitcoin. Turning the promise into a
proof requires **a second pass later**: `ots upgrade` fetches the Merkle path down to
the confirmed block and bakes it into the file, after which the proof stands alone and
needs no calendar ever again.

**Consequence for the design: anchoring is a two-phase commit.** Stamp on the night,
upgrade on a later night, commit the upgraded file. A design that stamps and commits
once, and never upgrades, ships permanently-pending proofs that still depend on
someone else's server — the failure mode worth naming in advance.

## 4. What it would prove — and what it would not

**Would prove:** the hash — and therefore the exact bytes of that day's manifest, and
through the manifest's SHA-256 entries, the exact preserved catalogue and AIS
documents — existed **no later than** a specific Bitcoin block. Independently
checkable by anyone, years later, without this repository, without GitHub, without the
machine, and without trusting the publisher's clock. It replaces "we say we held it on
the 7th" with "the Bitcoin blockchain shows this hash existed by the 9th".

**Would not prove:**

- *That the data is true.* A notarized lie is a notarized lie. This anchors possession
  in time, nothing else.
- *That it did not exist earlier.* An anchor is a ceiling on the existence time, never
  a floor. Nothing stops earlier possession, and nothing proves it either.
- *That the preserved bytes came from the archive.* The URL, HTTP status and retrieval
  time in the manifest are still the machine's own assertions. Anchoring makes those
  assertions **unrevisable after the fact**; it does not make them independently
  witnessed. The honest phrasing is "these are the claims this machine committed to
  by that block", not "this is what ESA published".
- *Anything, without a Bitcoin node.* The client checks the block header via a Bitcoin
  node (`--bitcoin-node`). Verifying without one means trusting a block explorer or a
  hosted verifier — the trust the anchor was meant to remove. A verify page must say
  which of the two the reader is doing.

## 5. How it would be built (if approved)

Two nightly steps, no secrets, no new service:

1. **stamp** — after the register's commit is prepared, `ots stamp` the day's
   `manifest.json`; commit `manifest.json.ots` alongside it.
2. **upgrade** — the same job, running over the last ~14 days of `.ots` files that
   are still incomplete: `ots upgrade --dry-run` to check, then upgrade and commit
   the ones that became complete. Idempotent, and self-healing after any outage
   (`.bak` files from the upgrade are not committed).

Failures are recorded like any other source outage: a calendar that does not answer
means that night's manifest is unstamped, and the record says so rather than the
pipeline retrying into silence. The manifest already contains the SHA-256 of every
preserved byte, so **one stamp per night covers the whole night's material** — no
per-file stamping.

**What must not be done:** the client's git integration
(`ots-git-gpg-wrapper`) timestamps *PGP signatures on commits*. The nightly commits are
made by an unsigned Actions identity, so that path does not apply — and it would
anchor the commit rather than the preserved bytes, which is the weaker object. Stamp
the manifest.

## 6. The open question — scope (Frank)

The audit named Dark Ocean and asked "possibly the other registers". The registers
this could cover, in descending order of how much the anchor adds:

| register | what an anchor adds |
|---|---|
| **Dark Ocean** (machine-attention) | the most — the claim *is* "held before eviction", against an archive that deletes |
| **The Foreknown** (machine-attention) | a lot — "the machine notarized what was knowable, when" is a timing claim, and `announced_at` never changing is currently a promise |
| **The Protocol / Parallax / Policy** (frankbueltge.de) | real but smaller — daily registers whose value is continuity; an anchor makes the "never backfilled" rule externally checkable |

My recommendation: **Dark Ocean and The Foreknown first** (one shared step in
machine-attention, where the timing claims are explicit), and the site's registers
only if the same step ports without new machinery. Anchoring everything at once buys
less than it costs in moving parts.

## 7. Verdict

**Worth building.** It is keyless, free, additive, small, needs no account and no
secret, and it repairs the one genuinely weak joint in an evidentiary register — that
its dates are currently self-asserted. The costs are two honest ones: proofs are
pending until upgraded, and full trustless verification wants a Bitcoin node. Both are
statable in one sentence each on a verify page, which is exactly the standard this
house holds itself to.

Nothing is wired up. The live stamp above was a test against a copy of a committed
manifest, made outside the repository; no `.ots` file has entered any register.
