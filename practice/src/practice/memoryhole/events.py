"""The event classifier — deterministic, versioned, rules first.

Method pattern: the origin's world chamber (`redaction/world/triviality.py`),
which types title rewrites with disclosed rules and no model in the loop. This
is the same shape applied to running text, and it is the reason Memory Hole is
its own investigation rather than the origin with more rows: the origin ranks
how much weight a removal carried; this names what was done to the sentence.

Five types, all of them operations on text:

  number_revised       a figure was rewritten in place
  date_shifted         a year or date was rewritten in place
  negation_flipped     a negation appeared or disappeared in a rewrite
  commitment_removed   a commitment verb was dropped (with the sentence or
                       out of it)
  attribution_removed  an ascription to a person or office was dropped

E-2 is the discipline these names carry: they say what happened to the text,
never why. "Institution X is covering up" is not an output of this module and
must not become one. I8 is enforced structurally rather than by good
intentions: any passage carrying an attribution marker is recorded as a digest,
never as text, so a name in a register line is impossible by construction — and
verify.py rechecks that.

What the rules cannot decide is recorded as an abstention. That, and only that,
is what the model layer may look at.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import dataclass

from . import prose, salience
from .textdiff import Diff, tokens

EVENTS_VERSION = "events-v1"

NUMBER_REVISED = "number_revised"
DATE_SHIFTED = "date_shifted"
NEGATION_FLIPPED = "negation_flipped"
COMMITMENT_REMOVED = "commitment_removed"
ATTRIBUTION_REMOVED = "attribution_removed"

TYPES = (NUMBER_REVISED, DATE_SHIFTED, NEGATION_FLIPPED, COMMITMENT_REMOVED,
         ATTRIBUTION_REMOVED)

_NUMERIC_TOKEN = re.compile(r"^\d[\d.,]*$")
_YEARLIKE = re.compile(r"^(?:19|20)\d{2}$")
_MONTH = re.compile(
    r"\b(?:january|february|march|april|may|june|july|august|september"
    r"|october|november|december|januar|februar|märz|mai|juni|juli|august"
    r"|september|oktober|november|dezember)\b", re.I)

# Ascription to a person or an office. Deliberately coarse: a false positive
# costs a passage its text in the record (a digest stands in its place), which
# is the safe direction under I8.
ATTRIBUTION = re.compile(
    r"\b(?:according to|as stated by|said|says|stated|told|announced by"
    r"|spokesperson|spokeswoman|spokesman|director|minister|president"
    r"|commissioner|chairman|chairwoman|chair of|head of|dr\.|prof\."
    r"|laut|zufolge|sagte|sagt|erklärte|betonte|teilte mit|nach angaben"
    r"|sprecher|sprecherin|präsident|präsidentin|minister|ministerin"
    r"|staatssekretär|direktor|direktorin|leiter|leiterin|vorstand)\b",
    re.I)


@dataclass(frozen=True)
class Event:
    type: str
    rule: str
    before_sha256: str
    after_sha256: str | None = None
    before: str | None = None
    after: str | None = None
    salience: int = 0
    signals: tuple[str, ...] = ()


@dataclass(frozen=True)
class Abstention:
    before_sha256: str
    before: str | None
    after: str | None
    salience: int
    signals: tuple[str, ...]


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def carries_attribution(text: str) -> bool:
    return bool(ATTRIBUTION.search(text))


def _numeric(values: list[str]) -> Counter:
    return Counter(t for t in values if _NUMERIC_TOKEN.match(t))


def _is_datelike(token: str) -> bool:
    return bool(_YEARLIKE.match(token))


def _count(pattern: re.Pattern, text: str) -> int:
    return len(pattern.findall(text))


def classify_pair(before: str, after: str) -> list[tuple[str, str]]:
    """Rules for one aligned rewrite. Several may fire; order is fixed."""
    verdicts: list[tuple[str, str]] = []
    tb, ta = tokens(before), tokens(after)
    nb, na = _numeric(tb), _numeric(ta)
    if nb != na:
        gone = list((nb - na).elements())
        came = list((na - nb).elements())
        changed = gone + came
        if any(_is_datelike(t) for t in changed):
            verdicts.append((DATE_SHIFTED, "year rewritten in place"))
        if any(not _is_datelike(t) for t in changed):
            verdicts.append((NUMBER_REVISED, "figure rewritten in place"))
    elif _MONTH.search(before) and not _MONTH.search(after):
        verdicts.append((DATE_SHIFTED, "month name dropped from the sentence"))

    if _count(salience.NEGATION, before) != _count(salience.NEGATION, after):
        verdicts.append((NEGATION_FLIPPED, "negation count changed"))

    if _count(salience.COMMIT, before) > 0 and _count(salience.COMMIT, after) == 0:
        verdicts.append((COMMITMENT_REMOVED, "commitment verb dropped in rewrite"))

    if carries_attribution(before) and not carries_attribution(after):
        verdicts.append((ATTRIBUTION_REMOVED, "ascription dropped in rewrite"))

    return verdicts


def classify_removal(text: str) -> list[tuple[str, str]]:
    """Rules for a sentence that was dropped outright."""
    verdicts: list[tuple[str, str]] = []
    if _count(salience.COMMIT, text) > 0:
        verdicts.append((COMMITMENT_REMOVED, "sentence with commitment verb removed"))
    if carries_attribution(text):
        verdicts.append((ATTRIBUTION_REMOVED, "sentence with an ascription removed"))
    return verdicts


def _event(kind: str, rule: str, before: str, after: str | None) -> Event:
    """Build one event. A passage carrying an ascription is recorded as a
    digest only — I8: the name stays in the preserved bytes as evidence and
    never becomes the subject of the record."""
    redact = (kind == ATTRIBUTION_REMOVED
              or carries_attribution(before)
              or (after is not None and carries_attribution(after)))
    scored = salience.score(before)
    return Event(
        type=kind,
        rule=rule,
        before_sha256=sha256(before),
        after_sha256=sha256(after) if after is not None else None,
        before=None if redact else before,
        after=None if redact or after is None else after,
        salience=scored.score,
        signals=tuple(scored.signals),
    )


def classify(diff: Diff) -> tuple[list[Event], list[Abstention]]:
    """The whole chain for one before/after pair of pages.

    Only prose survives into classification: the extraction is a tag strip, so
    navigation residue is the normal case, not the exception.
    """
    events: list[Event] = []
    abstentions: list[Abstention] = []

    for before, after in diff.pairs:
        if not (prose.is_prose(before) or prose.is_prose(after)):
            continue
        verdicts = classify_pair(before, after)
        if verdicts:
            events.extend(_event(kind, rule, before, after)
                          for kind, rule in verdicts)
            continue
        scored = salience.score(before)
        if scored.score:
            redact = carries_attribution(before) or carries_attribution(after)
            abstentions.append(Abstention(
                before_sha256=sha256(before),
                before=None if redact else before,
                after=None if redact else after,
                salience=scored.score,
                signals=tuple(scored.signals)))

    for passage in prose.keep_prose(diff.removed):
        verdicts = classify_removal(passage)
        if verdicts:
            events.extend(_event(kind, rule, passage, None)
                          for kind, rule in verdicts)
            continue
        scored = salience.score(passage)
        if scored.score:
            abstentions.append(Abstention(
                before_sha256=sha256(passage),
                before=None if carries_attribution(passage) else passage,
                after=None,
                salience=scored.score,
                signals=tuple(scored.signals)))

    events.sort(key=lambda e: (e.type, e.before_sha256))
    abstentions.sort(key=lambda a: (-a.salience, a.before_sha256))
    return events, abstentions
