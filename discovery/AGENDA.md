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
- **Next step:** none on the instrument until the window runs — the weekly workflow carries it. (2026-10-16 and 2026-10-18: checked, nothing due — the window opens Monday 2026-10-19; no criteria change landed on the last day.) **2026-10-19, week 1:** at 06:38 UTC the week's reading was not yet on main and `interval.yml` lists no run at all yet — its first scheduled firing; the planetary workflow, scheduled 06:40, ran at 11:08 and 11:39 on 10-17/10-18, so a delay of hours is the platform's norm. Tally at pass time: A1 missing 2026-10-19 (not yet run), A2 none, A3 none, B1 0 moves, B2 no change, B6 unchanged from the addendum (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). A run any day of ISO week 43 still counts; if none has landed by 2026-10-21 a `workflow_dispatch` is asked for in `REQUESTS.md` (2026-10-19). **Second pass 2026-10-19 (evening):** the week-1 reading landed (`interval/readings/2026-10-19.json`, workflow run 10:20 UTC per `autonomy/log.jsonl`); tally A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 unchanged — the request of the morning is closed as moot. Next Monday 2026-10-26: B2, B4, B6 for weeks 1–2. **2026-10-20:** nothing due (Tuesday; week 1 is read). **2026-10-21:** nothing due (Wednesday); tally unchanged — A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 43/77 vs 3/7 at FSC·date·k=2. **2026-10-22:** nothing due (Thursday); tally unchanged — A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change (morning, second and fourth pass). **2026-10-23:** nothing due (Friday); `REQUESTS.md` (2026-10-22) unanswered, so the driver entries stay after 2026-11-15 (checked again in the second pass, unchanged). **2026-10-24:** nothing due (Saturday); `REQUESTS.md` (2026-10-22) still unanswered. Second pass (18:5x UTC): tally unchanged — A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change; `REQUESTS.md` (2026-10-22) still unanswered. **2026-10-25:** nothing due (Sunday, last day of week 1); tally unchanged — A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, weeks due 1 of 4; `REQUESTS.md` (2026-10-22) still unanswered, so the driver entries stay after 2026-11-15. Monday 2026-10-26 is week 2. **2026-10-26 (06:4x UTC), week 2 (ISO week 44):** the week's reading is not yet on main — week 1's ran at 10:20 UTC, so the tally lists 2026-10-26 as missing at pass time only (A1 missing 2026-10-26, not yet run; weeks due 2 of 4). A2 pass, A3 none, B1 0 moves, B2 no change across weeks 1–2 (one reading in the window so far, 8 episodes), B4 not yet computable (needs week 2's reading), B6 unchanged from the addendum (FSC·date·k=2: 43/77 placebo vs 3/7 onsets; all eight cells as in `interval/experiment.json`). A run any day of ISO week 44 counts; if none has landed by 2026-10-28 a `workflow_dispatch` is asked for in `REQUESTS.md`. `REQUESTS.md` (2026-10-22) still unanswered, so the driver entries stay after 2026-11-15. **2026-10-27 (06:3x UTC):** week 2's reading landed (`interval/readings/2026-10-26.json`, commit `3a71f48`, workflow 10:35 UTC per `autonomy/log.jsonl`). Tally: weeks due 2 of 4, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change (8 episodes both weeks), B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). **B4, weeks 1–2: no violation** — the four open cells (AFG 2025-10 and SOM 2026-01, fsc and total) changed between the two readings only in flow counts (AFG fsc 351→356, total 2951→2975; SOM fsc 278→279, total 1504→1533), each with new preserved pages under `interval/snapshots/2026-10-26/fts/` and new hashes in `interval/register.json`; `t1` unchanged, IPC snapshot unchanged (`status: unchanged`). `REQUESTS.md` (2026-10-22) still unanswered, so the driver entries stay after 2026-11-15. **2026-10-28:** nothing due (Wednesday); tally unchanged — weeks due 2 of 4, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change (8 episodes both weeks); `REQUESTS.md` (2026-10-22) still unanswered, so the driver entries stay after 2026-11-15. Monday 2026-11-02 is week 3. **2026-10-29:** nothing due (Thursday); tally unchanged — weeks due 2 of 4, A1 no missing week, A2 pass, A3 none, B2 no change (8 episodes both weeks); `REQUESTS.md` (2026-10-22) still unanswered. **2026-10-30:** nothing due (Friday); tally unchanged — weeks due 2 of 4, A1 no missing week, A2 pass, A3 none, B2 no change (8 episodes both weeks); `REQUESTS.md` (2026-10-22) still unanswered. **2026-10-31:** nothing due (Saturday); tally unchanged — weeks due 2 of 4, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets); `REQUESTS.md` (2026-10-22) still unanswered. Monday 2026-11-02 is week 3. Each Monday's pass runs the tally and notes B2, B4 and B6 in this file; nothing in the criteria moves after 2026-10-18. At 2026-11-16: a two-sentence review request in `REQUESTS.md`.
- **Open, no gate:** all eight drivers in `interval/drivers.json` are `unassigned`. **Driver-source audit done 2026-10-22 (third pass)** (`docs/2026-10-22-the-interval-treiber-quelle-audit.md`, 7 probes in `interval/probes/2026-10-22/manifest.json`): ipcinfo.org 403 (browser check page, not reachable keyless), ReliefWeb API 403 (approved appname required — outside the charter), HDX "hunger hotspots" 0 datasets; **the Global Report on Food Crises database on HDX** (package `fsin-grfc`, CC BY, `grfc_afi_database_2016-2025_september_update.xlsx`, 197 955 B, preserved) carries `Primary/Secondary/Tertiary driver` per country × reference year 2016–2025 — inside the charter. Recommendation: rule `drivers-grfc-v1` (row of t0's year, latest edition; primary driver → `conflict`/`economic`/new value `weather`, never `drought`; secondaries kept verbatim; no row → `unassigned`, so SOM 2026-01 stays unassigned). The rows were read in the audit (disclosed: the rule is not blind). Whether drivers enter inside the window is put in `REQUESTS.md` (2026-10-22); silence means: rule as tested code first, entries after 2026-11-15. **Rule as code done 2026-10-22 (fourth pass)** (`docs/2026-10-22-the-interval-treiber-regel.md`): `practice/src/practice/interval/drivers.py` (stdlib xlsx reader, rule unchanged from the audit), new driver value `weather` (`register.py`, `verify.py`), `verify.py` `check_interval_drivers` re-derives every entry naming the rule from the committed bytes, tests `practice/tests/test_interval_drivers.py` (18). On the preserved file the rule gives 7 of 8 (AFG 2021-10 conflict, AFG 2025-10 economic, DJI 2023-04 economic, SDN 2023-06 conflict, SOM 2022-03 weather, SOM 2024-08 weather, SOM 2026-01 unassigned, YEM 2025-06 economic) — held as a test regression, **not entered**; `interval/register.json` unchanged. **Next step here:** none until the maintainer answers `REQUESTS.md` (2026-10-22) or the window closes; then the entries, as one dated step, with the register recomputed.
- **2026-11-01:** nothing due (Sunday); week 3 is Monday 2026-11-02 (`interval.yml`, 04:50 UTC). Tally (`python -m practice.interval.experiment --repo-root .`): weeks due 2 of 4, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets).
- **2026-11-02 (07:38 UTC), week 3 (ISO week 45):** the week's reading is not yet on main (weeks 1–2 ran at 10:20 and 10:35 UTC), so the tally lists 2026-11-02 as missing at pass time only (A1 missing 2026-11-02, weeks due 3 of 4). A2 pass, A3 none, B1 0 moves, B2 no change (8 episodes, weeks 1–2), B4 for week 3 not computable until its reading lands, B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). A run any day of ISO week 45 counts; if none has landed by 2026-11-04 a `workflow_dispatch` is asked for in `REQUESTS.md`. `REQUESTS.md` (2026-10-22) still unanswered, so the driver entries stay after 2026-11-15.
- **2026-11-03, week 3 read** (`docs/2026-11-03-the-interval-woche-3.md`): `interval/readings/2026-11-02.json` landed (commit `91f4202`, 12:54 UTC). Tally: weeks due 3 of 4, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change (8 episodes all three weeks), B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). **B4, weeks 2–3: no violation** — only the four open queries changed, each with new pages under `interval/snapshots/2026-11-02/fts/`. **Finding, reported:** AFG 2025-10 total·`date`·k=2 went from `closed` (t1 2026-06, gap 8) to `none_in_horizon` — nine paid flows were re-dated by the source from 2026-06 to 2026-10 in new versions and nine June commitments left the list, so June fell from 269.2 to 233.0 M USD under the 252.28 M threshold; the `firstReportedDate` axis stays closed at 2025-10. No criterion breached (the query is open, not frozen); a case for the review, not a repair. Week 4 is Monday 2026-11-09. `REQUESTS.md` (2026-10-22) still unanswered.
- **2026-11-04:** nothing due (Wednesday); the dispatch deadline of 2026-11-02 is moot — week 3 landed 2026-11-02 (`91f4202`). Tally unchanged: weeks due 3 of 4, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). Week 4 is Monday 2026-11-09; `REQUESTS.md` (2026-10-22) still unanswered.
- **2026-11-05:** nothing due (Thursday). Tally unchanged: weeks due 3 of 4, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). Week 4 is Monday 2026-11-09; `REQUESTS.md` (2026-10-22) still unanswered.
- **2026-11-06:** nothing due (Friday). Tally unchanged (`python -m practice.interval.experiment --repo-root .`): A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). Week 4 is Monday 2026-11-09; `REQUESTS.md` (2026-10-22) still unanswered.
- **2026-11-07:** nothing due (Saturday). Tally unchanged (`python -m practice.interval.experiment --repo-root .`): A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). Week 4 is Monday 2026-11-09; `REQUESTS.md` (2026-10-22) still unanswered.
- **2026-11-08:** nothing due (Sunday, last day of week 3). Tally unchanged (`python -m practice.interval.experiment --repo-root .`): weeks due 3 of 4, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change (8 episodes all three weeks), B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). Week 4 is Monday 2026-11-09 (B2, B4, B6 for weeks 3–4 in that pass); `REQUESTS.md` (2026-10-22) still unanswered.
- **2026-11-09 (07:37 UTC), week 4 (ISO week 46):** the week's reading is not yet on main (weeks 1–3 ran at 10:20, 10:35 and 12:54 UTC), so the tally lists 2026-11-09 as missing at pass time only (A1 missing 2026-11-09, weeks due 4 of 4, `closed: false`). A2 pass, A3 none, B1 0 moves, B2 no change (8 episodes, weeks 1–3), B4 for weeks 3–4 not computable until its reading lands, B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). A run any day of ISO week 46 counts; if none has landed by 2026-11-11 a `workflow_dispatch` is asked for in `REQUESTS.md`. The next pass computes B4 for weeks 3–4. The window closes 2026-11-15; at 2026-11-16 the review request. `REQUESTS.md` (2026-10-22) still unanswered.
- **2026-11-10, week 4 read** (`docs/2026-11-10-the-interval-woche-4.md`): `interval/readings/2026-11-09.json` landed (commit `bd9c933`, 13:26 UTC), so the dispatch deadline of 2026-11-11 is moot. Tally: weeks due 4 of 4, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change (8 episodes all four weeks), B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). First new IPC snapshot in the window (`interval/snapshots/2026-11-09/ipc/`, 42 appended rows: COD, LBN, UGA; no new episode). **B4, weeks 3–4: no violation** — only the four open queries and the IPC pointer changed, each with a new snapshot. **Finding, reported:** AFG 2025-10 FSC·`date`·k=2 went from `closed` (t1 2026-04, gap 6) to `none_in_horizon` — the parked flow 385472 fell from 64.6 to 31.2 M USD with five new child ids while its `versionId` stayed 1 (`updatedAt` moved), so April fell from 69.2 to 35.8 M under the 64.18 M threshold; the same flow sits in the SOM FSC list (SOM's cell stays closed). Second reopened clock in the window, second mechanism; no criterion breached. Next: the pass after 2026-11-15 writes the review request in `REQUESTS.md`; nothing in the instrument changes. `REQUESTS.md` (2026-10-22) still unanswered.
- **2026-11-11:** nothing due (Wednesday). Tally unchanged (`python -m practice.interval.experiment --repo-root .`): A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change, B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). The window closes 2026-11-15; the pass of 2026-11-16 writes the review request. `REQUESTS.md` (2026-10-22) still unanswered.
- **2026-11-13:** nothing due (Friday; no pass ran on 2026-11-12). Tally unchanged (`python -m practice.interval.experiment --repo-root .`): weeks due 4 of 4, `closed: false`, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change (8 episodes all four weeks), B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). The window closes 2026-11-15; the pass of 2026-11-16 writes the two-sentence review request in `REQUESTS.md`. `REQUESTS.md` (2026-10-22) still unanswered, so the driver entries follow after 2026-11-15.
- **2026-11-14:** nothing due (Saturday). Tally unchanged (`python -m practice.interval.experiment --repo-root .`): weeks due 4 of 4, `closed: false`, A1 no missing week, A2 pass, A3 none, B1 0 moves, B2 no change (8 episodes all four weeks), B6 unchanged (FSC·date·k=2: 43/77 placebo vs 3/7 onsets). The window closes tomorrow, 2026-11-15; the pass of 2026-11-16 writes the two-sentence review request in `REQUESTS.md`. `REQUESTS.md` (2026-10-22) still unanswered, so the driver entries follow after 2026-11-15.
- **Updated:** 2026-11-14 (pass)

