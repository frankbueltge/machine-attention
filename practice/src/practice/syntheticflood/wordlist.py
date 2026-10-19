"""The committed word lists (Register A). A version file never changes; a new
list is a new file. Loading validates the shape the verifier also holds."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

LISTS = ("fixed", "controls", "pool")
WORD = re.compile(r"[a-z]+")


def path_for(repo_root: Path, version: str) -> Path:
    return repo_root / "syntheticflood" / "wordlists" / f"{version}.json"


def validate(doc: dict) -> list[str]:
    problems = []
    seen: dict[str, str] = {}
    for name in LISTS:
        words = doc.get(name)
        if not isinstance(words, list) or not words:
            problems.append(f"list {name} missing or empty")
            continue
        for w in words:
            if not isinstance(w, str) or not WORD.fullmatch(w):
                problems.append(f"{name}: {w!r} is not a lowercase ASCII word")
            elif w in seen:
                problems.append(f"{w!r} in both {seen[w]} and {name}")
            else:
                seen[w] = name
    return problems


def load(repo_root: Path, version: str) -> tuple[dict, str, str]:
    """Return (document, repo-relative path, SHA-256 of its bytes)."""
    path = path_for(repo_root, version)
    data = path.read_bytes()
    doc = json.loads(data)
    problems = validate(doc)
    if doc.get("version") != version:
        problems.append(f"file says version {doc.get('version')!r}")
    if problems:
        raise ValueError(f"{path.name}: " + "; ".join(problems))
    return doc, path.relative_to(repo_root).as_posix(), hashlib.sha256(data).hexdigest()


def terms(doc: dict) -> list[tuple[str, str]]:
    """(list name, word) in a fixed order: fixed, controls, pool."""
    return [(name, w) for name in LISTS for w in doc[name]]
