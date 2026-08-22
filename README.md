# machine attention

**A machine investigative practice.** One machine, built for autonomous, public,
data-intensive investigation and digital form-making — its attention, memory,
rejections, uncertainty and cost all public, all measured. No personas: internal
agents are ephemeral capabilities, fully attributed in the autonomy protocol.

The practice was designed as the counter-experiment to the research ecology at
frankbueltge.de and corrected on day one from a monitoring corridor to an open
practice — the reasoning lives in
[`docs/2026-08-08-korrektur-praxis-ueber-observatorium.md`](docs/2026-08-08-korrektur-praxis-ueber-observatorium.md).

## The stage

The public face is not documentation but a stage: monumental true statements,
real clocks, the ledger as fading traces. Every figure is a real system state;
quiet nights are shown as exactly that.

Since 2026-08-08 (late UTC) the work carries its four depths — depth on
demand, because evidence is infinite and attention is not:

- **ATTRACT** — `index.html`, the ten-second stage.
- **ENTER** — `future/<id>.html`, one dossier per announced future: its whole
  life from the record, every event anchored in a preserved snapshot, the
  world's reaction while it ran, the verdict once it closed.
- **INVESTIGATE** — `ledger.html`, the full register night by night — and
  what the machine itself has noticed (its observations and sensor
  proposals, with their promotion status).
- **VERIFY** — `verify.html`, where the claims meet the bytes: manifests,
  hashes, and the commands to re-run the chain.

All four levels are static, deterministic builds from the same committed
records, so `verify.py` covers them byte for byte — and "no dead ends" is a
test, not an intention.

**Live:** https://frankbueltge.de/attention/ — published on frankbueltge.de
(Frank's decision, 2026-08-08), where the site pulls the committed stage build
nightly via its `attention-integrate` workflow. This repository builds
`public/` as the canonical, verified artifact; it does not deploy itself.

## Project 001 — The Foreknown

> An observatory of announced futures. The machine notarizes what was knowable,
> when — and measures the gap between warning and response while the clock is
> still running.

Design and source audit: [`docs/2026-08-08-foreknown-001-audit-und-entwurf.md`](docs/2026-08-08-foreknown-001-audit-und-entwurf.md).
Every night the notary reads the world's public warning feeds (V0: GDACS
hazard alerts, NOAA NHC cyclone forecasts — both keyless, audited 2026-08-08),
preserves the original bytes with SHA-256 at the moment of issue, and folds
them into the registry of announced futures:

- **NOTARIZED** — first seen; `announced_at` is the retrieval time and never
  changes again.
- **REVISED** — window or severity changed; the original stays in the history.
- **CLOSED_BY_SOURCE / DISSIPATED** — the feed let go of it.
- **overdue** — the window passed but the warning is still fed: a flag worth
  watching, not an error.

Once a future closes, the **resolver** measures its verdict — derived from
committed records only, never from a model or a fresh fetch: alert episodes
get `EPISODE_ENDED` with duration, revision count and severity trajectory
(escalations Orange→Red are first-class); dissipated forecasts are matched
against the registry's own alert episodes — `MATERIALIZED_AS_ALERT` with the
measured lead time, or `NO_ALERT_MATCH`, which is a statement about the
record, not about the world. Cold-start bias is flagged per resolution.
Resolutions live in `foreknown/resolutions/` and are append-only.

### The reaction axis

