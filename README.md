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

**Live:** https://frankbueltge.de/attention/ — published on frankbueltge.de
(Frank's decision, 2026-08-09), where the site pulls the committed stage build
nightly via its `attention-integrate` workflow. This repository builds
`public/` as the canonical, verified artifact; it does not deploy itself.

## Project 001 — The Foreknown

> An observatory of announced futures. The machine notarizes what was knowable,
> when — and measures the gap between warning and response while the clock is
> still running.

Design and source audit: [`docs/2026-08-09-foreknown-001-audit-und-entwurf.md`](docs/2026-08-09-foreknown-001-audit-und-entwurf.md).
Every night the notary reads the world's public warning feeds (V0: GDACS
hazard alerts, NOAA NHC cyclone forecasts — both keyless, audited 2026-08-09),
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

The funding axis (OCHA FTS response plans) is preserved daily, so the money's
movement between warning and event accumulates as a committed time series.

Ethics, constitutive: the subject is the warning system and institutional
time — never the victims. No natural persons, no accusations, no risk
forecasts of our own. Sobriety is the register.

**Background project:** [state-before-interface](https://github.com/frankbueltge/state-before-interface)
(public AI procurement) keeps observing nightly and feeds the practice.

## Layout

```
practice/                 shared substrate (fetch, preserve, autonomy) +
                          project runtimes (practice.foreknown)
foreknown/snapshots/      preserved bytes, manifests, run records (append-only)
foreknown/registry.json   the notary's ledger of announced futures
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
- **Discovery pass** — since 2026-08-09 a nightly cloud routine (06:30 UTC)
  in the maintainer's Claude UI, visible and manually startable there;
  `discovery.yml` stays as a manual fallback (`workflow_dispatch`, repo
  secret). No hard budget cap (decision 2026-08-09); every run appends to
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
python ../stage/generate.py --repo-root ..
python ../verify.py --repo-root ..
```

## Licensing

Code: Apache-2.0. Own texts: CC BY 4.0. Own derived data (registry, manifests,
run records): CC0. Preserved warning feeds remain documents of their issuers
(GDACS/EC-JRC, NOAA, UN OCHA — all public); source links, retrieval times and
hashes are kept with every copy.
