"""Symbolic, auditable salience — inherited from the origin
(frankbueltge.de, `redaction/salience.py`), weights and regexes unchanged.

No model. Every weight is disclosed and versioned. Here it does not gate a
daily ranking (Memory Hole has no exhibit) but describes how much weight a
recorded operation carried, so a reader can sort without the record ordering
institutions for them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

SALIENCE_VERSION = "salience-v1"

WEIGHTS: dict[str, int] = {
    "number": 2,
    "date": 2,
    "named_entity": 1,
    "negation": 2,
    "commitment_verb": 3,
}
CAP = 5  # occurrences of one signal counted at most CAP times

NUMBER = re.compile(
    r"(?<!\w)\d[\d.,]*\s?(?:%|percent|prozent|mio|million|millionen|mrd"
    r"|billion|bn)?",
    re.I,
)
DATE = re.compile(
    r"\b(?:19|20)\d{2}\b"
    r"|\b\d{1,2}\.\s?\d{1,2}\.\s?(?:19|20)\d{2}\b"
    r"|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec"
    r"|januar|februar|märz|mai|juni|juli|oktober|dezember)\b",
    re.I,
)
NEGATION = re.compile(
    r"\b(?:no|not|never|none|kein|keine|keinen|nicht|niemals)\b", re.I)
COMMIT = re.compile(
    r"\b(?:will|shall|must|commit|commits|committed|pledge|pledged|pledges"
    r"|wird|werden|muss|müssen|soll|sollen|verpflichtet)\b",
    re.I,
)
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_CAPWORD = re.compile(r"[A-ZÄÖÜ][\wÄÖÜäöüß]+")


@dataclass(frozen=True)
class Salience:
    score: int = 0
    signals: list[str] = field(default_factory=list)


def named_entity_count(text: str) -> int:
    """Capitalised words that are not sentence-initial — a deliberately simple,
    auditable heuristic for named entities."""
    n = 0
    for sentence in _SENT_SPLIT.split(text):
        words = sentence.split()
        for word in words[1:]:
            if _CAPWORD.match(word):
                n += 1
    return n


def score(text: str) -> Salience:
    counts = {
        "number": len(NUMBER.findall(text)),
        "date": len(DATE.findall(text)),
        "negation": len(NEGATION.findall(text)),
        "commitment_verb": len(COMMIT.findall(text)),
        "named_entity": named_entity_count(text),
    }
    signals = sorted(k for k, v in counts.items() if v > 0)
    total = sum(WEIGHTS[k] * min(counts[k], CAP) for k in signals)
    return Salience(score=total, signals=signals)
