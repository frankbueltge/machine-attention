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

Ethics, constitutive: the subject is the warning system and institutional
time — never the victims. No natural persons, no accusations, no risk
forecasts of our own. Sobriety is the register.

**Background project:** [state-before-interface](https://github.com/frankbueltge/state-before-interface)
(public AI procurement) keeps observing nightly and feeds the practice.

## Dark Ocean — V0, admitted 2026-08-09

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
`darkocean/`; **no stage presence until the project passes its
E-experiment** (admission path, stage 5). Origin:
[The Ghost Fleet](https://frankbueltge.de/ghost-fleet/), which keeps
running unchanged.

The **E-experiment runs 2026-08-09/10 → 2026-08-22/23, review 2026-08-24**;
its acceptance criteria were committed before the window opened and bind
from its first night —
[`docs/2026-08-09-dark-ocean-e-experiment-kriterien.md`](docs/2026-08-09-dark-ocean-e-experiment-kriterien.md).
Three outcomes are possible, not two: RUNNING as flagship, RUNNING as a
quiet instrument, or an honest RETIRED. The two readings already committed
(2026-08-07, 2026-08-08) predate the criteria and count as baseline
context, not as evidence.

## Layout

```
practice/                 shared substrate (fetch, preserve, autonomy) +
                          project runtimes (practice.foreknown,
                          practice.darkocean)
darkocean/snapshots/      preserved catalog pages + AIS samples (append-only)
darkocean/readings/       nightly Coverage-vs-Declaration records
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
