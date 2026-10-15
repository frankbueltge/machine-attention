# Discovery agenda — the pass's own working list

*Opened 2026-10-04 by the house, together with the pass's new mandate
(`docs/2026-10-04-discovery-neuer-auftrag.md`). From the next night on the
discovery pass keeps this file itself: every night it updates the stage, the
next step and the date of the candidate it worked on. Admission path:
`docs/2026-08-08-projekt-aufnahme.md` — EXPOSÉ → AUDIT → V0 → E-EXPERIMENT →
RUNNING (any time: RETIRED).*

## Focus

### The Interval — slow-onset food crises: projection against funding

- **Stage:** E-EXPERIMENT — criteria committed 2026-10-14, **before** the window (`docs/2026-10-14-the-interval-e-experiment-kriterien.md`, machine-readable `interval/experiment.json`, which carries the document's hash). V0 increments 1–6 done 2026-10-09 to 2026-10-14. Window: four ISO weeks without a gap, Mondays 2026-10-19, 10-26, 11-02, 11-09; closes 2026-11-15; review from 2026-11-16 is the maintainer's. The reading of 2026-10-13 is pre-window context. `verify.py` (`check_interval_experiment`) fails if the criteria postdate the window, the weeks are not four or more consecutive Mondays, or the prose changes without its hash. Tally: `python -m practice.interval.experiment --repo-root .` (counts A1–A3, B1, B2 from the readings; decides nothing).
- **Gate:** the maintainer's GO for V0 given on 2026-10-04 (wording private),
  recorded in `docs/2026-10-04-kandidat-the-interval.md`.
- **Sources:** IPC on HDX (CC0) and OCHA FTS, both keyless. **The FEWS NET data
  warehouse is not to be fetched** — its operator asks automated and AI clients not
  to (candidate document §2); asking FEWS NET for access is the maintainer's call (§7).
- **Next step:** none on the instrument until the window runs — the weekly workflow carries it. (2026-10-15: checked, nothing due — the window opens Monday 2026-10-19.) Each Monday's pass may run the tally and note B2/B4 in this file; nothing in the criteria moves after 2026-10-18. At 2026-11-16: a two-sentence review request in `REQUESTS.md`.
- **Open, no gate:** all eight drivers in `interval/drivers.json` are `unassigned` — no in-charter driver source is preserved yet; find one (public, keyless) before any driver is entered.
- **Updated:** 2026-10-14 (pass)

## Next

### Planetary Listening — "One Quarry, Two Records"

- **Stage:** V0, increment 2 done 2026-10-15 — the nightly T+1 reading for GE.RUE
  (`docs/2026-10-15-planetary-listening-v0-inkrement-2.md`, module
  `practice/src/practice/planetary/nightly.py`, first reading
  `planetary/readings/2026-10-15.json`, snapshot `planetary/snapshots/2026-10-15/`).
  Day 2026-10-14 (Wed): one strong impulse 07:31:34 UTC, STA/LTA 153 — inside the
  spike's weekday band; ISC 204, USGS 0. Publisher documents preserved verbatim
  (availability `Updated`, extent, WFCatalog); re-ingestion is now a compared event
  (`segment_rewritten` / `_gone` / `_inserted`), recomputed by `verify.py`
  (`check_planetary_readings`). Tonight is the baseline; the four closed extent
  segments carry the same `Updated` as in the audit of 2026-08-22.
  Increment 1 (2026-10-14): the spike chose **Rüdersdorf**; Geseke parked (operator
  calendar silent 412 days, `planetary/declarations/geseke-2026-10-14.json`; GR.KAST
  did not separate declared from control days).
- **Gate:** the maintainer's GO of 2026-10-04 (wording private), audit recommendations
  taken for the open decisions. The audit's "Bewusst nicht" list binds V0.
- **Next step:** V0 increment 3 — the daily workflow `.github/workflows/planetary.yml`
  (after ~06:00 UTC; the publisher's `Updated` tonight was 05:14:43), running
  `practice.planetary.nightly`, `tools/anchor.py --register`, `verify.py`, commit. Then
  the acceptance criteria as a committed file before any window.
- **Re-read when:** Geseke — if the operator page shows a forward date again, re-measure
  hearing there (pairing B would restore the second register, audit flagship condition d).
- **Substrate note:** from the repo root, `practice/` shadows the installed package;
  module runs there need `PYTHONPATH=practice/src`.
- **Updated:** 2026-10-15 (pass)

### Synthetic Flood — how much of public language machines now write

- **Stage:** EXPOSÉ (2026-08-08), parked 2026-08-22; **taken up again on the
  maintainer's wish of 2026-10-04** (wording private). His GO for V0 is given in
  advance, on the condition that the AUDIT clears the two blockers below.
- **Blockers to clear first** (re-audit of 2026-08-22, §3): (1) an axis that is
  not GDELT — the GDELT part would duplicate The Consensus on the house's site;
  (2) the headline figure is a share that drifts monthly, so the measurement and
  its acceptance window must be built for that cadence, not for fourteen nights.
- **Keyless, cost-free axes to probe** (named by the house, unchecked): science
  abstracts via OpenAlex, Crossref or PubMed E-utilities, using the published
  "excess vocabulary" method as a neighbour, not a copy; Wikipedia's own tagging of
  suspected machine-written text, counted through the MediaWiki API; Common Crawl
  read over HTTPS (index.commoncrawl.org, data.commoncrawl.org), with no AWS
  account involved. Every claim about these is the audit's to make.
- **When:** on nights the focus waits — a refreshed EXPOSÉ that names the axis,
  then the AUDIT. Notes at the end of `docs/2026-08-08-kandidat-synthetic-flood.md`.
- **Updated:** 2026-10-04 (house)

## Parked

### Compute Ground

- **Blocker:** no machine-readable permit registers, and no thesis on form (same
  re-audit, §3).

## Retired

### Dark Ocean

- **Retired:** 2026-10-04, last night 2026-10-03 (`darkocean/RETIRED.json`,
  `docs/2026-10-04-dark-ocean-retired.md`). Its workflow is removed; nothing here
  restarts it.

### The Foreknown

- **Retired:** 2026-10-04, last night 2026-10-03 (`foreknown/RETIRED.json`). The
  record is an archive; nothing here restarts it.