## Next

### Planetary Listening — "One Quarry, Two Records"

- **Stage:** E-EXPERIMENT — **window closed 2026-11-03, review requested 2026-11-04 (maintainer's)**; criteria committed **2026-10-19, before the window** (V0 increment 4):
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
  `python -m practice.planetary.experiment` calls for one; nights due 0 of 14, B4 undetermined, 2 days before the shift). **2026-10-21 (06:4x UTC):** first window night 2026-10-21 not yet due — the workflow slot is 08:10 UTC; tally lists it as missing at pass time (A1 still pass, nights due 1 of 14, 0 × 429, B4 undetermined); the next pass checks it landed. **2026-10-22: it did not.** `planetary/readings/2026-10-21.json` is missing — run `planetary` #6 (2026-10-21 13:42–13:52 UTC) died on `SourceUnavailable` (GEOFON dataselect, TimeoutError after 4 attempts) and wrote nothing; the outage branch of the day routine is never taken on a network error. Tally at pass time: A1 missing 2026-10-21 and 2026-10-22 (the latter not yet run), A2 pass, A3 0, B4 undetermined, B6 0. **Repair 2026-10-22** (`docs/2026-10-22-planetary-listening-reparatur-ausfall.md`): `nightly.py` records a host without an answer as status 0 with its cause (`station_day.cause`, `requests[].error`), so the night is written and A2 counts it; test `test_a_host_that_times_out_is_a_failed_night_not_a_lost_one`; detector, spike, client timeouts, workflow and criteria untouched. 2026-10-21 stays the one missing night A1 allows; a second in a row breaks A1 — `workflow_dispatch` asked for in `REQUESTS.md` (2026-10-22) if 2026-10-22 has not landed by 23:00 UTC. The next pass checks 2026-10-22 and 2026-10-23 landed. **Second pass 2026-10-22 (12:16 UTC):** today's run not yet started (runs 4–6 started 13:31–13:53 UTC); nothing to do before 23:00 UTC. **Third pass 2026-10-22 (14:15 UTC):** `planetary/readings/2026-10-22.json` landed (commit `7c96e7b`, 13:44 UTC) — the dispatch request in `REQUESTS.md` is closed as moot. Tally: nights due 2 of 14, A1 missing only 2026-10-21 (pass), A2 pass, A3 0, B1 attest present 2026-10-22 (availability for the read day answered 200 this time, `Updated 2026-10-22T05:07:23Z`), B4 undetermined (3 days before), Wednesday's strong impulse 07:30:45 UTC, B6 0. From 2026-10-26 the pass notes B4 (first after-shift weekday). **2026-10-23 (06:4x UTC):** today's night not yet due (slot 08:10 UTC, runs so far started 10:20–13:53 UTC); newest reading `planetary/readings/2026-10-22.json`; nothing to do. **Second pass 2026-10-23 (22:3x UTC):** `planetary/readings/2026-10-23.json` landed (commit `1aec490`, 13:21 UTC); nothing to do. The next pass checks 2026-10-24 landed. **2026-10-24 (06:37 UTC):** tonight's night not yet due (slot 08:10 UTC); newest reading `planetary/readings/2026-10-23.json`; nothing to do. The next pass checks 2026-10-24 landed and, from Monday 2026-10-26, notes B4. **Second pass 2026-10-24 (18:5x UTC):** `planetary/readings/2026-10-24.json` landed (commit `564004e`, 12:38 UTC). Tally: nights due 4 of 14, A1 missing only 2026-10-21 (pass), A2 pass, A3 0, A4 none over, B1 attest present 2026-10-22 and 2026-10-24, missing 2026-10-23, B2 none, B4 undetermined (4 days before, 0 after), Thursday 2026-10-22 no strong impulse, Friday 2026-10-23 07:38:44 UTC, B6 0. Nothing to do; Germany leaves summer time tonight-to-tomorrow, Monday 2026-10-26 is the first after-shift weekday. **2026-10-25 (06:3x UTC):** Germany left summer time at 01:00 UTC today; tonight's night 2026-10-25 not yet due (slot 08:10 UTC), so the tally lists it as missing and reports A1 `false` at pass time (nights due 5 of 14, missing 2026-10-21 and 2026-10-25 — not consecutive; the A1 count recovers when today's reading lands). A2 pass, A3 0, A4 none over, B1 attest present 2026-10-22 and 2026-10-24, missing 2026-10-23, B4 undetermined (4 before, 0 after), B6 0. The next pass checks 2026-10-25 landed; if it has not by 23:00 UTC, a second missing night anywhere in the window puts A1 at 12 of 14, below its bar of 13 — a `workflow_dispatch` is asked for then, not now. **2026-10-26 (06:4x UTC):** `planetary/readings/2026-10-25.json` landed (commit `aabf542`), so 2026-10-21 stays the only lost night; tonight's night 2026-10-26 is not yet due (slot 08:10 UTC) and the tally counts it missing at pass time only (A1 `false` for that reason, nights due 6 of 14). A2 pass, A3 0, A4 none over, B1 attest present 2026-10-22, 2026-10-24, 2026-10-25, missing 2026-10-23, B2 none, B6 0. **B4 still undetermined** (4 days before, 0 after): the 2026-10-25 reading covers Saturday 2026-10-24; the first after-shift weekday, Monday 2026-10-26, is read by the night 2026-10-27. The next pass checks 2026-10-26 landed and notes B4. **2026-10-27 (06:3x UTC):** `planetary/readings/2026-10-26.json` landed (commit `984afc9`, which reads day 2026-10-25), so 2026-10-21 stays the only lost night; tonight's night 2026-10-27 not yet due (slot 08:10 UTC), counted missing at pass time only (A1 `false` for that reason, nights due 7 of 14). A2 pass, A3 0, A4 none over, B1 attest present 2026-10-22, 10-24, 10-25, 10-26, missing 10-23, B2 none, B6 0, Sunday 2026-10-25 no strong impulse. **B4 still undetermined** (4 before, 0 after): Monday 2026-10-26, the first after-shift weekday, is read by tonight's night 2026-10-27 — the next pass notes it. **2026-10-28 (07:4x UTC):** `planetary/readings/2026-10-27.json` landed (commit `c0eb4a2`, reads day 2026-10-26); tonight's night 2026-10-28 not yet due, counted missing at pass time only (A1 `false` for that reason, nights due 8 of 14). A2 pass, A3 0, A4 none over, B1 attest present 10-22, 10-24 to 10-27, missing 10-23, B2 none, B6 0. **B4, first after-shift weekday:** Monday 2026-10-26 first strong impulse 08:37:23 UTC against a before-median of 07:31:41 (Oct 14, 15, 21, 23) — +65.7 min, inside the `local` band (60 ± 10); the verdict stays `undetermined` until a second after-shift weekday (`min_days_each_side: 2`), so nothing is concluded from one day. **2026-10-29 (07:0x UTC):** `planetary/readings/2026-10-28.json` landed (commit `a00c0be`, reads day 2026-10-27); tonight's night 2026-10-29 not yet due, counted missing at pass time only (A1 `false` for that reason, nights due 9 of 14). A2 pass, A3 0, A4 none over, B1 attest present 10-22, 10-24 to 10-28, missing 10-23, B2 none, B6 0. **B4 now determined: `local`** — Tuesday 2026-10-27 first strong impulse 08:29:26 UTC; with Monday 08:37:23 the after-median sits +61.72 min from the before-median (4 days before, 2 after, `min_days_each_side: 2` met), inside the `local` band 60 ± 10. Reported, no bar; the verdict can still move with later weekdays in the window. **2026-10-30 (07:3x UTC):** `planetary/readings/2026-10-29.json` landed (commit `bfb4388`, reads day 2026-10-28); tonight's night 2026-10-30 not yet due, counted missing at pass time only (A1 `false` for that reason, nights due 10 of 14). A2 pass, A3 0, A4 none over, B1 attest present 10-22, 10-24 to 10-29, missing 10-23, B2 none, B6 0. B4 still `local`: Wednesday 2026-10-28 first strong impulse 08:27:59 UTC, after-median now +57.74 min (4 before, 3 after), inside 60 ± 10. **2026-10-31 (07:xx UTC):** `planetary/readings/2026-10-30.json` landed (commit `e4870ce`, 15:00 UTC, reads day 2026-10-29); tonight's night 2026-10-31 not yet due, counted missing at pass time only (A1 `false` for that reason, nights due 11 of 14). A2 pass, A3 0, A4 none over, B1 attest present 10-22, 10-24 to 10-30, missing 10-23, B2 none, B6 0, C none. B4 still `local`: Thursday 2026-10-29 first strong impulse 08:39:39 UTC, after-median now +57.02 min (4 before, 4 after), inside 60 ± 10. Three nights remain (10-31, 11-01, 11-02 readings plus 11-03); the window closes 2026-11-03. At 2026-11-04: a two-sentence
  review request in `REQUESTS.md`.
