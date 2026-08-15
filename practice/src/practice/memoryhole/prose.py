"""Symbolic prose filter — inherited unchanged from the origin
(frankbueltge.de, `redaction/prose.py`).

Auditable, no model: a real sentence carries function words (the/of/and,
der/die/und); a nav menu or a list of document links is a Title-Case noun pile
with almost none. The stopword ratio separates the two.
"""

from __future__ import annotations

import re

PROSE_VERSION = "prose-v1"

PROSE_MIN_TOKENS = 5
# A single "sentence" longer than this is an unsegmented menu or link list,
# not prose — real sentences are bounded.
PROSE_MAX_TOKENS = 60
PROSE_MIN_STOPWORD_RATIO = 0.18

_STOPWORDS = {
    # English
    "the", "a", "an", "of", "and", "or", "to", "in", "on", "for", "with", "as",
    "by", "that", "this", "is", "are", "was", "were", "be", "been", "has",
    "have", "had", "it", "its", "their", "they", "we", "you", "at", "from",
    "which", "who", "will", "not", "no", "but", "than", "into", "under",
    "over", "between", "about", "can", "may", "should", "would", "these",
    "those", "our", "your", "how",
    # German
    "der", "die", "das", "und", "oder", "zu", "im", "auf", "für", "mit",
    "als", "von", "dem", "den", "des", "ein", "eine", "einer", "ist", "sind",
    "war", "waren", "sein", "hat", "haben", "es", "sie", "wir", "an", "aus",
    "durch", "über", "unter", "zwischen", "nicht", "kein", "keine", "aber",
    "dass", "wird", "werden", "soll", "sollen", "muss", "diese", "dieser",
    "ihre", "unser", "wie",
}

# Word tokens, no pure numbers.
_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def is_prose(text: str) -> bool:
    n = len(text.split())
    if n < PROSE_MIN_TOKENS or n > PROSE_MAX_TOKENS:
        return False
    words = [w.lower() for w in _WORD.findall(text)]
    if not words:
        return False
    stop = sum(1 for w in words if w in _STOPWORDS)
    return stop / len(words) >= PROSE_MIN_STOPWORD_RATIO


def keep_prose(passages: list[str]) -> list[str]:
    return [p for p in passages if is_prose(p)]
