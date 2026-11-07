"""Register A baseline of a successor word list, carried from committed counts.

    python -m practice.syntheticflood.carry --repo-root . \
        --wordlist wordlist-v3 --predecessor wordlist-v2 \
        --controlcheck syntheticflood/controlcheck/2026-11-06.json

writes syntheticflood/baseline/<wordlist>.json and fetches nothing. Rule
`baseline-carry-v1` was committed before any request on the successor list
(docs/2026-11-07-synthetic-flood-basislinie-v3.md):

  carried  a word on the predecessor list keeps its committed baseline entry
           (counts 2018–2022 and the totals of those same readings) unchanged;
  added    a word new to the successor list takes its counts 2018–2022 from
           the control-check record that composed the list, with that
           record's own year totals.

Every entry's share is still count_y / total_y of one and the same reading,
and its verdict is re-derived by baseline-v1 (`baseline.verdict`). A word
found in neither source refuses the whole baseline: nothing is read to fill
a gap. A changed rule is a new RULE id, never an edit of this one.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .. import autonomy
from ..preserve import sha256, write_json
from . import baseline, wordlist

RULE = "baseline-carry-v1"


def _record_totals_and_counts(record: dict) -> tuple[dict, dict]:
    totals: dict[str, int] = {}
    counts: dict[str, dict[str, int]] = {}
    for row in record["rows"]:
        if row["year"] not in baseline.YEARS or row["count"] is None:
            continue
        if row["word"] is None:
            totals[row["year"]] = row["count"]
        else:
            counts.setdefault(row["word"], {})[row["year"]] = row["count"]
    return totals, counts


def derive(repo_root: Path, version: str, predecessor: str, check_rel: str) -> dict:
    doc, wl_file, wl_sha = wordlist.load(repo_root, version)
    _, pre_file, pre_sha = wordlist.load(repo_root, predecessor)
    ppath = baseline.baseline_path(repo_root, predecessor)
    pre = json.loads(ppath.read_text(encoding="utf-8"))
    if pre["wordlist"]["sha256"] != pre_sha or pre["rule"]["id"] != baseline.RULE:
        raise ValueError(f"{ppath.name} is not a {baseline.RULE} baseline of {pre_file}")
    cpath = repo_root / check_rel
    record = json.loads(cpath.read_text(encoding="utf-8"))
    if record["wordlist"]["sha256"] != pre_sha:
        raise ValueError(f"{cpath.name} did not check {pre_file}")
    if record["composition"]["controls"] != doc["controls"]:
        raise ValueError(f"{cpath.name} did not compose {wl_file}")
    totals_added, counts_added = _record_totals_and_counts(record)
    if sorted(totals_added) != list(baseline.YEARS):
        raise ValueError(f"{cpath.name}: a baseline year total is missing")
    by_word = {w["word"]: w for w in pre["words"]}
    words = []
    for name, word in wordlist.terms(doc):
        if word in by_word:
            old = by_word[word]
            counts, totals, source = old["counts"], pre["totals"], "carried"
        elif sorted(counts_added.get(word, {})) == list(baseline.YEARS):
            counts, totals, source = counts_added[word], totals_added, "added"
        else:
            raise ValueError(f"{word}: in neither the predecessor baseline nor {cpath.name}")
        counts = {y: counts[y] for y in baseline.YEARS}
        words.append({"list": name, "word": word, "source": source, "counts": counts,
                      **baseline.verdict(counts, totals)})
    tally: dict[str, dict[str, int]] = {}
    for w in words:
        tally.setdefault(w["list"], {}).setdefault(w["verdict"], 0)
        tally[w["list"]][w["verdict"]] += 1
    return {
        "schema": baseline.SCHEMA,
        "rule": {"id": RULE, "years": list(baseline.YEARS),
                 "min_count": baseline.MIN_COUNT, "max_ratio": baseline.MAX_RATIO},
        "wordlist": {"file": wl_file, "version": version, "sha256": wl_sha},
        "sources": {
            "carried": {"file": ppath.relative_to(repo_root).as_posix(),
                        "sha256": sha256(ppath.read_bytes()), "totals": pre["totals"]},
            "added": {"file": cpath.relative_to(repo_root).as_posix(),
                      "sha256": sha256(cpath.read_bytes()), "totals": totals_added},
        },
        "tally": {k: dict(sorted(v.items())) for k, v in sorted(tally.items())},
        "words": words,
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--wordlist", required=True)
    p.add_argument("--predecessor", required=True)
    p.add_argument("--controlcheck", required=True, help="repo-relative record path")
    args = p.parse_args(argv)
    root = args.repo_root.resolve()
    out = baseline.baseline_path(root, args.wordlist)
    if out.exists():
        raise SystemExit(f"{out.name} exists; a baseline is never rewritten")
    result = derive(root, args.wordlist, args.predecessor, args.controlcheck)
    write_json(out, result)
    autonomy.append(root, "syntheticflood-baseline", "machine", detail={
        "wordlist": args.wordlist, "rule": RULE, "tally": result["tally"],
        "added": [w["word"] for w in result["words"] if w["source"] == "added"]})
    print(json.dumps(result["tally"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
