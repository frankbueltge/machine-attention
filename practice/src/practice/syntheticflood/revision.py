"""Register A, revision: how one cohort's counts move between two readings.

    python -m practice.syntheticflood.revision --repo-root . --cohort 2026-09 \
        --earlier 2026-10-19 --later 2026-10-22

writes syntheticflood/revisions/<cohort>/<earlier>_<later>.json from two
committed readings of the same cohort, under rule revision-v1. Committed
2026-10-24 (docs/2026-10-24-synthetic-flood-v0-inkrement-3d.md), before the
M+2 reading of 2026-09 exists: the first derived list of 2026-09 is
`control_breach` (`reduced`, ratio 1.827), and one possible cause named there
is the M+1 mix of the cohort. This rule is how the second reading will be
compared with the first. It fetches nothing; a changed rule is a new RULE id.

Per (list, word) present in both readings:
  thin   the earlier count is below MIN_COUNT; reported, not judged
  drift  (later / later total) / (earlier / earlier total), four places
  moved  drift outside [1 / BAND, BAND]

The file describes counts and their revision, not texts, and not a cause.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .. import autonomy
from ..preserve import sha256, write_json
from . import baseline, cohort

SCHEMA = "syntheticflood-revision-v1"
RULE = "revision-v1"
MIN_COUNT = 50
BAND = 1.1


def compare(earlier: dict, later: dict) -> dict:
    """Pure: the revision between two complete readings of one cohort."""
    t1, t2 = earlier["total"]["count"], later["total"]["count"]
    after = {(c["list"], c["word"]): c["count"] for c in later["counts"]}
    rows = []
    for c in earlier["counts"]:
        key = (c["list"], c["word"])
        if key not in after:
            continue
        row = {"list": key[0], "word": key[1], "earlier": c["count"], "later": after[key]}
        if c["count"] < MIN_COUNT:
            row["status"] = "thin"
        else:
            drift = round((after[key] / t2) / (c["count"] / t1), 4)
            row.update(status="moved" if not 1 / BAND <= drift <= BAND else "held",
                       drift=drift)
        rows.append(row)
    return {
        "rule": {"id": RULE, "min_count": MIN_COUNT, "band": BAND},
        "total": {"earlier": t1, "later": t2, "growth": round(t2 / t1, 4)},
        "moved": [r["word"] for r in rows if r["status"] == "moved"],
        "words": rows,
    }


def build(repo_root: Path, cohort_id: str, earlier_on: str, later_on: str) -> dict:
    if cohort_id in baseline.YEARS:
        raise ValueError(f"{cohort_id} is a baseline year, not a cohort to revise")
    if not earlier_on < later_on:
        raise ValueError("the earlier reading must be read before the later one")
    paths = [cohort.reading_path(repo_root, cohort_id, d) for d in (earlier_on, later_on)]
    readings = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
    for p, r in zip(paths, readings):
        if r["cohort"] != cohort_id or r["total"]["count"] is None \
                or any(c["count"] is None for c in r["counts"]):
            raise ValueError(f"{p.name}: reading incomplete or of another cohort")
    return {
        "schema": SCHEMA,
        "cohort": cohort_id,
        "earlier": {"file": paths[0].relative_to(repo_root).as_posix(),
                    "sha256": sha256(paths[0].read_bytes()),
                    "lag_months": readings[0]["lag_months"],
                    "wordlist": readings[0]["wordlist"]["version"]},
        "later": {"file": paths[1].relative_to(repo_root).as_posix(),
                  "sha256": sha256(paths[1].read_bytes()),
                  "lag_months": readings[1]["lag_months"],
                  "wordlist": readings[1]["wordlist"]["version"]},
        **compare(*readings),
    }


def revision_path(repo_root: Path, cohort_id: str, earlier_on: str, later_on: str) -> Path:
    return repo_root / "syntheticflood" / "revisions" / cohort_id / f"{earlier_on}_{later_on}.json"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--cohort", required=True)
    p.add_argument("--earlier", required=True, help="read date of the earlier reading")
    p.add_argument("--later", required=True, help="read date of the later reading")
    args = p.parse_args(argv)
    root = args.repo_root.resolve()
    result = build(root, args.cohort, args.earlier, args.later)
    write_json(revision_path(root, args.cohort, args.earlier, args.later), result)
    autonomy.append(root, "syntheticflood-revision", "machine", detail={
        "cohort": args.cohort, "earlier": args.earlier, "later": args.later,
        "rule": RULE, "total_growth": result["total"]["growth"],
        "moved": len(result["moved"])})
    print(json.dumps({"total": result["total"], "moved": result["moved"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
