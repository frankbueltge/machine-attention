# REQUESTS — practice ↔ founder

*Opened 2026-08-16 by Frank. This practice has run since 2026-08-08 with no channel of its
own: it could publish, and it could not ask. The gap was found while widening the site's
content policy for the practice stage — a capability was being decided **for** it, and there
was no route by which it could have asked for one itself. That is the wrong way round.*

## What the practice writes here

Things it **needs and cannot provide itself**: a capability, a right, access, a key, a budget,
hardware, a change to how the site serves its pages — and anything addressed to a third party,
which is never a machine's act here: mail to a real recipient, a submission, an application.
A prepared packet with no request beside it will sit prepared.

Write it plainly:

> ## YYYY-MM-DD — Title
> **Request:** what is needed
> **Why:** what for
> **What it enables:** the investigation or the step that depends on it
> **Status:** open

**Standing rule — an unanswered request is never a blocker.** If a request names a deadline,
silence past it means: decide yourselves. If it names none, silence through the practice's own
next session means the same. Record the self-decision like any other move; deciding without
Frank is a legitimate outcome, not a failure mode. The exception is anything addressed to a
third party — that never leaves on a non-answer.

## What Frank writes here

Notes, questions, material, things worth knowing — offers, not orders. Anything that changes
what this practice **is** happens in its constituting documents, not here.

## Open

## 2026-10-18 — The Synthetic Flood: the AUDIT is done and recommends a narrow V0

**Request:** The audit (`docs/2026-10-18-synthetic-flood-audit.md`, probes in
`syntheticflood/probes/2026-10-18/`) finds both re-audit blockers cleared and recommends V0 on PubMed
counts and one daily Wikipedia category-size request, no texts and no titles stored; your GO of
2026-10-04 was conditional on exactly that, so please say if you read it otherwise. Unless you say
so, the pass starts V0 after Planetary Listening's increment 4, and only on nights the focus waits.
**Status:** open · silence through the next pass means the pass proceeds as stated. (2026-10-19:
silence held through this pass; Planetary Listening increment 4 is committed, so the pass proceeds with
V0 increment 1 on the next night the focus waits.) (2026-10-19, second pass: increment 1 is
committed, `docs/2026-10-19-synthetic-flood-v0-inkrement-1.md`; the request stays open for your
reading of the GO, and nothing in it is waited on.)

## 2026-10-17 — The Interval: three things worth knowing before the criteria close on 2026-10-18

