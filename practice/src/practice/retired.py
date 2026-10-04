"""Closing records of retired projects — one RETIRED.json per project directory.

The admission path pre-committed the word for an honest end
(docs/2026-08-08-projekt-aufnahme.md: "jederzeit: RETIRED" — honestly ended,
records kept, reason committed). The maintainer retired The Foreknown and Dark
Ocean on 2026-10-04 (wording private; docs/2026-10-04-foreknown-retired.md,
docs/2026-10-04-dark-ocean-retired.md). Nothing is deleted: a retired
project's records stay as they were on its last night, and verify.py keeps
holding them — and fails any night recorded after it.

Who reads it: the export (status word), the staleness check (a retired
register is reported, not judged), verify.py, and — for The Foreknown, the
only project that had a stage — the stage and the moments.
"""

from __future__ import annotations

from pathlib import Path

from .preserve import read_json

REQUIRED = ("project", "status", "last_night", "decided", "record", "reason")


def retired_file(project: str) -> Path:
    return Path(project) / "RETIRED.json"


def read_retired(repo_root: Path, project: str) -> dict | None:
    """The project's closing record, or None while it runs."""
    path = retired_file(project)
    record = read_json(repo_root / path, None)
    if not record:
        return None
    missing = [key for key in REQUIRED if not record.get(key)]
    if missing:
        raise ValueError(f"{path}: missing {', '.join(missing)}")
    if record["status"] != "RETIRED" or record["project"] != project:
        raise ValueError(f"{path}: must say status RETIRED for project {project}")
    return record
