"""Sentence-level diff.

The origin records removals only — redaction is taking away. Memory Hole needs
the replacement side too: "the number was revised" and "the negation was
flipped" are statements about a pair, not about an absence. So the diff keeps
three things: removed sentences, added sentences, and aligned pairs where a
sentence was rewritten rather than dropped.

Alignment is the token-set similarity used by the origin's world chamber
(`world/triviality.py`), at a floor set here: below it, a "replace" opcode is
two independent operations (something went, something else came), not one
rewrite.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field

TEXTDIFF_VERSION = "textdiff-v1"

# Below this token-set similarity, a replace opcode is a removal plus an
# addition rather than a rewrite of the same sentence.
ALIGN_FLOOR = 0.5

_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_WORD = re.compile(r"[^\W_]+", re.UNICODE)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT_SPLIT.split(text.strip()) if s.strip()]


def tokens(text: str) -> list[str]:
    return _WORD.findall(text)


def similarity(a: str, b: str) -> float:
    ta = {t.casefold() for t in tokens(a)}
    tb = {t.casefold() for t in tokens(b)}
    union = ta | tb
    if not union:
        return 0.0
    return len(ta & tb) / len(union)


@dataclass(frozen=True)
class Diff:
    removed: list[str] = field(default_factory=list)
    added: list[str] = field(default_factory=list)
    pairs: list[tuple[str, str]] = field(default_factory=list)

    @property
    def removed_tokens(self) -> int:
        return sum(len(p.split()) for p in self.removed)


def _align(before: list[str], after: list[str]) -> tuple[
        list[tuple[str, str]], list[str], list[str]]:
    """Greedy best-match alignment inside one replace block. Deterministic:
    candidates are consumed in index order, ties go to the earlier index."""
    pairs: list[tuple[str, str]] = []
    unmatched_after = list(range(len(after)))
    matched_before: set[int] = set()
    for i, a in enumerate(before):
        best_j = None
        best_score = ALIGN_FLOOR
        for j in unmatched_after:
            score = similarity(a, after[j])
            if score > best_score:
                best_score = score
                best_j = j
        if best_j is not None:
            pairs.append((a, after[best_j]))
            unmatched_after.remove(best_j)
            matched_before.add(i)
    removed = [a for i, a in enumerate(before) if i not in matched_before]
    added = [after[j] for j in unmatched_after]
    return pairs, removed, added


def diff(before: str, after: str) -> Diff:
    a, b = sentences(before), sentences(after)
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    removed: list[str] = []
    added: list[str] = []
    pairs: list[tuple[str, str]] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "delete":
            removed.extend(a[i1:i2])
        elif tag == "insert":
            added.extend(b[j1:j2])
        elif tag == "replace":
            block_pairs, block_removed, block_added = _align(a[i1:i2], b[j1:j2])
            pairs.extend(block_pairs)
            removed.extend(block_removed)
            added.extend(block_added)
    return Diff(removed=removed, added=added, pairs=pairs)
