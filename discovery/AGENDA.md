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
- **Next step:** none on the instrument until the window runs — the weekly workflow carries it. (2026-10-16 and 2026-10-18: checked, nothing due — the window opens Monday 2026-10-19; no criteria change landed on the last day.) **2026-10-19, week 1:** at 06:38 UTC the week's reading was not yet on main and `interval.yml` lists no run at all yet — its first scheduled firing; the planetary workflow, scheduled 06:40, ran at 11:08 and 11:39 on 10-17/10-18, so a delay of hours is the platform's norm. Tally at pass time: A1 missing 2026-10-19 (not yet run), A2 none, A3 none, B1 0 moves, B2 no change, B6 unchanged from the addendum (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). A run any day of ISO week 43 still counts; if none has landed by 2026-10-21 a `workflow_dispatch` is asked for in `REQUESTS.md` (2026-10-19). **Second pass 2026-10-19 (evening):** the week-1 reading landed (`interval/readings/2026-10-19.json`, workflow run 10:20 UTC per `autonomy/log.jsonl`); tally A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 unchanged — the request of the morning is closed as moot. Next Monday 2026-10-26: B2, B4, B6 for weeks 1–2. Each Monday's pass runs the tally and notes B2, B4 and B6 in this file; nothing in the criteria moves after 2026-10-18. At 2026-11-16: a two-sentence review request in `REQUESTS.md`.
- **Open, no gate:** all eight drivers in `interval/drivers.json` are `unassigned` — no in-charter driver source is preserved yet; find one (public, keyless) before any driver is entered.
- **Updated:** 2026-10-19 (pass)

## Next

### Planetary Listening — "One Quarry, Two Records"

- **Stage:** E-EXPERIMENT — criteria committed **2026-10-19, before the window** (V0 increment 4):
  `docs/2026-10-19-planetary-listening-e-experiment-kriterien.md`, machine-readable
  `planetary/experiment.json` (carries the document's hash), tally
  `python -m practice.planetary.experiment --repo-root .`
  (`practice/src/practice/planetary/experiment.py`, tests `practice/tests/test_planetary_experiment.py`),
  `verify.py` `check_planetary_experiment` fails if the criteria postdate the first night, the window is
  shorter than the audit's 14 nights, A4 exceeds 400 KB or the prose changes without its hash.
  Window: 14 nights, readings 2026-10-21 to 2026-11-03 (days 10-20 to 11-02); closes 2026-11-03; review
  from 2026-11-04 is the maintainer's. Addenda allowed until 2026-10-20. Pass = A1 (≥ 13/14, never two
  in a row missing) · A2 (≤ 1 failed night) · A3 (0 × 429) · A4 (≤ 400 KB a night) · A5 (verify green)
  · B6 (detector unchanged) · C (no class word, no person, no stage); B1–B5 reported. **B4, the clock
  test:** Germany leaves summer time on 2026-10-25; the weekday impulse sat at 07:31 UTC (09:31 CEST,
  `planetary/readings/2026-10-15.json`, `2026-10-16.json`). Median shift of each weekday's first strong
  impulse: `local` if 60 ± 10 min, `utc` if 0 ± 10, else `neither` — expectation `local`, reported, no
  bar. **Known before the window:** on both workflow runs (10-17, 10-18, ~11:00 UTC) availability and
  WFCatalog for the read day answered 204 — the publisher's index then ended one day short
  (`planetary/snapshots/2026-10-17/GE.RUE.HHZ/extent.txt`, `2026-10-18/…`); B1 counts it, `nightly.py`
  is deliberately not changed before the window. V0 increments 1–3 done 2026-10-14 to 2026-10-16.
- **Gate:** the maintainer's GO of 2026-10-04 (wording private), audit recommendations
  taken for the open decisions. The audit's "Bewusst nicht" list binds V0.
- **Next step:** none on the instrument once the window opens; 2026-10-20 is the last day for a dated
  addendum. From 2026-10-26 the pass notes B4 (first after-shift weekday). At 2026-11-04: a two-sentence
  review request in `REQUESTS.md`.
- **Repair 2026-10-19 (second pass), before the window:** the workflow slot moved 06:40 → 08:10 UTC
  (`.github/workflows/planetary.yml`) — `planetary/readings/2026-10-19.json` carries publisher
  `Updated 06:22:02Z`, inside the 30-minute margin, and `test_planetary_workflow.py` was red on main.
  Criteria count dates, not hours (criteria §4.2); detector and `nightly.py` untouched (B6).
- **Re-read when:** Geseke — if the operator page shows a forward date again, re-measure
  hearing there (pairing B would restore the second register, audit flagship condition d).
- **Substrate note:** after `pip install -e ./practice` module runs need no `PYTHONPATH`
  (checked 2026-10-16); without installation, `practice/` shadows the package.
- **Updated:** 2026-10-19 (pass)

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
- **Stage now:** V0 increment 1 done 2026-10-19 (second pass,
  `docs/2026-10-19-synthetic-flood-v0-inkrement-1.md`): `syntheticflood/wordlists/wordlist-v1.json`
  (47 fixed, 20 controls, 99 pool; immutable, a change is a new version), reader
  `practice/src/practice/syntheticflood/` (`cohort.py`, `pubmed.py`, `wordlist.py`), tests
  `practice/tests/test_syntheticflood.py`, `verify.py` `check_syntheticflood` (counts only, every
  query rebuilt, every count bound to the SHA-256 of its canonical answer). First reading
  `syntheticflood/readings/2026-09/2026-10-19.json`: cohort 2026-09 at M+1, 165 555 abstracts
  (165 058 at the audit a day earlier — revision already visible), 167 requests, 0 × 429.
- **Next step:** V0 increment 2 — Register B, one daily `allcategories` request with the contact user
  agent, sizes of the dated subcategories only, reader and verifier. Then increment 3: the 2018–2022
  baseline (retrospective readings) and the stability test of every fixed word. No workflow before.
  Only on nights the focus waits.
- **Updated:** 2026-10-19 (second pass)

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
