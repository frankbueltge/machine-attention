"""Register A reader: one PubMed cohort, every committed word, counts only.

    python -m practice.syntheticflood.cohort --repo-root . --cohort 2026-09

writes syntheticflood/readings/<cohort>/<read date>.json. A cohort is read at
M+1, M+2 and M+3 (exposé §3); only M+3 counts as its value, and a reading
further out is marked retrospective. Nothing here stores a text, a title or
a name: the query is the repeat instruction, the count is the observation,
the SHA-256 binds it to the bytes that arrived.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .. import autonomy
from ..fetch import Client, SourceUnavailable, USER_AGENT
from ..preserve import Snapshot, sha256, utc_now, write_json
from . import pubmed, wordlist

SCHEMA = "syntheticflood-cohort-v1"
SNAP_BASE = "syntheticflood/snapshots"
VALUE_LAG = 3


def lag(cohort: str, read_on: str) -> int:
    cy, cm = (int(x) for x in cohort.split("-"))
    ry, rm = (int(x) for x in read_on[:7].split("-"))
    return (ry - cy) * 12 + (rm - cm)


def _count(client: Client, term: str, snap: Snapshot, name: str) -> dict:
    url = pubmed.count_url(term)
    row = {"term": term, "url": url}
    try:
        data, status = client.fetch(url)
    except SourceUnavailable as e:
        row.update(status=None, error=e.detail, count=None)
        return row
    row.update(status=status, bytes=len(data), sha256=sha256(data))
    count = None
    if status == 200:
        try:
            count = pubmed.parse_count(data)
        except (ValueError, KeyError, TypeError):
            pass
    row["count"] = count
    if count is None or data != pubmed.canonical(count):
        # Not the known shape: keep the bytes so the claim stays checkable.
        row["file"] = snap.preserve(f"{name}.json", data, url, status)["file"]
    return row


def read(repo_root: Path, cohort: str, read_on: str, version: str,
         client: Client | None = None) -> dict:
    n = lag(cohort, read_on)
    if n < 1:
        raise ValueError(f"cohort {cohort} is not complete on {read_on}")
    doc, wl_file, wl_sha = wordlist.load(repo_root, version)
    client = client or Client()
    snap = Snapshot(repo_root, f"{read_on}-{cohort}", base=SNAP_BASE)
    started = utc_now()
    total = _count(client, pubmed.cohort_term(cohort), snap, "cohort")
    counts = []
    for name, word in wordlist.terms(doc):
        row = _count(client, pubmed.cohort_term(cohort, word), snap, f"{name}-{word}")
        counts.append({"list": name, "word": word, **row})
    if snap.entries:
        snap.write_manifest()
    return {
        "schema": SCHEMA,
        "date": read_on,
        "cohort": cohort,
        "lag_months": n,
        "value": n == VALUE_LAG,
        "retrospective": n > VALUE_LAG,
        "source": pubmed.HOST,
        "user_agent": USER_AGENT,
        "wordlist": {"file": wl_file, "version": version, "sha256": wl_sha},
        "started_at": started,
        "finished_at": utc_now(),
        "requests": client.requests,
        "http_429": client.http_429,
        "total": total,
        "counts": counts,
    }


def reading_path(repo_root: Path, cohort: str, read_on: str) -> Path:
    return repo_root / "syntheticflood" / "readings" / cohort / f"{read_on}.json"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--cohort", required=True, help="YYYY-MM")
    p.add_argument("--date", default=date.today().isoformat())
    p.add_argument("--wordlist", default="wordlist-v1")
    args = p.parse_args(argv)
    root = args.repo_root.resolve()
    out = reading_path(root, args.cohort, args.date)
    if out.exists():
        print(f"{out.relative_to(root)} exists; a reading is never rewritten")
        return 1
    reading = read(root, args.cohort, args.date, args.wordlist)
    write_json(out, reading)
    missing = sum(1 for r in [reading["total"], *reading["counts"]] if r["count"] is None)
    autonomy.append(root, "syntheticflood-cohort-reading", "machine", detail={
        "date": args.date, "cohort": args.cohort, "lag_months": reading["lag_months"],
        "requests": reading["requests"], "http_429": reading["http_429"],
        "terms": len(reading["counts"]), "missing": missing})
    print(f"{out.relative_to(root)}: {len(reading['counts'])} terms, "
          f"{missing} missing, {reading['http_429']} x 429")
    return 0 if missing == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
