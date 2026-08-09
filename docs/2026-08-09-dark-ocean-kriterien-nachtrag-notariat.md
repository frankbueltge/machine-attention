# Dark Ocean E-experiment — proposed addendum: the notarial act

> **ACCEPTED 2026-08-09, by the session holding the attention lane (Frank's standing
> delegation this afternoon). Group N is part of the criteria from night 1; the chosen
> route is option 1 — N1 is built and verified before the window opens, and if the build
> does not verify today, option 3 (delay the window) applies. Option 2 is excluded.
> The language rule of §6 is decided: working documents German, anything that can become
> public copy English. Recorded in the criteria document's §0 and in the autonomy
> protocol. — Whoever picks this up next: N1 is being built in this session; check
> `git log darkocean/` before starting it a second time.**

**Date:** 2026-08-09 · **Status: proposal, not a change.** The criteria committed today
(`2026-08-09-dark-ocean-e-experiment-kriterien.md`) bind as written; its §0 allows a
dated addendum with reasons until the window opens (night 1 = run 04:50 UTC on
2026-08-10). This is that addendum, offered for Frank's decision.

**Where it comes from:** decision D1 of the portfolio audit
(`frankbueltge.de/docs/design/2026-08-09-portfolio-audit.md` §4/§7) — reposition Dark
Ocean so the *notarial act* is the claim and the per-bin counts are its demonstration,
**before the criteria are fixed, so that the criteria measure the right thing.** The
positioning itself now lives in [`darkocean/METHOD.md`](../darkocean/METHOD.md).

## 1. The gap

The committed criteria are strong on operations (A), on the overlap statistics (B), on
stage-worthiness (C), on honesty (D) and on the charter (E). Read against the audit
verdict, one thing is missing: **nothing in A–E measures the notarial act.**

That matters because the audit was explicit about where this register wins and loses.
As a measurement of maritime reality, the per-bin overlap counts are a degraded subset
of what Global Fishing Watch already publishes — read that way, V0 loses. The daylight
is the preservation act: the publisher's own checksummed claims, held daily, keylessly,
append-only, verified by a second implementation, with detection refused. B1–B4 measure
the demonstration; the claim itself goes unmeasured. And C4, by naming *"two registers
overlap by about X %"* as the sentence that would send the project to Instrument, makes
the overlap rate the implicit headline — the exact framing the audit warned against.

## 2. Why this is not a documentation problem

Verified against the live catalogue on 2026-08-09:

- The 42 products of the 2026-08-07 reading: **all `online: true`, all
  `EvictionDate 9999-12-31`.**
- Every Baltic S1 GRD product of a day two years earlier (2024-08-07, 51 products):
  **51 × online, 51 × `9999-12-31`.**

Copernicus is not evicting this material and announces no date at which it will. The
eviction premise is therefore **structural, not observed** — which is defensible, and
must be said rather than implied.

- `run.py` writes the day it just read and **never reads an earlier reading.** There
  is no look-back, so no `online` transition, no appearing `EvictionDate` and no
  checksum change can ever be caught. As the register stands, the notarial act is
  **structurally unmeasurable** — not merely unmeasured.
- The look-back is cheap and keyless: `GET /odata/v1/Products(<id>)` returns the
  current `Name`, `Online`, `EvictionDate`, `PublicationDate` and `ModificationDate`
  without any account (verified today against a product from the 2026-08-07 reading).

So the fix is a small nightly step, not a new data source — but it is a **build**, and
it has to exist before the window if the window is to measure it.

## 3. Proposed criteria group N — the notarial act

| # | Criterion |
|---|---|
| N1 | **Continuity probe committed:** each night re-probes every product recorded in the window so far (and the two pre-window nights) by catalogue Id, and commits `online`, `eviction_date`, `modification_date` and the publisher's checksums **as they stand that night** — not as they were first seen. Cost: one keyless request per product, a few hundred per night by the window's end |
| N2 | **Divergence is a headline, not an error:** any product that goes offline, gains a real `EvictionDate`, changes `ModificationDate`, or whose checksums no longer match what was preserved, is committed as a **catch** with both values side by side. A checksum change is never silently reconciled to the newer value |
| N3 | **The negative counts as a result:** if no divergence occurs in 14 nights, the review commits the sentence plainly — *n products held, m re-probes, zero divergences observed; the preservation claim rests on the mechanism, not yet on an event.* An empty catch list is a finding, not a failed criterion |
| N4 | **The window's headline sentence is about the act, not the rate.** C4 stays as written for the overlap rate; N4 adds its counterpart: a true sentence of the form *"this machine holds the archive's own checksummed claims for N days of the Baltic, re-checked nightly, and here is what changed"* is a stage moment even at zero divergences — because the subject is the register, not the sea |

**Consequential edit to the existing text, if N is accepted:** B1's "Kennzahl" and C4's
example sentence stay valid but are no longer the only candidates for the window's
headline. Nothing in A, B, D or E is weakened.

## 4. The cost of accepting it — stated, because it is not free

N1 is a build against a live source, and night 1 begins at 04:50 UTC on 2026-08-10.
Three honest options:

1. **Build N1 before the window opens** — the probe is small (one OData call per
   recorded product, the existing keyless client, the existing manifest/preserve path),
   but it is untested code entering a nightly run, and it needs its `verify.py` side.
2. **Open the window on time and let N join at a named night** — the criteria's §0
   binding is then partially retrofitted, which is precisely the discipline §0 exists
   to protect. Acceptable only if the addendum says so up front: *N applies from night
   k, the first k−1 nights carry no continuity data, and the review states it.*
3. **Delay the window by the days the build needs** — cleanest measurement, costs
   calendar time, and moves the review past 2026-08-24.

**Recommendation: option 3 if the build cannot be finished and verified today, option 1
if it can.** Option 2 is the one that quietly weakens the thing the criteria document
was written to prevent — a moving bar — and should be chosen deliberately or not at all.

## 5. What this addendum does not touch

The three open questions in the criteria document's §7 (the C bar, the three-way
outcome, whether the two pre-window nights count) — those stay exactly as put to Frank.
The V1 detection path, the Earth Engine question and the region are likewise untouched.

## 6. A note on language

This addendum and `darkocean/METHOD.md` are written in English, matching the
repository's README and the ecology's English-only rule; the criteria document they
attach to is German. Worth a deliberate decision by whoever owns this lane rather than
a drift — the method sheet in particular is the text that becomes public copy if Dark
Ocean reaches the stage.
