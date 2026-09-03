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
