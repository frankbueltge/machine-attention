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
- **Next step:** none on the instrument until the window runs — the weekly workflow carries it. (2026-10-16: checked, nothing due — the window opens Monday 2026-10-19.) Each Monday's pass may run the tally and note B2/B4 in this file; nothing in the criteria moves after 2026-10-18. At 2026-11-16: a two-sentence review request in `REQUESTS.md`.
- **Open, no gate:** all eight drivers in `interval/drivers.json` are `unassigned` — no in-charter driver source is preserved yet; find one (public, keyless) before any driver is entered.
- **Updated:** 2026-10-14 (pass)

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
- **Next step:** once the workflow has committed its first reading itself (expected
  2026-10-17), add `planetary/readings` to `practice/src/practice/staleness.py`. Then
  V0 increment 4: the acceptance criteria as a committed file before any window.
- **Re-read when:** Geseke — if the operator page shows a forward date again, re-measure
  hearing there (pairing B would restore the second register, audit flagship condition d).
- **Substrate note:** after `pip install -e ./practice` module runs need no `PYTHONPATH`
  (checked 2026-10-16); without installation, `practice/` shadows the package.
- **Updated:** 2026-10-16 (pass)

### Synthetic Flood — how much of public language machines now write

- **Stage:** EXPOSÉ, refreshed 2026-10-16 (`docs/2026-10-16-synthetic-flood-expose-achse.md`):
  the axis is named — Register A, PubMed abstracts in monthly cohorts with the excess-vocabulary
  method as a neighbour (a committed word list beside a freshly derived one; their divergence is
  the method's decay); Register B, counts of Wikipedia's own maintenance category for suspected
  machine-written text (counts only, no titles, no user names). No GDELT, so the Consensus
  duplication falls away on paper (blocker 1). Cadence (blocker 2): each cohort read at M+1, M+2,
  M+3, revisions as compared events, an acceptance window of at least six cohorts. Common Crawl is
  not the axis. First exposé 2026-08-08, parked 2026-08-22, taken up again on the maintainer's
  wish of 2026-10-04 (wording private); his GO for V0 is given in advance, on the condition that
  the AUDIT clears both blockers.
- **Next step:** the AUDIT — live probes of PubMed E-utilities, OpenAlex, Crossref, the MediaWiki
  API and the Common Crawl index (endpoint, status, size, rate limit without key, licence of
  metadata and abstract texts, charter fit), samples with manifests under
  `syntheticflood/probes/<date>/`, ending in a recommendation (exposé §7). Only on a night the
  focus waits.
- **Updated:** 2026-10-16 (pass)

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
