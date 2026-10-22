"""Register A, the derived list of one cohort reading, as a file.

    python -m practice.syntheticflood.derived --repo-root . --cohort 2026-09 \
        --date 2026-10-22 --wordlist wordlist-v2

writes syntheticflood/derived/<cohort>/<read date>.json from the committed
cohort reading and the committed baseline of the same word list, under rule
excess-v1 (excess.py). It fetches nothing. The file names both inputs with
their SHA-256, so verify.py re-derives every ratio from them; a reading that
is not complete, or is on another word list than the baseline, is refused.
The list describes words, not texts, and not how much was machine-written.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .. import autonomy
from ..preserve import sha256, write_json
from . import baseline, cohort, excess

SCHEMA = "syntheticflood-derived-v1"


def build(repo_root: Path, cohort_id: str, read_on: str, version: str) -> dict:
    if cohort_id in baseline.YEARS:
        raise ValueError(f"{cohort_id} is a baseline year, not a cohort to measure")
    rpath = cohort.reading_path(repo_root, cohort_id, read_on)
    bpath = baseline.baseline_path(repo_root, version)
    reading = json.loads(rpath.read_text(encoding="utf-8"))
    base = json.loads(bpath.read_text(encoding="utf-8"))
    if reading["wordlist"] != base["wordlist"]:
        raise ValueError(f"{rpath.name}: reading and baseline are on different word lists")
    rows = [reading["total"], *reading["counts"]]
    if any(r["count"] is None for r in rows):
        raise ValueError(f"{rpath.name}: reading incomplete")
    if [(c["list"], c["word"]) for c in reading["counts"]] != \
            [(w["list"], w["word"]) for w in base["words"]]:
        raise ValueError(f"{rpath.name}: words differ from the baseline")
    counts = {c["word"]: c["count"] for c in reading["counts"]}
    result = excess.derive(base, counts, reading["total"]["count"], cohort_id)
    return {
        "schema": SCHEMA,
        "date": read_on,
        "cohort": cohort_id,
        "lag_months": reading["lag_months"],
        "value": reading["value"],
        "wordlist": base["wordlist"],
        "reading": {"file": rpath.relative_to(repo_root).as_posix(),
                    "sha256": sha256(rpath.read_bytes())},
        "baseline": {"file": bpath.relative_to(repo_root).as_posix(),
                     "sha256": sha256(bpath.read_bytes())},
        "total": reading["total"]["count"],
        **result,
    }


def derived_path(repo_root: Path, cohort_id: str, read_on: str) -> Path:
    return repo_root / "syntheticflood" / "derived" / cohort_id / f"{read_on}.json"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--cohort", required=True)
    p.add_argument("--date", required=True, help="read date of the cohort reading")
    p.add_argument("--wordlist", default="wordlist-v2")
    args = p.parse_args(argv)
    root = args.repo_root.resolve()
    out = derived_path(root, args.cohort, args.date)
    result = build(root, args.cohort, args.date, args.wordlist)
    write_json(out, result)
    autonomy.append(root, "syntheticflood-derived", "machine", detail={
        "cohort": args.cohort, "date": args.date, "rule": excess.RULE,
        "control_breach": result["control_breach"], "derived": len(result["derived"])})
    print(json.dumps({"control_breach": result["control_breach"],
                      "derived": result["derived"]}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
