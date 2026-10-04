"""The Foreknown's closing record (2026-10-04) — the general rule lives in
practice/src/practice/retired.py; this module names The Foreknown's file for
the parts that only ever concern it (the stage's moments)."""

from __future__ import annotations

from pathlib import Path

from .. import retired as _retired

RETIRED_FILE = _retired.retired_file("foreknown")


def read_retired(repo_root: Path) -> dict | None:
    return _retired.read_retired(repo_root, "foreknown")
