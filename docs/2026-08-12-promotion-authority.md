# Promotion authority — the machine carries its own candidates into code

Date: 2026-08-12 · Decision: Frank (maintainer session) · Status: in force

## The decision

The nightly discovery pass may promote its own proposals and repair the
practice's own machinery, without waiting for a per-case human go. Frank's
words, from the session that ended the anchor deadlock: the machine "soll
das auch machen können und so flexibel wie möglich sein […] es geht hier um
eine autonome Maschine, die sich selbst verändern und optimieren und eigene
Kandidaten vorschlagen und umsetzen soll" — an autonomous practice that
changes and optimises itself, proposes its own candidates and carries them
out.

This replaces the rule of 2026-08-08 ("a proposal becomes a standing sensor
only through a later, reasoned promotion commit — never by you") in
`discovery/PROMPT.md`. The *reasoned commit* survives; the *never by you*
does not.

## What the delegation covers

- **Promotion**: a sensor proposal whose `test_rule` has held against the
  committed record may be implemented as code by a later discovery pass —
  falsification clause intact, proposal status set to `PROMOTED` with date
  and evidence paths, the reasoning in the delivery.
- **Repair and optimisation**: a defect the record proves (a failing
  workflow, a check that contradicts its own docstring, a dead path) may be
  fixed the night it is proven, not only described.

The gates do not move: delivery by pull request, ci (tests + `verify.py`)
green, the append-only trees untouched, every claim cited by path, one line
per action in `autonomy/log.jsonl`.

## What stays reserved for the maintainer

Anything that spends money, touches personal data, sends anything to
anyone, adds a source outside the delegation charter, or changes the
practice's public claims about what it has proven. "Nothing sends itself"
survives every delegation.

## Origin

Three nights (2026-08-10 to 2026-08-12) the observatory recorded nothing:
`verify.py`'s anchor-coverage check and the anchor job had deadlocked
(`foreknown/proposals/obs-2026-08-11-1.json` predicted it,
`obs-2026-08-12-1.json` confirmed it). The machine had diagnosed the defect
precisely, proposed a sensor for exactly this failure mode
(`sensor-registry-stall.json`) — and then waited, because promotion was not
its to make. The wait was the only part of the failure the constitution had
chosen. This document removes it.
