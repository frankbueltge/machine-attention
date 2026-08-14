"""The watchlist — whose memory, and how it is asked for.

The list itself lives in `memoryhole/watchlist.json` (data, not code, because
curation is editorial work and should be readable without Python). This module
loads it, validates it, and enforces the two rules the audit made structural:

  * every institution carries the query strategy that was **probed live**, with
    the probe result that justifies it — audit condition 1. A host is not
    configured, it is tried;
  * the origin's 32 pages are excluded by URL. Chamber 1 of Editorial Deadline
    keeps its pages untouched; Memory Hole doubles none of them.

Categories: A German federal level · B EU regulators and Commission ·
C German regulators and supervision · D corporations with public
self-commitments · E the control group, whose whole job is to make the
instrument's own false-positive rate a number.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

WATCHLIST_PATH = "memoryhole/watchlist.json"
CATEGORIES = ("A", "B", "C", "D", "E")
STRATEGIES = ("domain", "prefix", "single_url")


def page_id(url: str) -> str:
    """Stable, filesystem-safe identity for one page, in the record and in the
    snapshot file names."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def rank(day: str, url: str) -> str:
    """Deterministic sampling rank. A hash of day and URL, so the sample is
    reproducible by anyone holding the preserved discovery bytes — and so the
    instrument cannot be accused of choosing its pages after seeing them."""
    return hashlib.sha256(f"{day}|{url}".encode("utf-8")).hexdigest()


def load(repo_root: Path) -> dict:
    path = repo_root / WATCHLIST_PATH
    doc = json.loads(path.read_text(encoding="utf-8"))
    problems = validate(doc)
    if problems:
        raise SystemExit("watchlist is invalid:\n  - " + "\n  - ".join(problems))
    return doc


def excluded_urls(doc: dict) -> set[str]:
    return set(doc.get("excluded", {}).get("urls", []))


def validate(doc: dict) -> list[str]:
    """Schema and the two structural rules. Returns the problems, so a test can
    hold the committed file to them."""
    problems: list[str] = []
    if not doc.get("version"):
        problems.append("missing version")

    excluded = excluded_urls(doc)
    if not excluded:
        problems.append("excluded.urls is empty — chamber 1's pages must be "
                        "named to be avoided")

    institutions = doc.get("institutions", [])
    if not institutions:
        problems.append("no institutions")
    slugs: set[str] = set()
    for entry in institutions:
        slug = entry.get("slug", "?")
        if slug in slugs:
            problems.append(f"{slug}: duplicate slug")
        slugs.add(slug)
        if entry.get("category") not in CATEGORIES[:4]:
            problems.append(f"{slug}: category {entry.get('category')!r} is "
                            "not one of A-D")
        strategy = entry.get("strategy")
        if strategy not in STRATEGIES:
            problems.append(f"{slug}: strategy {strategy!r} is not one of "
                            f"{STRATEGIES}")
        if strategy == "single_url":
            if not entry.get("urls"):
                problems.append(f"{slug}: single_url strategy without urls")
        elif not entry.get("query"):
            problems.append(f"{slug}: no query target")
        probe = entry.get("probe")
        if not isinstance(probe, dict) or not probe.get("at"):
            problems.append(f"{slug}: no live probe recorded — condition 1 of "
                            "the audit is that a strategy is proved, not "
                            "configured")
        elif "http_status" not in probe:
            problems.append(f"{slug}: probe without an http_status")
        for url in entry.get("urls", []):
            if url in excluded:
                problems.append(f"{slug}: {url} is watched by chamber 1")

    controls = doc.get("controls", [])
    if len(controls) < 15:
        problems.append(f"only {len(controls)} control pages — the control "
                        "group is the E-experiment's measuring instrument, "
                        "not decoration")
    seen: set[str] = set()
    for control in controls:
        url = control.get("url", "?")
        if control.get("category") != "E":
            problems.append(f"control {url}: category must be E")
        if url in seen:
            problems.append(f"control {url}: duplicate")
        seen.add(url)
        if url in excluded:
            problems.append(f"control {url}: is watched by chamber 1")
        probe = control.get("probe")
        if not isinstance(probe, dict) or "http_status" not in probe:
            problems.append(f"control {url}: no live probe recorded")
    return problems
