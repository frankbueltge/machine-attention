# Discovery agenda — the pass's own working list

*Opened 2026-10-04 by the house, together with the pass's new mandate
(`docs/2026-10-04-discovery-neuer-auftrag.md`). From the next night on the
discovery pass keeps this file itself: every night it updates the stage, the
next step and the date of the candidate it worked on. Admission path:
`docs/2026-08-08-projekt-aufnahme.md` — EXPOSÉ → AUDIT → V0 → E-EXPERIMENT →
RUNNING (any time: RETIRED).*

## Focus

### The Interval — slow-onset food crises: projection against funding

- **Stage:** E-EXPERIMENT — **addendum 2026-10-17** (`docs/2026-10-17-the-interval-e-experiment-nachtrag.md`, held in `interval/experiment.json` under `addenda`): B6 base rate added (reported, no bar; `base_rate` in `experiment.py`, pre-window 43/77 placebo vs 3/7 onsets at FSC·date·k=2, all eight cells in the addendum), C clarified (no page, figure, number or data on the site; naming is not a stage), trial of the reading step in a throwaway copy (0 × 429, verify green, nothing committed). This answers the house's offer in `REQUESTS.md` of 2026-10-17; the criteria close after 2026-10-18. Criteria committed 2026-10-14, **before** the window (`docs/2026-10-14-the-interval-e-experiment-kriterien.md`, machine-readable `interval/experiment.json`, which carries the document's hash). V0 increments 1–6 done 2026-10-09 to 2026-10-14. Window: four ISO weeks without a gap, Mondays 2026-10-19, 10-26, 11-02, 11-09; closes 2026-11-15; review from 2026-11-16 is the maintainer's. The reading of 2026-10-13 is pre-window context. `verify.py` (`check_interval_experiment`) fails if the criteria postdate the window, the weeks are not four or more consecutive Mondays, or the prose changes without its hash. Tally: `python -m practice.interval.experiment --repo-root .` (counts A1–A3, B1, B2 from the readings; decides nothing).
- **Gate:** the maintainer's GO for V0 given on 2026-10-04 (wording private),
  recorded in `docs/2026-10-04-kandidat-the-interval.md`.
- **Sources:** IPC on HDX (CC0) and OCHA FTS, both keyless. **The FEWS NET data
  warehouse is not to be fetched** — its operator asks automated and AI clients not
  to (candidate document §2); asking FEWS NET for access is the maintainer's call (§7).
- **Next step:** none on the instrument until the window runs — the weekly workflow carries it. (2026-10-16 and 2026-10-18: checked, nothing due — the window opens Monday 2026-10-19; no criteria change landed on the last day.) Each Monday's pass runs the tally and notes B2, B4 and B6 in this file; nothing in the criteria moves after 2026-10-18. At 2026-11-16: a two-sentence review request in `REQUESTS.md`.
- **Open, no gate:** all eight drivers in `interval/drivers.json` are `unassigned` — no in-charter driver source is preserved yet; find one (public, keyless) before any driver is entered.
- **Updated:** 2026-10-18 (pass)

## Next

### Planetary Listening — "One Quarry, Two Records"

- **Stage:** V0, increment 3 done 2026-10-16 — the daily workflow
  `.github/workflows/planetary.yml` (06:40 UTC; test `practice/tests/test_planetary_workflow.py`
  holds the slot ≥ 30 min after every committed publisher `Updated`), documented in
  `docs/2026-10-16-planetary-listening-v0-inkrement-3.md`. Second reading
  `planetary/readings/2026-10-16.json` (day 2026-10-15): one strong impulse 07:31:49 UTC,
  STA/LTA 106 — again in the weekday band; first compared re-ingestion against 2026-10-15:
  0 events. Increment 2 (2026-10-15): nightly reader, publisher documents, re-ingestion as
  a compared event (`check_planetary_readings`). Increment 1 (2026-10-14): spike chose
  **Rüdersdorf**; Geseke parked (`planetary/declarations/geseke-2026-10-14.json`).
- **Gate:** the maintainer's GO of 2026-10-04 (wording private), audit recommendations
  taken for the open decisions. The audit's "Bewusst nicht" list binds V0.
- **Next step:** V0 increment 4 — the acceptance criteria as a committed file before any
  window. (2026-10-18: done — the workflow committed its first own reading,
  `planetary/readings/2026-10-17.json` in commit 934c970, so `planetary/readings` is now in
  `practice/src/practice/staleness.py`, labelled by run day, tested in
  `practice/tests/test_staleness.py`.)
- **Re-read when:** Geseke — if the operator page shows a forward date again, re-measure
  hearing there (pairing B would restore the second register, audit flagship condition d).
- **Substrate note:** after `pip install -e ./practice` module runs need no `PYTHONPATH`
  (checked 2026-10-16); without installation, `practice/` shadows the package.
- **Updated:** 2026-10-18 (pass)

### Synthetic Flood — how much of public language machines now write

- **Stage:** AUDIT done 2026-10-18 (`docs/2026-10-18-synthetic-flood-audit.md`, 26 probes with
  manifest in `syntheticflood/probes/2026-10-18/`): PubMed E-utilities counts carry Register A
  without storing a text (77–81 B per count, 3 req/s keyless); Wikipedia's container
  "Articles containing suspected AI-generated texts" has dated monthly subcategories (May 2025 to
  October 2026), one `allcategories` request reads all sizes — a standing backlog by tag month,
  not an inflow; OpenAlex keyless budget shared on the egress address (807 → 412 in seconds) and
  Crossref at 1 req/s are denominator controls only; Common Crawl unreachable from this container,
  not judged, not the axis. Both re-audit blockers cleared; recommendation: GO for a narrow V0.
  Exposé 2026-10-16 (axis and cadence), first exposé 2026-08-08, parked 2026-08-22, taken up again
  2026-10-04 with the maintainer's GO for V0 conditional on the audit.
- **Gate:** the conditional GO of 2026-10-04 (wording private); the pass's reading of it is put to
  the maintainer in `REQUESTS.md` (2026-10-18), silence through the next pass means proceed.
- **Next step:** V0 increment 1 — the committed word list and candidate pool, a reader for one
  cohort, the first reading of 2026-09 (M+1); Wikipedia requests with the contact user agent, one
  a day. Only after Planetary Listening increment 4, and only on a night the focus waits.
- **Updated:** 2026-10-18 (pass)

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
