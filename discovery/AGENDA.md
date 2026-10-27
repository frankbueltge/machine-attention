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
- **Next step:** none on the instrument until the window runs — the weekly workflow carries it. (2026-10-16 and 2026-10-18: checked, nothing due — the window opens Monday 2026-10-19; no criteria change landed on the last day.) **2026-10-19, week 1:** at 06:38 UTC the week's reading was not yet on main and `interval.yml` lists no run at all yet — its first scheduled firing; the planetary workflow, scheduled 06:40, ran at 11:08 and 11:39 on 10-17/10-18, so a delay of hours is the platform's norm. Tally at pass time: A1 missing 2026-10-19 (not yet run), A2 none, A3 none, B1 0 moves, B2 no change, B6 unchanged from the addendum (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). A run any day of ISO week 43 still counts; if none has landed by 2026-10-21 a `workflow_dispatch` is asked for in `REQUESTS.md` (2026-10-19). **Second pass 2026-10-19 (evening):** the week-1 reading landed (`interval/readings/2026-10-19.json`, workflow run 10:20 UTC per `autonomy/log.jsonl`); tally A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 unchanged — the request of the morning is closed as moot. Next Monday 2026-10-26: B2, B4, B6 for weeks 1–2. **2026-10-20:** nothing due (Tuesday; week 1 is read). **2026-10-21:** nothing due (Wednesday); tally unchanged — A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 43/77 vs 3/7 at FSC·date·k=2. **2026-10-22:** nothing due (Thursday); tally unchanged — A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change (morning, second and fourth pass). **2026-10-23:** nothing due (Friday); `REQUESTS.md` (2026-10-22) unanswered, so the driver entries stay after 2026-11-15 (checked again in the second pass, unchanged). **2026-10-24:** nothing due (Saturday); `REQUESTS.md` (2026-10-22) still unanswered. Second pass (18:5x UTC): tally unchanged — A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change; `REQUESTS.md` (2026-10-22) still unanswered. **2026-10-25:** nothing due (Sunday, last day of week 1); tally unchanged — A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, weeks due 1 of 4; `REQUESTS.md` (2026-10-22) still unanswered, so the driver entries stay after 2026-11-15. Monday 2026-10-26 is week 2. **2026-10-26 (06:4x UTC), week 2 (ISO week 44):** the week's reading is not yet on main — week 1's ran at 10:20 UTC, so the tally lists 2026-10-26 as missing at pass time only (A1 missing 2026-10-26, not yet run; weeks due 2 of 4). A2 pass, A3 none, B1 0 moves, B2 no change across weeks 1–2 (one reading in the window so far, 8 episodes), B4 not yet computable (needs week 2's reading), B6 unchanged from the addendum (FSC·date·k=2: 43/77 placebo vs 3/7 onsets; all eight cells as in `interval/experiment.json`). A run any day of ISO week 44 counts; if none has landed by 2026-10-28 a `workflow_dispatch` is asked for in `REQUESTS.md`. `REQUESTS.md` (2026-10-22) still unanswered, so the driver entries stay after 2026-11-15. **2026-10-27 (06:3x UTC):** week 2's reading landed (`interval/readings/2026-10-26.json`, commit `3a71f48`, workflow 10:35 UTC per `autonomy/log.jsonl`). Tally: weeks due 2 of 4, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change (8 episodes both weeks), B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). **B4, weeks 1–2: no violation** — the four open cells (AFG 2025-10 and SOM 2026-01, fsc and total) changed between the two readings only in flow counts (AFG fsc 351→356, total 2951→2975; SOM fsc 278→279, total 1504→1533), each with new preserved pages under `interval/snapshots/2026-10-26/fts/` and new hashes in `interval/register.json`; `t1` unchanged, IPC snapshot unchanged (`status: unchanged`). `REQUESTS.md` (2026-10-22) still unanswered, so the driver entries stay after 2026-11-15. Monday 2026-11-02 is week 3. Each Monday's pass runs the tally and notes B2, B4 and B6 in this file; nothing in the criteria moves after 2026-10-18. At 2026-11-16: a two-sentence review request in `REQUESTS.md`.
- **Open, no gate:** all eight drivers in `interval/drivers.json` are `unassigned`. **Driver-source audit done 2026-10-22 (third pass)** (`docs/2026-10-22-the-interval-treiber-quelle-audit.md`, 7 probes in `interval/probes/2026-10-22/manifest.json`): ipcinfo.org 403 (browser check page, not reachable keyless), ReliefWeb API 403 (approved appname required — outside the charter), HDX "hunger hotspots" 0 datasets; **the Global Report on Food Crises database on HDX** (package `fsin-grfc`, CC BY, `grfc_afi_database_2016-2025_september_update.xlsx`, 197 955 B, preserved) carries `Primary/Secondary/Tertiary driver` per country × reference year 2016–2025 — inside the charter. Recommendation: rule `drivers-grfc-v1` (row of t0's year, latest edition; primary driver → `conflict`/`economic`/new value `weather`, never `drought`; secondaries kept verbatim; no row → `unassigned`, so SOM 2026-01 stays unassigned). The rows were read in the audit (disclosed: the rule is not blind). Whether drivers enter inside the window is put in `REQUESTS.md` (2026-10-22); silence means: rule as tested code first, entries after 2026-11-15. **Rule as code done 2026-10-22 (fourth pass)** (`docs/2026-10-22-the-interval-treiber-regel.md`): `practice/src/practice/interval/drivers.py` (stdlib xlsx reader, rule unchanged from the audit), new driver value `weather` (`register.py`, `verify.py`), `verify.py` `check_interval_drivers` re-derives every entry naming the rule from the committed bytes, tests `practice/tests/test_interval_drivers.py` (18). On the preserved file the rule gives 7 of 8 (AFG 2021-10 conflict, AFG 2025-10 economic, DJI 2023-04 economic, SDN 2023-06 conflict, SOM 2022-03 weather, SOM 2024-08 weather, SOM 2026-01 unassigned, YEM 2025-06 economic) — held as a test regression, **not entered**; `interval/register.json` unchanged. **Next step here:** none until the maintainer answers `REQUESTS.md` (2026-10-22) or the window closes; then the entries, as one dated step, with the register recomputed.
- **Updated:** 2026-10-27 (pass)

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
- **Next step:** none on the instrument once the window opens; 2026-10-20 was the last day for a dated
  addendum — **none taken** (2026-10-20: nothing in `planetary/readings/2026-10-19.json` or the tally
  `python -m practice.planetary.experiment` calls for one; nights due 0 of 14, B4 undetermined, 2 days before the shift). **2026-10-21 (06:4x UTC):** first window night 2026-10-21 not yet due — the workflow slot is 08:10 UTC; tally lists it as missing at pass time (A1 still pass, nights due 1 of 14, 0 × 429, B4 undetermined); the next pass checks it landed. **2026-10-22: it did not.** `planetary/readings/2026-10-21.json` is missing — run `planetary` #6 (2026-10-21 13:42–13:52 UTC) died on `SourceUnavailable` (GEOFON dataselect, TimeoutError after 4 attempts) and wrote nothing; the outage branch of the day routine is never taken on a network error. Tally at pass time: A1 missing 2026-10-21 and 2026-10-22 (the latter not yet run), A2 pass, A3 0, B4 undetermined, B6 0. **Repair 2026-10-22** (`docs/2026-10-22-planetary-listening-reparatur-ausfall.md`): `nightly.py` records a host without an answer as status 0 with its cause (`station_day.cause`, `requests[].error`), so the night is written and A2 counts it; test `test_a_host_that_times_out_is_a_failed_night_not_a_lost_one`; detector, spike, client timeouts, workflow and criteria untouched. 2026-10-21 stays the one missing night A1 allows; a second in a row breaks A1 — `workflow_dispatch` asked for in `REQUESTS.md` (2026-10-22) if 2026-10-22 has not landed by 23:00 UTC. The next pass checks 2026-10-22 and 2026-10-23 landed. **Second pass 2026-10-22 (12:16 UTC):** today's run not yet started (runs 4–6 started 13:31–13:53 UTC); nothing to do before 23:00 UTC. **Third pass 2026-10-22 (14:15 UTC):** `planetary/readings/2026-10-22.json` landed (commit `7c96e7b`, 13:44 UTC) — the dispatch request in `REQUESTS.md` is closed as moot. Tally: nights due 2 of 14, A1 missing only 2026-10-21 (pass), A2 pass, A3 0, B1 attest present 2026-10-22 (availability for the read day answered 200 this time, `Updated 2026-10-22T05:07:23Z`), B4 undetermined (3 days before), Wednesday's strong impulse 07:30:45 UTC, B6 0. From 2026-10-26 the pass notes B4 (first after-shift weekday). **2026-10-23 (06:4x UTC):** today's night not yet due (slot 08:10 UTC, runs so far started 10:20–13:53 UTC); newest reading `planetary/readings/2026-10-22.json`; nothing to do. **Second pass 2026-10-23 (22:3x UTC):** `planetary/readings/2026-10-23.json` landed (commit `1aec490`, 13:21 UTC); nothing to do. The next pass checks 2026-10-24 landed. **2026-10-24 (06:37 UTC):** tonight's night not yet due (slot 08:10 UTC); newest reading `planetary/readings/2026-10-23.json`; nothing to do. The next pass checks 2026-10-24 landed and, from Monday 2026-10-26, notes B4. **Second pass 2026-10-24 (18:5x UTC):** `planetary/readings/2026-10-24.json` landed (commit `564004e`, 12:38 UTC). Tally: nights due 4 of 14, A1 missing only 2026-10-21 (pass), A2 pass, A3 0, A4 none over, B1 attest present 2026-10-22 and 2026-10-24, missing 2026-10-23, B2 none, B4 undetermined (4 days before, 0 after), Thursday 2026-10-22 no strong impulse, Friday 2026-10-23 07:38:44 UTC, B6 0. Nothing to do; Germany leaves summer time tonight-to-tomorrow, Monday 2026-10-26 is the first after-shift weekday. **2026-10-25 (06:3x UTC):** Germany left summer time at 01:00 UTC today; tonight's night 2026-10-25 not yet due (slot 08:10 UTC), so the tally lists it as missing and reports A1 `false` at pass time (nights due 5 of 14, missing 2026-10-21 and 2026-10-25 — not consecutive; the A1 count recovers when today's reading lands). A2 pass, A3 0, A4 none over, B1 attest present 2026-10-22 and 2026-10-24, missing 2026-10-23, B4 undetermined (4 before, 0 after), B6 0. The next pass checks 2026-10-25 landed; if it has not by 23:00 UTC, a second missing night anywhere in the window puts A1 at 12 of 14, below its bar of 13 — a `workflow_dispatch` is asked for then, not now. **2026-10-26 (06:4x UTC):** `planetary/readings/2026-10-25.json` landed (commit `aabf542`), so 2026-10-21 stays the only lost night; tonight's night 2026-10-26 is not yet due (slot 08:10 UTC) and the tally counts it missing at pass time only (A1 `false` for that reason, nights due 6 of 14). A2 pass, A3 0, A4 none over, B1 attest present 2026-10-22, 2026-10-24, 2026-10-25, missing 2026-10-23, B2 none, B6 0. **B4 still undetermined** (4 days before, 0 after): the 2026-10-25 reading covers Saturday 2026-10-24; the first after-shift weekday, Monday 2026-10-26, is read by the night 2026-10-27. The next pass checks 2026-10-26 landed and notes B4. **2026-10-27 (06:3x UTC):** `planetary/readings/2026-10-26.json` landed (commit `984afc9`, which reads day 2026-10-25), so 2026-10-21 stays the only lost night; tonight's night 2026-10-27 not yet due (slot 08:10 UTC), counted missing at pass time only (A1 `false` for that reason, nights due 7 of 14). A2 pass, A3 0, A4 none over, B1 attest present 2026-10-22, 10-24, 10-25, 10-26, missing 10-23, B2 none, B6 0, Sunday 2026-10-25 no strong impulse. **B4 still undetermined** (4 before, 0 after): Monday 2026-10-26, the first after-shift weekday, is read by tonight's night 2026-10-27 — the next pass notes it. At 2026-11-04: a two-sentence
  review request in `REQUESTS.md`.
- **Repair 2026-10-19 (second pass), before the window:** the workflow slot moved 06:40 → 08:10 UTC
  (`.github/workflows/planetary.yml`) — `planetary/readings/2026-10-19.json` carries publisher
  `Updated 06:22:02Z`, inside the 30-minute margin, and `test_planetary_workflow.py` was red on main.
  Criteria count dates, not hours (criteria §4.2); detector and `nightly.py` untouched (B6).
- **Re-read when:** Geseke — if the operator page shows a forward date again, re-measure
  hearing there (pairing B would restore the second register, audit flagship condition d).
- **Substrate note:** after `pip install -e ./practice` module runs need no `PYTHONPATH`
  (checked 2026-10-16); without installation, `practice/` shadows the package.
- **Updated:** 2026-10-27 (pass)

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
- **Increment 2 done 2026-10-20** (`docs/2026-10-20-synthetic-flood-v0-inkrement-2.md`): Register B
  reader `practice/src/practice/syntheticflood/wikipedia.py` + `categories.py` (one request, answer
  preserved under `syntheticflood/snapshots/<date>-categories/`), `verify.py`
  `check_syntheticflood_categories` (independent re-derivation from the bytes, names and sizes only),
  tests `practice/tests/test_syntheticflood_categories.py`. First reading
  `syntheticflood/categories/2026-10-20.json` is an **outage**: 4 × 429 from the reader, while a
  command-line request with the same user agent a minute earlier got 200; a single diagnostic probe
  (`syntheticflood/probes/2026-10-20/`) got 429 again. Six requests in total, then stopped.
- **Step 2b done 2026-10-20 (second pass)** (`docs/2026-10-20-synthetic-flood-v0-schritt-2b.md`):
  reader once at 09:40:58 UTC → 429; command-line client once at 09:46:26 → 429
  (`x-envoy-ratelimited: true`, `retry-after: 33`); both preserved in
  `syntheticflood/probes/2026-10-20/`. No client difference proven; the reader stays unchanged. Most
  likely the edge limit sits on this container's shared egress address (not proven). Two requests,
  no repeat.
- **Increment 3 done 2026-10-21** (`docs/2026-10-21-synthetic-flood-v0-inkrement-3.md`): year
  cohorts (`hasabstract AND YYYY[dp]`), readings `syntheticflood/readings/2018…2022/2026-10-21.json`
  (839 requests, 4 × 429 each retried to 200, 0 missing); rule `baseline-v1` written before the first
  request (`practice/src/practice/syntheticflood/baseline.py`: rare < 50 in a year, stable if max/min
  share ≤ 1.5); result `syntheticflood/baseline/wordlist-v1.json`, re-derived by `verify.py`
  `check_syntheticflood_baseline`; tests `practice/tests/test_syntheticflood_baseline.py`. Fixed 31
  stable / 10 rising / 6 rare; controls 19 stable / 1 rare; pool 81 / 16 / 2. **Findings:** the
  control `significantly` is a PubMed stopword (0 in every reading, the 2026-09 one too); `delve` and
  nine other fixed words already rose 2018→2022, so the derived list must measure excess against the
  baseline trend, not its level.
- **Increment 3b done 2026-10-22** (`docs/2026-10-22-synthetic-flood-v0-inkrement-3b.md`):
  `syntheticflood/wordlists/wordlist-v2.json` (control `significantly` → `reduced`, fixed and pool
  unchanged; `wordlist-v1` untouched) and rule `excess-v1`
  (`practice/src/practice/syntheticflood/excess.py`, tests `practice/tests/test_syntheticflood_excess.py`):
  least-squares line of 2018–2022 shares, ratio observed/expected, pool word in the month's list at
  ratio ≥ 2.0 and ≥ 50 abstracts, at most 20; a control outside [1/1.5, 1.5] marks the month
  `control_breach`. Committed before any derived list is computed; the 2026-09 reading's pool counts
  were not looked at. No fetch.
- **Increment 3c done 2026-10-22 (second pass)** (`docs/2026-10-22-synthetic-flood-v0-inkrement-3c.md`):
  five baseline years and cohort 2026-09 (M+1) read on `wordlist-v2`
  (`syntheticflood/readings/{2018…2022,2026-09}/2026-10-22.json`, 1 010 requests, 8 × 429 each retried
  to 200, 0 missing); `syntheticflood/baseline/wordlist-v2.json` (controls 20 stable, `reduced` 1.034);
  derived-list writer `practice/src/practice/syntheticflood/derived.py`, re-derived independently by
  `verify.py` `check_syntheticflood_derived`, tests `practice/tests/test_syntheticflood_derived.py`.
  **First derived list `syntheticflood/derived/2026-09/2026-10-22.json` is `control_breach`:**
  `reduced` 13.8 % observed vs 7.5 % on its baseline line (ratio 1.827); the other 19 controls
  0.678–1.399. The list is reported, not used; cause not proven (M+1 mix, a search change, or usage).
  Rule and word list untouched.
- **Increment 3d done 2026-10-24** (`docs/2026-10-24-synthetic-flood-v0-inkrement-3d.md`): rule
  `revision-v1` (`practice/src/practice/syntheticflood/revision.py`: share drift of each word between
  two readings of one cohort, `thin` below 50, `moved` outside [1/1.1, 1.1]), `verify.py`
  `check_syntheticflood_revisions`, tests `practice/tests/test_syntheticflood_revision.py` (6). First
  revision `syntheticflood/revisions/2026-09/2026-10-19_2026-10-22.json`: total +0.27 %, 137 words all
  `held` (0.984–1.034), 28 thin — `reduced` is not on `wordlist-v1`, so it says nothing about the
  breach. **Committed before the M+2 reading:** the breach can fall only if `reduced` drifts to
  ≤ 0.8209; the doc's table fixes what each outcome means and what follows. No fetch.
- **Next step:** read 2026-09 again at M+2 (from 2026-11-01, ≈ 170 requests) and derive again and write the revision
  `2026-10-22_<date>` — read by the table of increment 3d. No `wordlist-v3` or `excess-v2` before that second reading. Workflow (increment 4) only
  after a month derives without a breach. Register B stays closed until the reader reads one 200; the
  runner question in `REQUESTS.md` (2026-10-20) stays open. Only on nights the focus waits.
- **Updated:** 2026-10-24 (pass)

### The Declared Network — how long a silent weather station stays declared

- **Stage:** AUDIT done 2026-10-23 (second pass, `docs/2026-10-23-declared-network-audit.md`, 9 probes
  with manifest in `declarednetwork/probes/2026-10-23/`) — **parked on its result**. Exposé the same
  morning (`docs/2026-10-23-kandidat-declared-network.md`). Findings: **OSCAR/Surface `robots.txt` is
  `Disallow: /` for every agent** (`declarednetwork/probes/2026-10-23/oscar/robots.txt`) — the
  FEWS NET situation; the one station search sent before it was weighed is held by hash only, no
  bytes. That answer (16 706 land stations, keyless, one page, no contact fields) carries
  `assessedStatus` beside `declaredStatus` (459 declared operational / assessed silent): the register
  already juxtaposes today, so the daylight narrows to the **lag over time**, which it does not
  publish. **WDQMS** download is open (no robots, keyless CSV, joins on WIGOS-ID: 11 542 of 13 486)
  and its archive reaches back to 2020-07-06 (preserved heads for 2020-07-06, 2023-01-01,
  2026-10-21); ≈ 7 MB a day per variable, so V0 would commit derived rows only; licence not stated
  at the endpoint. **GHCN-Daily** inventory is year-resolved and not rewritten daily (Last-Modified
  2026-10-14): out as a control.
- **Blocker:** OSCAR `robots.txt` `Disallow: /` — whether to ask the operator or read it as not
  covering the REST interface is the maintainer's (`REQUESTS.md` 2026-10-23). The pass does not
  query OSCAR again until the maintainer says so.
- **Gate:** V0 needs the maintainer's GO (none asked for: the blocker comes first).
- **Next step:** none until `REQUESTS.md` (2026-10-23) is answered. If the register is opened: WDQMS
  rate and licence probe, then the GO request.
- **Updated:** 2026-10-23 (second pass)

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
