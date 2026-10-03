"""Registry stall check (foreknown/proposals/sensor-registry-stall.json,
promoted 2026-09-07).

Cause-agnostic and deliberately independent of the four nightly workflows
(sentinel, darkocean, memoryhole, anchor) it watches: it never writes a
register itself, only reads what checkout already put on disk, so whatever
silently stalled the register under watch cannot also silently stall this
check. Four distinct causes have shared the identical outward symptom since
2026-08-11 -- a register silently more than a day behind, no
autonomy/log.jsonl trace, no source-outage record -- because in each case
the job never reached the point of writing one: an anchor/verify-step
deadlock (obs-2026-08-11-1), a git push race (obs-2026-08-16-2), a
resolution-status logic contradiction in verify.py (obs-2026-08-27's
review), and practice.export.figures() crashing on a continuity probe's
first real catch (obs-2026-09-06-1). None of the per-source checks already
in run.json (GDACS/NHC/FTS failures, the DMA outage, the reaction axis's
retries) can see this, because they all presuppose the job reached the
point of writing its output.

Run early, ahead of the day's own nightly jobs (registry-stall.yml
schedules this before memoryhole/darkocean/sentinel): at that point the
newest committed data is necessarily last night's, so a healthy register
reads 0 or 1 days behind "yesterday" -- 0 for foreknown/snapshots and
foreknown/reaction/snapshots, which label a night by the day the job runs;
1 for darkocean/snapshots and memoryhole/readings, which label a night by
the day the data is about (both workflows commit with `date -u -d
'yesterday'`). THRESHOLD_DAYS is set from the committed record: two of the
four known causes were actually observed persisting unrepaired long enough
to measure (2026-08-11's deadlock: three nights before the 2026-08-12
handshake fix; 2026-09-04/05's export bug: two nights before the
2026-09-06 discovery pass traced and fixed it), and zero were observed
self-correcting without an active repair landing mid-gap. A register more
than one day behind yesterday has, on the evidence so far, stalled -- not
merely slipped a beat.

Retired registers (2026-10-04). The sensor's own falsification clause
foresaw the case: a register allowed to stop by design needs an explicit
exception "rather than firing on every gap". The Foreknown was retired on the
maintainer's decision of 2026-10-04 (foreknown/RETIRED.json); its two
registers end on their last night by design. They are still listed under
"checked", and reported under "retired" with that last night — never as
stale, and never silently dropped from the output.
"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from .autonomy import append as autonomy_append
from .foreknown.retired import read_retired

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# (register label, path relative to repo root, "dir" -> newest dated
# subdirectory name is the register's date; "file" -> newest <date>.json
# filename stem is)
REGISTERS = (
    ("foreknown/snapshots", "foreknown/snapshots", "dir"),
    ("foreknown/reaction/snapshots", "foreknown/reaction/snapshots", "dir"),
    ("darkocean/snapshots", "darkocean/snapshots", "dir"),
    ("memoryhole/readings", "memoryhole/readings", "file"),
)

# See module docstring: set from the two of four known causes actually
# observed persisting (2, 3 nights) versus zero observed self-correcting.
THRESHOLD_DAYS = 1


def _newest_date(base: Path, kind: str) -> str | None:
    if not base.is_dir():
        return None
    if kind == "dir":
        names = [p.name for p in base.iterdir()
                 if p.is_dir() and DATE_RE.match(p.name)]
    else:
        names = [p.stem for p in base.glob("*.json") if DATE_RE.match(p.stem)]
    return max(names) if names else None


def check(repo_root: Path, *, today: date | None = None) -> dict:
    """Compare each register's newest committed dated unit against
    "yesterday" (UTC). Returns {"checked": [labels], "stale": [entries],
    "retired": [entries]} (a retired register is reported, not judged),
    where a stale entry is {"register", "newest_committed_date",
    "days_behind"} -- days_behind is None when the register has no dated
    unit at all yet."""
    today = today or datetime.now(timezone.utc).date()
    yesterday = today - timedelta(days=1)
    closing = read_retired(repo_root)
    checked: list[str] = []
    stale: list[dict] = []
    retired: list[dict] = []
    for label, rel, kind in REGISTERS:
        newest = _newest_date(repo_root / rel, kind)
        checked.append(label)
        if closing and label.startswith("foreknown/"):
            retired.append({"register": label, "newest_committed_date": newest,
                            "last_night": closing["last_night"]})
            continue
        days_behind = (None if newest is None
                       else (yesterday - date.fromisoformat(newest)).days)
        if newest is None or days_behind > THRESHOLD_DAYS:
            stale.append({"register": label, "newest_committed_date": newest,
                          "days_behind": days_behind})
    return {"checked": checked, "stale": stale, "retired": retired}


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Check whether any register has silently stalled.")
    parser.add_argument("--repo-root", default=".", type=Path)
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    result = check(root)
    autonomy_append(root, "registry-stall-check", "machine", detail=result)
    if result["retired"]:
        print("RETIRED (by design, not stale):",
              [r["register"] for r in result["retired"]])
    if result["stale"]:
        print("STALE:", result["stale"])
    else:
        print("all running registers current as of yesterday (UTC)")


if __name__ == "__main__":
    main()