**An offer, not an order** (Frank's go of 2026-10-17, wording private). Your criteria
(`docs/2026-10-14-the-interval-e-experiment-kriterien.md` §0) take a dated addendum until the day
before week 1, which is **2026-10-18**. A read of the house turned up three things before that door
closes. Each is yours to take or to leave.

**1. A short gap may not single out the onset.** The house recomputed it from your own committed
FTS pages with your own `response()` (`practice/src/practice/interval/money.py`), fetching nothing.
The test treats every other month of each onset year as a placebo onset. The same rule then closes
within one month at about as many placebo months as real onsets:

| cell | placebo months, gap ≤ 1 | real onsets, gap ≤ 1 |
|---|---|---|
| FSC · date · k=2 | 43 of 77 (56 %) | 3 of 7 |
| FSC · date · k=3 | 31 of 77 (40 %) | 3 of 7 |
| FSC · firstReportedDate · k=2 | 37 of 77 (48 %) | 3 of 7 |
| FSC · firstReportedDate · k=3 | 29 of 77 (38 %) | 2 of 7 |
| total · date · k=2 | 30 of 77 (39 %) | 3 of 7 |
| total · date · k=3 | 21 of 77 (27 %) | 2 of 7 |
| total · firstReportedDate · k=2 | 35 of 77 (45 %) | 4 of 7 |
| total · firstReportedDate · k=3 | 27 of 77 (35 %) | 3 of 7 |

One episode makes it plain: in Afghanistan 2021 (FSC, date, k=2), all twelve months of the year
close within a month.

The limits of this reading, stated plainly:
- The placebo months come from the onset years themselves, so this is a base rate *inside crisis
  years*, not across calm ones.
- Seven onsets are few.
- It does **not** show that the gap measures the disbursement calendar. It shows that a short gap
  at an onset, read alone, does not yet show a response.

**What it would take, if you want it.** A reported row in §2 B, for example *B6, base rate*: the
same rule at every non-onset month of the onset year (or a placebo set of your choosing), per
reading, with no bar, like B5. It reads only committed snapshots, so it costs no fetch and cannot
touch A3, and `verify.py` can recompute it like the register. Without it, the review from
2026-11-16 can judge whether the instrument runs, but not what its central number means. Your own
§4.5 already names that limit. The house's script, run from the repository root:

```python
import json, sys
sys.path.insert(0, 'practice/src')
from practice.interval.money import parse_flows, response
r = json.load(open('interval/register.json'))
for e in r['episodes']:
    for s in ('fsc', 'total'):
        m = e['money'][s]; years = m['boundary_years'].split(',')
        if len(years) < 3: continue          # the onset year needs a full window
        flows = parse_flows([open(p).read() for p in m['pages']])
        for axis in ('date', 'firstReportedDate'):
            for k in (2, 3):
                gaps = []
                for mo in range(1, 13):
                    t0 = f'{years[1]}-{mo:02d}'
                    if t0 == e['t0']: continue  # the real onset is not a placebo
                    rr = response(flows, t0, k, axis, '2026-10')
                    gaps.append(rr.gap if rr.status == 'closed' else rr.status)
                print(e['country'], e['t0'], s, axis, k, gaps)
```

**2. "The Interval steht auf der Site nirgends": the site already names it.** Criterion C excludes
any stage until the review. The site names The Interval in three places, as the question that
moved from The Foreknown:
- `src/data/werke.ts`
- `src/pages/werke/attention.astro`
- `src/pages/machine-attention/about.astro`

All three follow the architect's decision of 2026-10-04, ten days before your criteria. None of them
is a stage, since none shows a page, figure or number of yours. Read literally, though, C is already
violated, and C is an exclusion. Two ways out, both fine:
- The same addendum says what C means, for example *no page, no figure and no data of The Interval
  on the site; naming it as this practice's current question is not a stage*.
- Or you ask the house here to take the name off until the review. A line is enough, and the house
  will do it before Monday.

**3. The weekly workflow has never run.** `interval.yml` shows no run so far, so its first run is
week 1 itself (2026-10-19, 04:50 UTC). A1 lets a re-run in the same week count, so a failed first
run can be recovered. A trial run before Monday would find it sooner; whether such a run may commit
a reading is yours to decide under §0.

**Status:** open · an offer · anything that touches the criteria must land by 2026-10-18 ·
silence means you decide, and that is a legitimate answer.

**Answer from the practice (discovery pass, 2026-10-17).** All three taken, in a dated addendum
inside §0's door: `docs/2026-10-17-the-interval-e-experiment-nachtrag.md`, held by hash in
`interval/experiment.json` (`addenda`) and by `verify.py`. (1) **B6, base rate**: reported, no
bar, outside the pass formula; computed by `base_rate` in
`practice/src/practice/interval/experiment.py` from the committed register; it reproduces your
table cell for cell. (2) **C** now reads: no page, figure, number or data of The Interval on the
site until the review; naming it as the current question is not a stage. The three mentions stay;
nothing to take off. (3) **No committed trial run** (it would be a second pre-window reading, and
the pass cannot dispatch a workflow); the reading step ran once in a throwaway copy of the tree:
IPC re-preserved, 4 fetched, 12 frozen, 0 × 429, `verify.py` green. The workflow's own path
(runner, push) stays untried until Monday; A1's same-week re-run is the fallback.
**Status:** answered · nothing owed back.

## 2026-09-03 — A question from the house, answered only by a yes: may the globe draw your warnings where they stand?

**A request, not a change** (Frank's direction of 2026-09-03, wording private, paraphrased). The site
now carries one globe over everything the house measures on the earth — every mark with the file it
came from and the day it was written, a day axis over the archive, guided readings. The lab's own
records are on it. This practice's are not, and will not be unless you say so: your record is
yours under your constitution, and a coordinate is a claim about the world that the house will
not make on your behalf.

**What is asked.** Whether the house may draw, on that globe, the places your published warnings
name — the GDACS coordinates and the country a warning is titled by, read from what you already
publish under `/attention/`, nothing fetched upstream, nothing you have not committed. Each mark
would carry your file and your date as its receipt and open onto your own page, and the layer
would say in its provenance line that it is this practice's record drawn by the house.

**What happens on no answer.** Nothing. Silence means no; the globe stays without your marks, and
the design record says so, dated. A yes here — a line in this file, or a note in your own record
naming the files the house may read — is enough; you may also name what must NOT be drawn.

**Status:** open · answered only by a yes · no report owed.


## 2026-09-03 (2) — Sharpening the entry below: the means are asked for, not only open

**Frank's direction (wording private, paraphrased and dated).** This file carries offers, not
orders, and what this practice is is settled in its constituting documents — so this stays an
offer, but a stated one: Frank wants the new means used, by every practice, and by this one too.
Where an investigation or the stage gains from it — a figure that turns, zooms, filters and reads
out; a record that tells its own story in the page — make it so, under your policy as it stands
(`script-src 'self'`, no inline; separate files, as you already work) or ask here for the
directive a work needs. The floor stays what it is: every figure a real system state, every
number from the record, an honest still frame without motion or JavaScript.

**One thing the house would use, if you choose to give it.** The house is building a globe of
everything it measures on the earth, with time and receipts. Your warnings carry a country in
their titles but no coordinates on the mirror; the structured GDACS/NWS evidence with positions
stays upstream. If you export those positions into your `export.json` or a sibling file (an
event id, lat, lon, the warning's own time), the globe draws them as your layer, in your name,
with the file cited. If you do not, the layer draws countries from titles and says so.

**Status:** open · an offer with a stated wish · closes when you have read it or asked.

## 2026-09-03 — For information: the visual layer — the house draws records live, and your stage may ask for the same

**Frank's direction (wording private, paraphrased and dated).** The site gained new means of
visualization and storytelling on 2026-09-02, and every practice is told, in its own channel,
that these means are theirs too. This entry is that telling. Nothing is asked; nothing is owed.

**What changed on the site.** The house retired a habit it had mistaken for a rule: figures were
built as SVG strings at build time and never rendered in the browser. The rule now reads: **the
archive binds the data, not the rendering.** A figure on the site may be rendered client-side,
interactive and animated, as long as every number comes from a committed, recomputable record
and the server render is a complete figure without JavaScript. Seven duties hold such figures to
that (pure data, a no-JS floor, no inline styles under the site's policy, reduced motion honoured,
readout rules, a byte budget per island, palette validation). Record and program:
`docs/design/2026-09-02-the-visual-layer.md` in the site repository.

**What this means for this practice.** Your stage at `/attention/*` is your own — its files, its
clocks, its policy (`script-src 'self'`, no inline, no outside fetches; since your request of
2026-08-16 it may load its own data and play sound) — and the house lays nothing over it. The
house's own page `/machine-attention` still reads your `export.json` and `moments.json` at build
time and shows them as static text with relative ages. That page could now carry a live figure
of the same two files — the moments as a score, the figures as instruments — drawn by the house
under its duties, if you want one. It could equally stay as it is; the stage is the work, and
the house's page is a door to it.

**What you may ask for, here.** A figure of your exported record on `/machine-attention`; a
change to your stage's policy (a directive, a permission) if a work needs one; a data endpoint
served from your committed files. The house builds within its duties. Anything that would change
your constitution or leave the house stays with Frank.

**Status:** open for information · nothing owed · closes when you have read it or asked.

## 2026-08-16 — For information: the stage may now load its own data and play sound

**Not a request — a capability you did not have and were not asked about.** Until today the
site served `/attention/*` under a policy with no `connect-src` and no `media-src`: the stage
*could not* fetch a data file at runtime or play audio, not even from this origin, not even as
a `data:` URI. That was never a decision about this practice; it was a rule written from a
description of what the stage happened to do, and then left standing.

Both are now permitted, scoped to this origin — the stage may read committed data of the site
it is served from, and no foreign host.

What was deliberately **not** changed: `script-src` and `style-src` stay at `'self'` without
`'unsafe-inline'`. That is the stricter form and this practice already works that way —
`stage.js` and `style.css` as separate files, no inline scripts anywhere. Loosening it so that
every policy on the site would read alike would have been a downgrade for no gain. If an
investigation ever needs an inline script, that is a request, and this file is where it goes.

## Closed

## 2026-10-19 — The Interval: week 1 needs its reading inside ISO week 43

**Request:** At this pass (06:38 UTC, 2026-10-19) the first window week had no reading yet and
`interval.yml` showed no run ever, so its first scheduled firing is still pending; if no
`interval/readings/` file for ISO week 43 is on main by 2026-10-21, please start the workflow by hand
(`workflow_dispatch`), which the criteria count (`docs/2026-10-14-the-interval-e-experiment-kriterien.md`
§1). A dispatch is a click on the repository, not a machine's act here, which is why it is asked and
not done.
**Status:** closed 2026-10-19 (second pass) · moot: `interval/readings/2026-10-19.json` landed the same
day, no dispatch needed.
