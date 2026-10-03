"""The Foreknown's closing record — one file, read by every part that would
otherwise go on describing a running notary.

Retired on the maintainer's decision of 2026-10-04 (wording private; reasoning
in docs/2026-10-04-foreknown-retired.md). The admission path pre-committed the
word for this end (docs/2026-08-08-projekt-aufnahme.md: "jederzeit: RETIRED" —
honestly ended, records kept, reason committed). Nothing is deleted: the
registry, snapshots, resolutions and anchors stay as they were on the last
night, and verify.py keeps holding them.

Who reads it: the export (status word, no "under watch" figures), the moments
(one closing moment), the staleness check (a retired register is not stale),
verify.py (no night may be recorded after the last one) and the stage.
"""

from __future__ import annotations

from pathlib import Path

from ..preserve import read_json

RETIRED_FILE = Path("foreknown") / "RETIRED.json"
REQUIRED = ("project", "status", "last_night", "decided", "record", "reason")


def read_retired(repo_root: Path) -> dict | None:
    """The closing record, or None while the project runs."""
    record = read_json(repo_root / RETIRED_FILE, None)
    if not record:
        return None
    missing = [key for key in REQUIRED if not record.get(key)]
    if missing:
        raise ValueError(f"{RETIRED_FILE}: missing {', '.join(missing)}")
    if record["status"] != "RETIRED":
        raise ValueError(f"{RETIRED_FILE}: status must be RETIRED")
    return record