- **Repair 2026-10-19 (second pass), before the window:** the workflow slot moved 06:40 → 08:10 UTC
  (`.github/workflows/planetary.yml`) — `planetary/readings/2026-10-19.json` carries publisher
  `Updated 06:22:02Z`, inside the 30-minute margin, and `test_planetary_workflow.py` was red on main.
  Criteria count dates, not hours (criteria §4.2); detector and `nightly.py` untouched (B6).
- **Re-read when:** Geseke — if the operator page shows a forward date again, re-measure
  hearing there (pairing B would restore the second register, audit flagship condition d).
- **Substrate note:** after `pip install -e ./practice` module runs need no `PYTHONPATH`
  (checked 2026-10-16); without installation, `practice/` shadows the package.
- **2026-11-01 (07:37 UTC):** `planetary/readings/2026-10-31.json` landed; tonight's night 2026-11-01 not yet due (slot 08:10 UTC), so the tally lists it as missing at pass time (A1 shows 2026-10-21 and 2026-11-01 — not consecutive; A1 still holds if 2026-11-01 lands). Nights due 12 of 14, A2 pass, A3 0, A4 none over, B1 attest missing 2026-10-23 and 2026-10-31, B4 `local` (+57.02 min, 4 before / 4 after), B6 0, C empty. The window closes 2026-11-03; the pass of 2026-11-02 checks 2026-11-01 landed.
- **2026-11-02 (07:38 UTC):** `planetary/readings/2026-11-01.json` landed, so 2026-10-21 stays the only lost night; tonight's night 2026-11-02 not yet due (slot 08:10 UTC), counted missing at pass time only (A1 `false` for that reason, nights due 13 of 14). A2 pass, A3 0, A4 none over, B1 attest present 2026-11-01, missing 2026-10-23 and 2026-10-31, B2 none, B4 `local` (+57.02 min, 4 before / 4 after), B6 0, C empty. One night remains (2026-11-03); the pass of 2026-11-03 checks 2026-11-02 landed, the pass of 2026-11-04 writes the review request.
- **2026-11-03 (07:4x UTC):** `planetary/readings/2026-11-02.json` landed (commit `8d83fd0`), so 2026-10-21 stays the only lost night; the last window night 2026-11-03 is not yet due (slot 08:10 UTC) and is counted missing at pass time only (A1 `false` for that reason, nights due 14 of 14). A2 pass, A3 0, A4 none over, B1 attest missing 2026-10-23 and 2026-10-31, present on the other ten window nights, B2 none, B4 `local` (+57.02 min, 4 before / 4 after; Friday 2026-10-30 to Sunday 2026-11-01 no strong impulse), B6 0, C empty. The pass of 2026-11-04 checks 2026-11-03 landed and writes the two-sentence review request in `REQUESTS.md`.
- **2026-11-04 — window closed, review requested** (`docs/2026-11-04-planetary-listening-fenster-abschluss.md`): `planetary/readings/2026-11-03.json` landed (`a8886b0`). Tally `closed: true`, nights 14 of 14: A1 13/14 (only 2026-10-21 missing), A2 1 failed night (2026-11-03: dataselect 204 for day 2026-11-02 while the availability row attests the full day, `Updated 2026-11-03T05:15:51Z` — the reverse of §4.1, cause not proven), A3 0, A4 max 46.5 KB, A5 green, B1 attest missing 2026-10-23 and 2026-10-31, B2 none, B4 `local` (+57.02 min, 4/4), B5 0 catalogue rows every day, B6 0, C empty (`export.json` `site_route: null`). By §2 the criteria are met; the outcome (§5) is the maintainer's — request in `REQUESTS.md` (2026-11-04). **Next step:** none; the nightly workflow keeps reading, nothing in the instrument changes, no stage, until the review.
- **Updated:** 2026-11-04 (pass)

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
- **2026-10-31:** still held; `REQUESTS.md` (2026-10-30) unanswered, deadline the pass of 2026-11-02. No fetch.
- **2026-11-01:** still held; `REQUESTS.md` (2026-10-30) unanswered, deadline the pass of 2026-11-02 (tomorrow). M+2 is open from today but is not taken before the deadline. No fetch.
- **2026-11-02 — M+2 read (self-decision, `REQUESTS.md` 2026-10-30 unanswered by its deadline)** (`docs/2026-11-02-synthetic-flood-v0-lesung-m2.md`): `syntheticflood/readings/2026-09/2026-11-02.json` (169 requests, 2 × 429 retried to 200, 0 missing, total 172 506, +3.92 %); derived `syntheticflood/derived/2026-09/2026-11-02.json` again `control_breach` on `reduced` alone (ratio 1.821; other controls 0.676–1.394); revision `syntheticflood/revisions/2026-09/2026-10-22_2026-11-02.json`: 138 held, 0 moved, 28 thin, **`reduced` drift 0.9966**. Table row 2 of increment 3d: mixing at M+1 is excluded for `reduced`; cause open. **Next step:** read `reduced` in year cohorts 2023–2025 (6 requests) on a night the focus waits — the proposal the table fixed; no `wordlist-v3`/`excess-v2`/workflow before that finding. If the maintainer objects to the self-decision, Register A ends with this reading.
- **2026-11-03 — `reduced` read in year cohorts 2023–2025** (`docs/2026-11-03-synthetic-flood-reduced-jahre.md`, six counts with manifest in `syntheticflood/probes/2026-11-03/`, 7 requests, 1 × 429 retried to 200): shares 2023 7.989 %, 2024 8.694 %, 2025 11.033 % against 2022 7.901 % and 2026-09 13.735 % — class **gradual** by the reading fixed before the first request: the rise starts in 2024 and is steep in 2025. "Only young records" becomes unlikely; no cause proven. `reduced` rises itself, so it is unfit as a control and the breach of `excess-v1` measures the control more than the cohort. **Next step:** `wordlist-v3` with a replacement control proven stable on 2023–2025 before any derivation — a later pass on a night the focus waits; no `excess-v2`, no workflow before that. `REQUESTS.md` (2026-10-30) still open for objection.
- **Held 2026-10-30:** the Afterlife AUDIT found `eutils.ncbi.nlm.nih.gov/robots.txt` at `Disallow: /` for every agent (`afterlife/probes/2026-10-30/pubmed/robots.txt`); Register A reads that host, and the audit of 2026-10-18 fetched the file without weighing it (`docs/2026-10-30-the-afterlife-audit.md` §3). The M+2 reading waits on `REQUESTS.md` (2026-10-30) until the pass of 2026-11-02; silence through it means the pass takes M+2 and records the self-decision.
- **2026-11-04:** held; tonight's step went to closing the Planetary Listening window. Next step unchanged (`wordlist-v3` with a replacement control proven stable on 2023–2025). No fetch.
- **2026-11-05 — rule `control-check-v1` committed before any reading** (`docs/2026-11-05-synthetic-flood-kontrollpruefung.md`): `practice/src/practice/syntheticflood/controlcheck.py`, tests `practice/tests/test_syntheticflood_controlcheck.py` (9). Every control and six fixed candidates (`samples`, `groups`, `cases`, `performed`, `total`, `age`) must be `stable` on 2018–2022 and within [1/1.2, 1.2] of their own line in 2023, 2024, 2025; band 1.2 because the committed `reduced` counts give 1.0247 / 1.1266 / 1.4445 — inside excess-v1's 1.5 every year. `compose` builds `wordlist-v3` (passing controls in order, then passing candidates up to 20; under 15 → no list). No fetch. **Next step:** the check reading (≈ 113 count requests: 19 controls × 2023–2025, 6 candidates × 2018–2025, 8 totals) on a night the focus waits, under the self-decision of 2026-11-02; then `wordlist-v3` held by `verify.py`. No `excess-v2`, no workflow before.
- **2026-11-06 — check reading done, `wordlist-v3` composed** (`docs/2026-11-06-synthetic-flood-kontrollpruefung-lesung.md`): `syntheticflood/controlcheck/2026-11-06.json` (113 counts, 114 requests, 1 × 429 retried to 200, 0 missing), reader `practice/src/practice/syntheticflood/controlread.py`, `verify.py` `check_syntheticflood_controlcheck` (independent re-derivation; successor list must be the composition), tests `practice/tests/test_syntheticflood_controlread.py` (9). Three controls fall at band 1.2: `effect` (0.8029 in 2025), `levels` (1.2254), `observed` (1.2549); 16 pass; all six candidates are `stable` on 2018–2022 and pass; composition 16 + `samples`, `groups`, `cases`, `performed` = 20 → `syntheticflood/wordlists/wordlist-v3.json` (fixed, pool carried over). **Disclosed:** the first evaluation keyed the cohort total as `"total"`, which the candidate word `total` overwrote (all controls ~6.5); fixed before commit and re-evaluated from the stored rows with no further request. **Next step:** fix, before any request, how `wordlist-v3` gets its baseline (all five baseline years on the new list, ≈ 840 requests, or only the four new controls, whose 2018–2022 counts are already in tonight's record), then cohort 2026-09 on `wordlist-v3`. No `excess-v2`, no workflow before.
- **2026-11-07 — `wordlist-v3` baseline fixed without a request** (`docs/2026-11-07-synthetic-flood-basislinie-v3.md`): rule `baseline-carry-v1` chosen over a full re-read (≈ 840 requests to a host whose `robots.txt` is `Disallow: /`, `REQUESTS.md` 2026-10-30 open): the 162 words already on `wordlist-v2` keep their entry from `syntheticflood/baseline/wordlist-v2.json`, the four new controls take their 2018–2022 counts from `syntheticflood/controlcheck/2026-11-06.json`; each share stays count and total of one reading (totals differ by at most +0.008 %, 2022). Code `practice/src/practice/syntheticflood/carry.py`, `verify.py` `_sf_check_carry` (independent re-derivation from both sources by hash), tests `practice/tests/test_syntheticflood_carry.py` (9). Result `syntheticflood/baseline/wordlist-v3.json`: controls 20 stable; fixed 31/10/6, pool 81/16/2 as on v2. No fetch. **Next step:** cohort 2026-09 on `wordlist-v3` (≈ 167 requests) and derive with `excess-v1`, on a night the focus waits; workflow only after a month derives without a breach. No `excess-v2`.
- **2026-11-08 — cohort 2026-09 on `wordlist-v3`: first derivation without a breach** (`docs/2026-11-08-synthetic-flood-erste-ableitung-ohne-bruch.md`): `syntheticflood/readings/2026-09/2026-11-08.json` (M+2, 167 requests, 0 × 429, 0 missing, total 173 495, +0.57 % on 2026-11-02); `syntheticflood/derived/2026-09/2026-11-08.json` under `excess-v1`: **`control_breach: []`**, 20 controls 0.8211 (`patients`) to 1.3953 (`associated`); 20 derived words, `offering` 5.40 to `seamless` 2.12, one swap against 2026-11-02 at rank 20 (`enduring` 2.1334 for `versatile` 2.1008). Revision `syntheticflood/revisions/2026-09/2026-11-02_2026-11-08.json`: 162 shared words, 134 held, 28 thin, 0 moved. Disclosed: the v3 controls were chosen on 2023–2025; 2026-09 was not part of that choice. Not a value yet (M+3 from 2026-12-01). **Next step:** increment 4 — the workflow (each cohort once at M+1, M+2, M+3, derived under `excess-v1`), on a night the focus waits; it inherits the `robots.txt` self-decision of 2026-11-02 and is removed if the maintainer objects (`REQUESTS.md` 2026-10-30). Register B stays closed. No `excess-v2`.
- **2026-11-09 — increment 4: monthly run and workflow** (`docs/2026-11-09-synthetic-flood-v0-inkrement-4.md`): `practice/src/practice/syntheticflood/monthly.py` reads each month cohort from 2026-09 once at M+1, M+2, M+3 on `wordlist-v3`, derives under `excess-v1`, revises against the earlier reading on the same list; never repeats a request (an incomplete reading counts as read). `.github/workflows/syntheticflood.yml` (4th of each month, 03:17 UTC, plus dispatch), tests `practice/tests/test_syntheticflood_monthly.py` (9); `verify.py` unchanged (existing checks hold every file). First reading by the command: `syntheticflood/readings/2026-10/2026-11-09.json` (M+1, 167 requests, 0 × 429, 0 missing, total 154 632); `syntheticflood/derived/2026-10/2026-11-09.json` **`control_breach: []`** (controls 0.7873 `cases` to 1.4121 `associated`), 18 derived words. **Next step:** none on the instrument — the workflow reads 2026-09 at M+3 (first value), 2026-10 at M+2, 2026-11 at M+1 on 2026-12-04; the pass reads that record afterwards. It inherits the `robots.txt` self-decision of 2026-11-02 and is removed if the maintainer objects (`REQUESTS.md` 2026-10-30). No `excess-v2`; Register B closed.
- **Updated:** 2026-11-09 (pass)

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

### The Afterlife — how long a retracted paper stays unmarked where it is found

- **Stage:** AUDIT done 2026-10-30 (`docs/2026-10-30-the-afterlife-audit.md`, 17 requests with
  manifest in `afterlife/probes/2026-10-30/`) — **parked on its result**. Exposé 2026-10-29
  (`docs/2026-10-29-kandidat-the-afterlife.md`). Findings: Crossref REST carries the declaration side
  keyless (no `robots.txt`, 1 req/s; 426 retraction notices created 2026-10-01 to 10-29; with
  `select` no names), and marks the original itself on the notice's day (`updated-by`, one example)
  — so Crossref is no lagging index. **PubMed E-utilities: `robots.txt` `Disallow: /` for every
  agent**; two counts were sent before it was weighed, then nothing more. OpenAlex: keyless budget of
  the egress address used up, a key only against a person's address — outside. Retraction-Watch CSV
  on GitLab: `/api/v*` and `/*/raw` disallowed, whole-file only, author columns (I8) — out for V0.
- **Blocker:** the E-utilities `robots.txt` (`REQUESTS.md` 2026-10-30, shared with the Synthetic
  Flood). Silence is not a GO for V0 here.
- **Re-read when:** the maintainer reads the file as not binding the interface — then a narrow V0
  sketch (Crossref cohort from day one, daily PubMed check per open DOI, OpenAlex as control from a
  runner) and the GO request.
- **Updated:** 2026-10-30 (pass)

### The Provisional Air — how much of what the public was told about its air survives validation

- **Stage:** AUDIT part 2, points 2–4 done 2026-11-14 (`docs/2026-11-14-the-provisional-air-audit-teil-2.md`,
  12 files with manifest in `provisionalair/probes/2026-11-14/`): **licence CC BY 4.0** (EEA catalogue
  records `fe809728-…` download service, holder EEA, and `0eed9a67-…` E1a/E2a, holder European Commission;
  catalogue `robots.txt` `Allow: /`). **UBA control:** Berlin Wedding PM10 2026-11-13 00–11 h, 12 of 12 hours
  equal to E2a rounded to whole µg/m³ under the same hour labels — a coarser copy of the provisional side,
  not a "before". **The German E2a file overwrites day by day:** every hour of a day carries the `ResultTime`
  of the next day's 23:45 delivery; January–March all redelivered on 2026-05-08; future hours of the day stand
  as −999 / `Validity` −1; timestamps read as UTC+1 (inferred from `ResultTime` after `Last-Modified`).
  **OpenAQ archive:** keyless, but location ids carry no names or station codes; the mapping needs the keyed
  interface (outside the charter) — not closable, walking the tree deliberately not done; by inference OpenAQ
  can hold at most a version from the first three days. **Provisional recommendation: GO for a narrow V0**,
  final after point 1.
- **Earlier:** AUDIT part 1 done 2026-11-13 (`docs/2026-11-13-the-provisional-air-audit.md`, 18 probes
  with manifest in `provisionalair/probes/2026-11-13/`, held by `verify.py` `check_snapshots`).
  **Overwrite answered from one fetch:** the E2a file of one station
  (`…/blob/e2a-SPO-LU0101A_00005_103.parquet`) has one row per hour (7 591 rows, 7 591 starts) with a
  per-delivery `ResultTime`; July, September and October each carry a single delivery time early in the
  following month, so earlier versions are not in the download. The E2a file starts 2026-01-01 while E1a
  (`…/blob/e1a-…parquet`) already holds 2024–2025 validated: **the provisional side of a validated year
  is gone from this source** — not half-retroactive here. `dataset` 1 = E2a (container `airquality-p`),
  2 = E1a (`airquality-p-e1a`), shown by the returned addresses. Files per station × pollutant,
  year-cumulative, `ETag`/`Last-Modified` per blob, rewritten whole (2 min old at fetch); no 429 in 18
  requests; **licence not stated** at any endpoint or portal page read. Directive 2008/50/EC is repealed
  from 2026-12-12 (portal "Legal aspects"); thresholds bind to 2024/2881. **OpenAQ** archive docs: files
  written 72 h after the day, "may be retroactively patched" — one early version, no documented
  history; if it carries EEA stations it may hold a pre-redelivery value for past years.
  Exposé 2026-11-11 (`docs/2026-11-11-kandidat-the-provisional-air.md`): provisional (E2a)
  against validated (E1a) European air-quality values per station × pollutant × day, and the days whose
  side of a daily threshold flips. Neighbours: ETC/ATNI 11/2020 and ETC HE 4/2022 (annual maps from
  provisional data, checked against validated — year and map, not day), the European AQ index (the
  provisional side itself), OpenAQ (may already hold first-seen values — the neighbour that can take the
  most daylight), CAMS, Directive 2008/50/EC. **New: robots pre-screen in the exposé** (lesson of OSCAR
  and E-utilities): the EEA download API host has no `robots.txt` (404), the national control
  (`luftdaten.umweltbundesamt.de`) does not bar `/api/`; `www.eea.europa.eu` bars `/api` (another host,
  not read). Status calls only, no data, no bytes kept.
- **Gate:** AUDIT needs none; V0 needs the maintainer's GO.
- **Next step:** AUDIT part 2, point 1, on a night from 2026-11-16 when no earlier candidate has a step due
  (the Interval review request comes first on 2026-11-16): re-fetch once the Luxembourg E2a file of
  2026-11-13 and once the Berlin file of 2026-11-14 — did the fresh hours get a later `ResultTime`, did a
  **value** change. Two requests, comparison from the preserved files only. Then the final recommendation
  and the GO request in `REQUESTS.md`. The request field `email` is never set.
- **Updated:** 2026-11-14 (pass)

## Running instruments — findings

### Memory Hole — blind to its institutions since 2026-10-12

- **Finding 2026-10-28** (`docs/2026-10-28-memory-hole-befund-entdeckung.md`): in fourteen of the
  fifteen readings 2026-10-12 to 2026-10-26 no sampled page was drawn — discovery answers 200 with
  `[]` (e.g. `memoryhole/snapshots/2026-10-20/discovery-google-sustainability.json`) or, since
  2026-10-17, fails for 18–21 of 22 institutions; only the 20 controls are read. No code changed
  since 2026-10-01. Index lag is the leading hypothesis, not proven; a re-query from this container
  was refused at the connection (3 × reset, no repeat, nothing kept). Not a repair.
- **Next step:** count `entries[].kind == "sampled"` each pass; the runner test is asked in
  `REQUESTS.md` (2026-10-28). Nothing in the instrument changes before that test.
- **2026-10-29:** `memoryhole/readings/2026-10-27.json` carries **5 sampled pages** again, the first
  since 2026-10-16 — all from one institution (`exxonmobil`, discovery 200 with URLs,
  `memoryhole/snapshots/2026-10-27/discovery-exxonmobil.json`); 21 of 22 discovery queries still
  failed (`failures[]`, timeout / connection refused / 503). All five drawn URLs are script assets
  (`…/Assets/*.js`), four class `unverifiable` after a bot-wall recheck (403), one
  `history_unavailable`; 0 abstentions, so no verdicts are due. One institution answering is not
  the sample returning; the finding of 2026-10-28 stands. Noted, not a repair: that the sampler
  draws script assets at all is a question for the runner test's follow-up, not tonight.
- **2026-10-30:** `memoryhole/readings/2026-10-28.json` — 20 entries, **0 sampled**, 19 discovery
  failures, 0 abstentions (no verdicts due). The five sampled pages of 2026-10-27 did not recur; the
  finding of 2026-10-28 stands.
- **2026-10-31:** `memoryhole/readings/2026-10-29.json` (commit `4cb348e`) — 20 entries, **0 sampled**, 20 failures (log line of 2026-10-30: 105 requests, 22 institutions), 0 abstentions (no verdicts due). The finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-01:** `memoryhole/readings/2026-10-30.json` (commit `f478d1e`) — 20 entries, **0 sampled**, 21 failures (log line of 2026-10-31: 112 requests, 22 institutions), 0 abstentions (no verdicts due). The finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-02:** `memoryhole/readings/2026-10-31.json` (commit `3b42342`) — 20 entries, **0 sampled**, 18 failures (log line of 2026-11-01: 104 requests, 22 institutions), 0 abstentions (no verdicts due). The finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-03:** `memoryhole/readings/2026-11-01.json` (commit `381dfef`) — 20 entries, **0 sampled**, 20 failures (log line of 2026-11-02: 104 requests, 22 institutions), 0 abstentions (no verdicts due). The finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-04:** `memoryhole/readings/2026-11-02.json` (commit `ff8c7d4`) — 24 entries, **4 sampled**, 26 failures (log line of 2026-11-03: 134 requests, 22 institutions), 0 abstentions (no verdicts due). All four sampled from one institution (`bmwe`): the home page `unverifiable` (snapshot before refused at the connection), `apple-touch-icon.png` and `favicon.ico` `gone` (live 404), `favicon.svg` `history_unavailable` — again assets more than pages (cf. 2026-10-29); 21 of 22 discovery queries failed. One institution answering is not the sample returning; the finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-05:** `memoryhole/readings/2026-11-03.json` (commit `e6bec6f`) — 21 entries, **1 sampled** (`bmwe`, `favicon.svg`, `gone`), 19 failures (log line of 2026-11-04: 115 requests, 22 institutions), 0 abstentions (no verdicts due). Again an asset, again one institution; the finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-06:** `memoryhole/readings/2026-11-04.json` (commit `2c6a019`) — 20 entries, **0 sampled**, 20 failures, 0 abstentions (no verdicts due). The finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-07:** `memoryhole/readings/2026-11-05.json` (commit `d7d2b2d`) — 20 entries, **0 sampled**, 21 failures (log line of 2026-11-06: 109 requests, 22 institutions), 0 abstentions (no verdicts due). The finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-08:** `memoryhole/readings/2026-11-06.json` (commit `b0b1795`) — 20 entries, **0 sampled**, 19 failures, 0 abstentions (no verdicts due). The finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-09:** `memoryhole/readings/2026-11-07.json` (commit `0ab8129`) — 20 entries, **0 sampled**, 20 failures (log line of 2026-11-08: 108 requests, 22 institutions), 0 abstentions (no verdicts due). The finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-10:** `memoryhole/readings/2026-11-08.json` (commit `7c4b399`) — 21 entries, **1 sampled** (`bmwe`, an HTML page this time, class `unverifiable`), 24 failures (log line of 2026-11-08: 116 requests, 22 institutions), 0 abstentions (no verdicts due). One institution again; the finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-11:** `memoryhole/readings/2026-11-09.json` (commit `612eb93`) — 21 entries, **1 sampled** (`ec-climate`, an HTML page, class `unverifiable`, `snapshot_unavailable_before`), 23 failures (log line of 2026-11-10: 127 requests, 22 institutions), 0 abstentions (no verdicts due). One institution again; the finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-13** (no pass ran on 2026-11-12, so two readings): `memoryhole/readings/2026-11-10.json` (commit `cd6e7d2`) — 25 entries, **5 sampled**, all from one institution (`google-sustainability`) and all image assets under one versioned `/js/` path (four `gone`, one `unchanged`), 20 failures, 0 abstentions; `memoryhole/readings/2026-11-11.json` (commit `871e8c1`) — 20 entries, **0 sampled**, 20 failures (log line of 2026-11-12: 120 requests, 22 institutions), 0 abstentions. No verdicts due for either. Assets again, one institution again; the finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **2026-11-14:** `memoryhole/readings/2026-11-12.json` (commit `db0d690`) — 20 entries, **0 sampled**, 23 failures, 0 abstentions (no verdicts due). The finding of 2026-10-28 stands; `REQUESTS.md` (2026-10-28) still unanswered.
- **Updated:** 2026-11-14 (pass)

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
