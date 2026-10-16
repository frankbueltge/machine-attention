"""Planetary Listening V0 increment 3: the daily workflow. It runs the same
command that made the committed readings, after the publisher has finished the
read day, and lands through the shared handshake. No network."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "planetary.yml"


def test_workflow_runs_the_nightly_reading_and_the_handshake():
    text = WORKFLOW.read_text(encoding="utf-8")
    steps = ["pip install --quiet -e ./practice",
             "python -m practice.planetary.nightly --repo-root .",
             "python tools/anchor.py --register",
             "python verify.py --repo-root .",
             "tools/commit-and-push.sh"]
    positions = [text.index(s) for s in steps]
    assert positions == sorted(positions), "install, read, register, verify, commit"


def test_schedule_follows_every_observed_publisher_update():
    """The slot must lie after the publisher's `Updated` for the read day in
    every committed reading, or the job would read a day still being written."""
    text = WORKFLOW.read_text(encoding="utf-8")
    minute, hour = re.search(r'cron: "(\d+) (\d+) \* \* \*"', text).groups()
    slot = int(hour) * 60 + int(minute)
    readings = sorted((ROOT / "planetary" / "readings").glob("*.json"))
    assert readings, "the workflow is admitted only after a committed reading"
    for path in readings:
        reading = json.loads(path.read_text(encoding="utf-8"))
        for row in reading["publisher"]["availability"]["rows"] or []:
            updated = row["Updated"]
            assert updated[:10] == reading["date"], "updated on the reading's date"
            hh, mm = int(updated[11:13]), int(updated[14:16])
            assert hh * 60 + mm + 30 <= slot, \
                f"{path.name}: publisher updated {updated}, slot too close"
