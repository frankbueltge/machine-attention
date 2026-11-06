"""Register A, the check reading of rule control-check-v1, and its record.

    python -m practice.syntheticflood.controlread --repo-root . --date 2026-11-06

reads, counts only, the year cohorts the rule needs and writes
syntheticflood/controlcheck/<date>.json; if the composition holds at least
MIN_CONTROLS words it also writes the next word list (`--next wordlist-v3`),
whose fixed and pool lists are carried over word for word. The rule itself
(practice.syntheticflood.controlcheck) was committed on 2026-11-05, before
any of these counts existed (docs/2026-11-05-synthetic-flood-kontrollpruefung.md).

What is read:
  totals      `hasabstract AND YYYY[dp]` for 2018–2025 (8)
  controls    every control of the current list except the struck word,
              in 2023, 2024, 2025 (their baseline is the committed one)
  candidates  every candidate in 2018–2025: 2018–2022 give it a baseline-v1
              entry from tonight's own counts and totals, 2023–2025 check it
Each row keeps the query, the count and the SHA-256 of what arrived; an
answer that is not the canonical count document is preserved as bytes.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from .. import autonomy
from ..fetch import Client, USER_AGENT
from ..preserve import Snapshot, sha256, utc_now, write_json
from . import baseline, controlcheck, pubmed, wordlist
from .cohort import SNAP_BASE, _count

SCHEMA = "syntheticflood-controlcheck-v1"
ALL_YEARS = baseline.YEARS + controlcheck.CHECK_YEARS


def plan(controls: list[str]) -> list[tuple[str, str | None]]:
    """(year, word or None for the total) in reading order."""
    rows: list[tuple[str, str | None]] = [(y, None) for y in ALL_YEARS]
    for w in controls:
        if w not in controlcheck.STRUCK:
            rows += [(y, w) for y in controlcheck.CHECK_YEARS]
    for w in controlcheck.CANDIDATES:
        rows += [(y, w) for y in ALL_YEARS]
    return rows


def evaluate(base: dict, controls: list[str], counts: dict) -> dict:
    """Checks and composition from committed inputs; fetches nothing.

    `base` is the committed baseline of the current list, `counts` maps
    year -> {None: cohort total, word: n, ...} as read tonight (a value None
    where unread). The total sits under the key None, never under a string:
    `total` is itself a candidate word."""
    totals = {y: counts[y].get(None) for y in ALL_YEARS}
    entries = {w["word"]: w for w in base["words"] if w["list"] == "controls"}
    results = {}
    for w in controls:
        if w in controlcheck.STRUCK:
            continue
        results[w] = controlcheck.check(
            entries[w], {y: counts[y].get(w) for y in controlcheck.CHECK_YEARS}, totals)
    candidates = {}
    for w in controlcheck.CANDIDATES:
        bc = {y: counts[y].get(w) for y in baseline.YEARS}
        if any(bc[y] is None or not totals[y] for y in baseline.YEARS):
            entry = {"word": w, "verdict": "unread", "shares": {}}
        else:
            entry = {"word": w, **baseline.verdict(bc, {y: totals[y] for y in baseline.YEARS})}
        candidates[w] = entry
        results[w] = controlcheck.check(
            entry, {y: counts[y].get(w) for y in controlcheck.CHECK_YEARS}, totals)
    return {"candidate_baseline": candidates, "results": results,
            "composition": controlcheck.compose(controls, results)}


def counts_from_rows(rows: list[dict]) -> dict:
    counts: dict = {y: {} for y in ALL_YEARS}
    for row in rows:
        counts[row["year"]][row["word"]] = row["count"]
    return counts


def read(repo_root: Path, read_on: str, version: str, client: Client | None = None) -> dict:
    doc, wl_file, wl_sha = wordlist.load(repo_root, version)
    bpath = baseline.baseline_path(repo_root, version)
    base = json.loads(bpath.read_text(encoding="utf-8"))
    if base["wordlist"]["sha256"] != wl_sha:
        raise ValueError(f"{bpath.name} is not the baseline of {wl_file}")
    client = client or Client()
    snap = Snapshot(repo_root, f"{read_on}-controlcheck", base=SNAP_BASE)
    started = utc_now()
    rows = []
    for year, word in plan(doc["controls"]):
        name = f"{year}-{word or 'cohort'}"
        row = _count(client, pubmed.cohort_term(year, word), snap, name)
        rows.append({"year": year, "word": word, **row})
    if snap.entries:
        snap.write_manifest()
    return {
        "schema": SCHEMA,
        "date": read_on,
        "source": pubmed.HOST,
        "user_agent": USER_AGENT,
        "rule": controlcheck.RULE,
        "wordlist": {"file": wl_file, "version": version, "sha256": wl_sha},
        "baseline": {"file": bpath.relative_to(repo_root).as_posix(),
                     "sha256": sha256(bpath.read_bytes())},
        "started_at": started,
        "finished_at": utc_now(),
        "requests": client.requests,
        "http_429": client.http_429,
        "rows": rows,
        **evaluate(base, doc["controls"], counts_from_rows(rows)),
    }


def next_list(repo_root: Path, record: dict, record_path: Path, version: str,
              new_version: str, committed: str) -> dict | None:
    controls = record["composition"]["controls"]
    if controls is None:
        return None
    doc, _, _ = wordlist.load(repo_root, version)
    comp = record["composition"]
    return {
        "schema": doc["schema"],
        "version": new_version,
        "committed": committed,
        "note": (f"Successor of {version}, which stays unchanged. Controls composed by rule "
                 f"{controlcheck.RULE} from {record_path.relative_to(repo_root).as_posix()} "
                 f"(struck {comp['struck']}, dropped {comp['dropped']}, added {comp['added']}); "
                 "'fixed' and 'pool' are carried over word for word. A changed list is a new "
                 "version file; this file never changes."),
        "fixed": list(doc["fixed"]),
        "controls": list(controls),
        "pool": list(doc["pool"]),
    }


def record_path(repo_root: Path, read_on: str) -> Path:
    return repo_root / "syntheticflood" / "controlcheck" / f"{read_on}.json"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--wordlist", default="wordlist-v2")
    p.add_argument("--next", default="wordlist-v3")
    args = p.parse_args(argv)
    root = args.repo_root.resolve()
    out = record_path(root, args.date)
    if out.exists():
        print(f"{out.relative_to(root)} exists; a reading is never rewritten")
        return 1
    rec = read(root, args.date, args.wordlist)
    write_json(out, rec)
    missing = sum(1 for r in rec["rows"] if r["count"] is None)
    comp = rec["composition"]
    nxt = None if missing else next_list(root, rec, out, args.wordlist, args.next, args.date)
    if nxt is not None:
        wpath = wordlist.path_for(root, args.next)
        if wpath.exists():
            raise SystemExit(f"{wpath.name} exists; a word list never changes")
        write_json(wpath, nxt)
    autonomy.append(root, "syntheticflood-controlcheck", "machine", detail={
        "date": args.date, "rule": controlcheck.RULE, "requests": rec["requests"],
        "http_429": rec["http_429"], "rows": len(rec["rows"]), "missing": missing,
        "kept": len(comp["kept"]), "dropped": comp["dropped"], "added": comp["added"],
        "next_list": args.next if nxt is not None else None})
    print(json.dumps({"requests": rec["requests"], "http_429": rec["http_429"],
                      "missing": missing, **comp}, indent=1))
    return 0 if missing == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