Since 2026-08-08 each night also measures what moved while the clock was
still running — **money** (which OCHA/FTS 2026 response plans list the
warning's countries, what they ask for, what FTS reports as funded) and
**attention** (news volume from those countries against their own 28-day
median, from GDELT's daily raw files). The axis implements the machine's own
proposal `sensor-fts-country-coverage`, written by the first discovery pass
before any human had built it; the proposal's text was followed as written,
including its refusal to judge funding adequacy.

Readings live in `foreknown/reaction/`. What the numbers are not is carried
in every record, not appended as a footnote: plan totals are the plans'
annual figures for every country they list and are not attributable to the
hazard; attention is measured for the *country*, not the hazard. Design,
source probes and the honest limits:
[`docs/2026-08-08-reaktions-achse.md`](docs/2026-08-08-reaktions-achse.md).

### E1, reviewed 2026-08-22

The first end-to-end experiment **did not pass — on two of four criteria,
and both are build gaps, not findings**
([`docs/2026-08-22-foreknown-e1-review.md`](docs/2026-08-22-foreknown-e1-review.md)).
E1 asked for announced futures from at least three sources; there are 112 of
them, from two. It asked for one full cycle from warning to resolution
carrying a money and an attention time series; 15 resolutions exist and not
one of them carries either — while both have been measured per future
every night since 2026-08-08 and never joined to the resolution record. The
stage, the provenance verifier and the autonomy trace hold, and the honesty
criterion is met well past its minimum: of 15 resolutions, **none
materialized as an alert**.

The register's own headline says the rest. Of 97 source-open futures, **93
were already announced before this machine first looked** — 4 arose under
watch. A repeat window will therefore count closed cycles rather than nights,
and its criteria will be committed only after the third source and the
reaction join exist, not before.

Ethics, constitutive: the subject is the warning system and institutional
time — never the victims. No natural persons, no accusations, no risk
forecasts of our own. Sobriety is the register.

**Instrument:** [state-before-interface](https://github.com/frankbueltge/state-before-interface)
(public AI procurement) keeps observing nightly and feeds the practice. An instrument is a
full project of this practice with no stage claim — it may produce nothing for a long time,
and that is allowed. "Background project" was the wrong word for it and was dropped on
2026-08-09 when the house settled its vocabulary.

## Dark Ocean — instrument since 2026-08-22 (V0 admitted 2026-08-09)

> Ships tell the world where they are. Satellites can see where they
> actually are. The two views do not always agree.

Second investigation, at V0 of the admission path (audit:
[`docs/2026-08-08-dark-ocean-audit.md`](docs/2026-08-08-dark-ocean-audit.md),
Frank's GO in the autonomy protocol). **Coverage vs Declaration**, fully
keyless: each night the machine notarizes which Sentinel-1 acquisitions
covered which half-degree bins of the Baltic (catalog rows with the
issuer's own checksums — scene bytes are never fetched) against how the
declared ocean distributed itself in one agency AIS sample. Counts only,
no vessel identities; the per-moment axis (DMA day dumps) is probed
nightly and its outage recorded, never bridged. Records live in
`darkocean/`; there is no stage presence, and after the review of 2026-08-22
there will not be one. Origin:
[The Ghost Fleet](https://frankbueltge.de/ghost-fleet/), which keeps
running unchanged.

**Reviewed 2026-08-22: the E-experiment did not pass, and the stage
ambition ends here** —
[`docs/2026-08-22-dark-ocean-e-review.md`](docs/2026-08-22-dark-ocean-e-review.md),
against criteria committed before the window opened
([`docs/2026-08-09-dark-ocean-e-experiment-kriterien.md`](docs/2026-08-09-dark-ocean-e-experiment-kriterien.md)).
Two things failed, and only one of them was bad luck. The sample-hour
criterion became unreachable after two nights were lost to a deadlock in
this repository's own machinery and two repair runs pulled their samples
hours off schedule — at most 10 of the required 12 disciplined nights
remained, an arithmetic that was computed and committed on 2026-08-14, eight
days before the review. The structural failure weighs more: the per-moment
declared axis never arrived. DMA's day dumps were unreachable on every one of
the 13 nights on record, so the headline number stayed a statement about
receiver geography and one sampling instant, and the strongest true sentence
after the window was that two registers overlap and one of them never
contradicts itself.

That sentence is an instrument reading, not a stage moment — which the
criteria had said in advance, in the negative, so that it would bite. So the
**continuity notary keeps running as an instrument**: every night it asks a
public archive whether it still says what it said, keyless, at no cost, with
**0 divergences in 3,571 re-asked catalog rows** over 11 nights. That null is
carried in the practice's export, not left implicit in a green run. The
built draft stays under `darkocean/draft/`, `noindex`, as a dated artefact of
the window; nothing is deleted, nothing is backfilled. The two pre-window
readings (2026-08-07, 2026-08-08) never counted as evidence.

## Memory Hole — V0, admitted 2026-08-15

> What does power change about its own public past?

Third investigation, at V0 of the admission path (audit:
[`docs/2026-08-14-memory-hole-audit.md`](docs/2026-08-14-memory-hole-audit.md),
Frank's GO on 2026-08-15). **The institutional wording, rechecked**, fully
keyless: each night one proven CDX query per institution asks the Internet
Archive which pages of that host it touched on the completed UTC day —
domain scope, many pages of few institutions, not a longer curated list.
A deterministic sample of those pages is read back, every capture passes a
validity gate before it may mean anything (challenge pages, consent banners
and bot-walls are counted as `unverifiable` and never diffed), the text diff
is typed by versioned rules into operations on text — `number_revised`,
`date_shifted`, `negation_flipped`, `commitment_removed`,
`attribution_removed` — and every deletion candidate is rechecked live before
the word "gone" appears. A model layer runs only where the rules abstain,
capped at 40 classifications a night, batched, every verdict marked as an
estimate; without a key it says so and the night proceeds.

**Acceptance criteria committed 2026-08-22** —
[`docs/2026-08-22-memory-hole-e-experiment-kriterien.md`](docs/2026-08-22-memory-hole-e-experiment-kriterien.md).
They arrive seven days late: the nightly readings started on 2026-08-13
without a declared window, so **those eight nights count as context, not as
evidence**, the same discipline Dark Ocean applied to its own pre-window
nights. The window does not open on the criteria's date either — three
build conditions come first, each one a lesson from the review published the
same day: the two deletion-detection bugs this project found in its own
origin get fixed there first; the archive fetch gets retry discipline and
proves three consecutive nights of real sample pairs, because otherwise every
yield number measures the Wayback Machine's availability instead of an
institution's behaviour; and the semantic layer's verdict route produces one
committed file, because a criterion about rules-versus-model cannot be
measured while no verdict exists. The yield bar (≥ 4 nights of 14 with a
validated semantic event) stays exactly where the audit put it, although the
eight context nights suggest it will be missed — lowering a threshold in
the knowledge of the data is the moving bar that just cost the sibling
project its stage.

Records live in `memoryhole/`; no stage presence until the project passes its
E-experiment (admission path, stage 5). Origin:
[Editorial Deadline / The Redaction](https://frankbueltge.de/redaction/),
which keeps running unchanged — Memory Hole doubles none of its 32 pages.

## Layout

```
practice/                 shared substrate (fetch, preserve, autonomy) +
                          project runtimes (practice.foreknown,
                          practice.darkocean, practice.memoryhole)
darkocean/snapshots/      preserved catalog pages + AIS samples (append-only)
darkocean/readings/       nightly Coverage-vs-Declaration records
memoryhole/watchlist.json institutions and control pages, each with the live
                          probe that justifies its query strategy
memoryhole/snapshots/     preserved CDX answers + archived pages (append-only)
memoryhole/readings/      nightly records of the institutional wording
foreknown/snapshots/      preserved bytes, manifests, run records (append-only)
foreknown/registry.json   the notary's ledger of announced futures
foreknown/resolutions/    measured verdicts for closed futures (append-only)
foreknown/reaction/       money and attention per announced future (derived)
foreknown/proposals/      discovery output: observations, sensor & source proposals
autonomy/log.jsonl        the autonomy protocol (append-only, no aggregate score)
stage/generate.py         builds public/ deterministically from committed records
public/                   the committed stage build
verify.py                 walks the provenance chain backwards; CI gate
discovery/PROMPT.md       the nightly discovery pass (the intelligence layer)
```

## Operations

- `sentinel.yml` — nightly notary run (05:45 UTC), commits as
  `Machine Attention <attention@machine-attention.invalid>`.
- `darkocean.yml` — nightly Coverage-vs-Declaration reading (04:50 UTC),
  same machine identity.
- `memoryhole.yml` — nightly reading of the institutional wording (02:30 UTC,
  early because the archive is slow: the audit budgets one to three hours),
  same machine identity. Optional `ANTHROPIC_API_KEY` for the capped model
  layer; without it the reading records `off: no key configured`.
- **Discovery pass** — since 2026-08-08 a nightly cloud routine (06:30 UTC)
  in the maintainer's Claude UI, visible and manually startable there;
  `discovery.yml` stays as a manual fallback (`workflow_dispatch`, repo
  secret). No hard budget cap (decision 2026-08-08); every run appends to
  the autonomy protocol — for routine runs the token usage lives in the
  Claude UI and the log entry says so.
- `ci.yml` — tests + `verify.py` + append-only guard.
- `automerge.yml` — discovery deliveries merge themselves once CI is green.
- Publishing: frankbueltge.de pulls `public/` nightly (no deployer here —
  the site's Cloudflare Pages deploy is the single deployer).

Local:

```bash
cd practice && python -m pip install -e '.[dev]' && python -m pytest
python -m practice.foreknown.run --repo-root ..
python -m practice.foreknown.reaction --repo-root .. --backfill 3
python ../stage/generate.py --repo-root ..
python ../verify.py --repo-root ..
```

## Licensing

Code: Apache-2.0. Own texts: CC BY 4.0. Own derived data (registry, manifests,
run records): CC0. Preserved warning feeds remain documents of their issuers
(GDACS/EC-JRC, NOAA, UN OCHA — all public); source links, retrieval times and
hashes are kept with every copy.
