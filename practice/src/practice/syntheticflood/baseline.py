"""Register A baseline: the stability test of every word against 2018–2022.

    python -m practice.syntheticflood.baseline --repo-root . --wordlist wordlist-v1

derives syntheticflood/baseline/<wordlist>.json from the committed year
readings (syntheticflood/readings/<YYYY>/<date>.json, the newest per year)
and fetches nothing. The rule was committed before the first baseline
request (docs/2026-10-21-synthetic-flood-v0-inkrement-3.md); a changed rule
is a new RULE id, never an edit of this one.

Per word: share_y = count_y / total_y for each baseline year.
  rare      some baseline year counts fewer than MIN_COUNT abstracts
  stable    max share / min share <= MAX_RATIO
  drifting  otherwise, with the direction from the first to the last year
The verdict describes the word's past, not machine writing; striking a word
is a later, versioned word list, never an edit here.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .. import autonomy
from ..preserve import sha256, write_json
from . import wordlist

SCHEMA = "syntheticflood-baseline-v1"
RULE = "baseline-v1"
YEARS = ("2018", "2019", "2020", "2021", "2022")
MIN_COUNT = 50
MAX_RATIO = 1.5


def newest_readings(repo_root: Path, version: str) -> dict[str, Path]:
    found = {}
    for year in YEARS:
        paths = []
        for p in sorted((repo_root / "syntheticflood/readings" / year).glob("*.json")):
            if json.loads(p.read_text(encoding="utf-8"))["wordlist"]["version"] == version:
                paths.append(p)
        if not paths:
            raise ValueError(f"no {version} reading of baseline year {year}")
        found[year] = paths[-1]
    return found


def verdict(counts: dict[str, int], totals: dict[str, int]) -> dict:
    shares = {y: round(counts[y] / totals[y], 9) for y in YEARS}
    low, high = min(shares.values()), max(shares.values())
    ratio = round(high / low, 4) if low > 0 else None
    if min(counts.values()) < MIN_COUNT:
        v = "rare"
    elif ratio <= MAX_RATIO:
        v = "stable"
    else:
        v = "rising" if shares[YEARS[-1]] > shares[YEARS[0]] else "falling"
        v = f"drifting-{v}"
    return {"shares": shares, "min_count": min(counts.values()), "ratio": ratio,
            "verdict": v}


def derive(repo_root: Path, version: str) -> dict:
    doc, wl_file, wl_sha = wordlist.load(repo_root, version)
    paths = newest_readings(repo_root, version)
    readings = {y: json.loads(p.read_text(encoding="utf-8")) for y, p in paths.items()}
    totals = {}
    for y, r in readings.items():
        rows = [r["total"], *r["counts"]]
        if r["wordlist"]["sha256"] != wl_sha or any(c["count"] is None for c in rows):
            raise ValueError(f"baseline year {y}: reading incomplete or on another list")
        totals[y] = r["total"]["count"]
    words = []
    for i, (name, word) in enumerate(wordlist.terms(doc)):
        counts = {y: readings[y]["counts"][i]["count"] for y in YEARS}
        words.append({"list": name, "word": word, "counts": counts,
                      **verdict(counts, totals)})
    tally: dict[str, dict[str, int]] = {}
    for w in words:
        tally.setdefault(w["list"], {}).setdefault(w["verdict"], 0)
        tally[w["list"]][w["verdict"]] += 1
    return {
        "schema": SCHEMA,
        "rule": {"id": RULE, "years": list(YEARS), "min_count": MIN_COUNT,
                 "max_ratio": MAX_RATIO},
        "wordlist": {"file": wl_file, "version": version, "sha256": wl_sha},
        "readings": {y: {"file": p.relative_to(repo_root).as_posix(),
                         "sha256": sha256(p.read_bytes())} for y, p in paths.items()},
        "totals": totals,
        "tally": {k: dict(sorted(v.items())) for k, v in sorted(tally.items())},
        "words": words,
    }


def baseline_path(repo_root: Path, version: str) -> Path:
    return repo_root / "syntheticflood" / "baseline" / f"{version}.json"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--wordlist", default="wordlist-v1")
    args = p.parse_args(argv)
    root = args.repo_root.resolve()
    out = baseline_path(root, args.wordlist)
    result = derive(root, args.wordlist)
    write_json(out, result)
    autonomy.append(root, "syntheticflood-baseline", "machine", detail={
        "wordlist": args.wordlist, "rule": RULE, "tally": result["tally"]})
    print(json.dumps(result["tally"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
