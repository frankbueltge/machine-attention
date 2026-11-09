"""Register A, increment 4: the monthly run of the workflow.

    python -m practice.syntheticflood.monthly --repo-root .

On a read date D it reads every cohort that is due -- each month cohort from
FIRST_COHORT on, once at M+1, M+2 and M+3 (exposé §3, cohort.VALUE_LAG) --
on the current word list, then writes, from the committed files only:

  the derived list under excess-v1 (derived.py), when the reading is complete;
  the revision against the cohort's latest earlier reading on the same word
  list (revision.py), when one exists and both are complete.

Due means: the month cohort D - L for L in LAGS, not before FIRST_COHORT, with
no committed reading at lag L on the current word list. A reading with missing
counts still counts as read: the cohort is not asked again at that lag, so a
re-run of the workflow on the same month never repeats a request (the host's
robots.txt is `Disallow: /`; the self-decision of 2026-11-02 and REQUESTS.md
2026-10-30 bound this to as few requests as the cadence needs). Year cohorts
(the baseline) are never read here.

Committed 2026-11-09 (docs/2026-11-09-synthetic-flood-v0-inkrement-4.md),
after the first derivation without a control breach (2026-11-08). It decides
nothing about the values: M+3 is the value, M+1 and M+2 are revisions.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from .. import autonomy
from ..preserve import write_json
from . import cohort, derived, revision

WORDLIST = "wordlist-v3"
FIRST_COHORT = "2026-09"
LAGS = (1, 2, 3)


def month_minus(read_on: str, n: int) -> str:
    y, m = int(read_on[:4]), int(read_on[5:7])
    k = y * 12 + (m - 1) - n
    return f"{k // 12:04d}-{k % 12 + 1:02d}"


def _readings(repo_root: Path, cohort_id: str) -> list[tuple[str, dict]]:
    folder = repo_root / "syntheticflood" / "readings" / cohort_id
    return [(p.stem, json.loads(p.read_text(encoding="utf-8")))
            for p in sorted(folder.glob("*.json"))]


def complete(reading: dict) -> bool:
    return all(r["count"] is not None for r in [reading["total"], *reading["counts"]])


def due(repo_root: Path, read_on: str, version: str = WORDLIST) -> list[str]:
    """Pure over the committed tree: the cohorts to read on read_on, oldest
    first."""
    out = []
    for n in sorted(LAGS, reverse=True):
        c = month_minus(read_on, n)
        if c < FIRST_COHORT:
            continue
        if cohort.reading_path(repo_root, c, read_on).exists():
            continue
        if any(r["lag_months"] == n and r["wordlist"]["version"] == version
               for _, r in _readings(repo_root, c)):
            continue
        out.append(c)
    return out


def earlier_on_same_list(repo_root: Path, cohort_id: str, read_on: str,
                         version: str = WORDLIST) -> str | None:
    dates = [d for d, r in _readings(repo_root, cohort_id)
             if d < read_on and r["wordlist"]["version"] == version and complete(r)]
    return dates[-1] if dates else None


def run(repo_root: Path, read_on: str, version: str = WORDLIST,
        client=None) -> list[dict]:
    done = []
    for c in due(repo_root, read_on, version):
        reading = cohort.read(repo_root, c, read_on, version, client=client)
        rpath = cohort.reading_path(repo_root, c, read_on)
        write_json(rpath, reading)
        row = {"cohort": c, "lag_months": reading["lag_months"],
               "requests": reading["requests"], "http_429": reading["http_429"],
               "missing": sum(1 for r in [reading["total"], *reading["counts"]]
                              if r["count"] is None),
               "files": [rpath.relative_to(repo_root).as_posix()]}
        if complete(reading):
            d = derived.build(repo_root, c, read_on, version)
            dpath = derived.derived_path(repo_root, c, read_on)
            write_json(dpath, d)
            row["control_breach"] = d["control_breach"]
            row["files"].append(dpath.relative_to(repo_root).as_posix())
            prev = earlier_on_same_list(repo_root, c, read_on, version)
            if prev:
                rev = revision.build(repo_root, c, prev, read_on)
                vpath = revision.revision_path(repo_root, c, prev, read_on)
                write_json(vpath, rev)
                row["moved"] = rev["moved"]
                row["files"].append(vpath.relative_to(repo_root).as_posix())
        done.append(row)
    return done


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--wordlist", default=WORDLIST)
    args = p.parse_args(argv)
    root = args.repo_root.resolve()
    done = run(root, args.date, args.wordlist)
    autonomy.append(root, "syntheticflood-monthly", "machine", detail={
        "date": args.date, "wordlist": args.wordlist, "rule": "excess-v1",
        "cohorts": done})
    print(json.dumps(done, indent=1))
    # A run with nothing due, or with missing counts, still lands: the record
    # of what was asked is the record.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
