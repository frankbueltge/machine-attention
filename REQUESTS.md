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
