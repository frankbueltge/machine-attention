"""The Interval V0, increment 5: the weekly reading.

One run = one record, `interval/readings/<date>.json`, written beside the
snapshots it caused and the register it rebuilt. Candidate document:
docs/2026-10-04-kandidat-the-interval.md §6 increment 5; decisions in
docs/2026-10-13-the-interval-v0-inkrement-5.md.

- IPC: the national table is fetched and preserved only when its bytes
  differ from the newest committed copy (sources.snapshot_ipc).
- Episodes are read from the newest committed IPC table after that step.
- FTS, per episode and flow set: a query is **frozen** once a complete page
  set exists from a snapshot day whose month lies more than GRACE_MONTHS
  after the episode's last window month. A frozen query is read from that
  snapshot and not fetched again; late revisions at FTS are not followed
  (V0's stated limit). Every other query is fetched in full.
- A fetched page set whose page hashes equal the newest complete set's is
  `unchanged` and not preserved a second time. Anything else is preserved,
  an incomplete set too, so the failure stands in the record.
- The decision is a function of committed snapshot days *before* the
  reading's date; verify.py recomputes it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from .. import autonomy
from ..fetch import Client, SourceUnavailable
from ..preserve import Snapshot, sha256, write_json
from . import money, register, sources

SCHEMA = "interval-reading-v1"
READINGS = "interval/readings"
GRACE_MONTHS = 3


def frozen(basis_day: str | None, window_end: str) -> bool:
    return basis_day is not None and basis_day[:7] > money.add_months(
        window_end, GRACE_MONTHS)


def _manifest_shas(root: Path, files: list[str]) -> list[str]:
    day = files[0].split("/")[2]
    entries = register._manifest(root, day)
    return [entries[f]["sha256"] for f in files]


def _ipc_step(root: Path, day: str, client: Client) -> dict:
    try:
        out = sources.snapshot_ipc(root, day, client)
    except SourceUnavailable as e:
        return {"status": "unavailable", "detail": e.detail}
    return {"status": "preserved" if out["preserved"] else "unchanged"}


def _fts_step(root: Path, day: str, client: Client, iso3: str, tag: str,
              years: str, basis: tuple[str, list[str]] | None) -> dict:
    url = sources.fts_url(iso3, years, filter_by=register.SETS[tag])
    try:
        pages = sources.fts_pages(client, url)
    except SourceUnavailable as e:
        return {"outcome": "unavailable", "detail": e.detail}
    shas = [sha256(data) for _, data, _ in pages]
    complete = bool(pages) and pages[-1][2] == 200 and not (
        json.loads(pages[-1][1]).get("meta") or {}).get("nextLink")
    if complete and basis and shas == _manifest_shas(root, basis[1]):
        return {"outcome": "unchanged", "pages": len(pages),
                "pages_sha256": shas}
    snap = Snapshot(root, day, base=sources.BASE)
    stem = years.replace(",", "_")
    for i, (u, data, status) in enumerate(pages, 1):
        snap.preserve(f"fts/{iso3}/{tag}-{stem}-p{i:03d}.json", data, u, status)
    snap.write_manifest()
    return {"outcome": "preserved" if complete else "incomplete",
            "pages": len(pages), "pages_sha256": shas}


def run(root: Path, day: str, client: Client) -> dict:
    ipc_out = _ipc_step(root, day, client)
    ipc = register.newest_ipc(root)
    if ipc is None:
        raise FileNotFoundError("no committed IPC snapshot")
    _, onsets, _ = register.read_onsets((root / ipc).read_text(encoding="utf-8"))
    queries = []
    for country, t0 in sorted(onsets):
        end = money.window(t0)[1]
        years = money.boundary_years(t0)
        for tag in register.SETS:
            basis = register.newest_fts(root, country, tag, years, before=day)
            q = {"country": country, "t0": t0, "set": tag,
                 "boundary_years": years, "window_end": end,
                 "basis_day": basis[0] if basis else None}
            if frozen(q["basis_day"], end):
                q["decision"] = "frozen"
            else:
                q["decision"] = "fetch"
                q.update(_fts_step(root, day, client, country, tag, years,
                                   basis))
            queries.append(q)
    built = register.write(root)
    reading = {
        "schema": SCHEMA, "date": day, "grace_months": GRACE_MONTHS,
        "ipc": dict(ipc_out, snapshot=ipc,
                    sha256=sha256((root / ipc).read_bytes())),
        "queries": queries,
        "requests": getattr(client, "requests", None),
        "http_429": getattr(client, "http_429", None),
        "register_sha256": sha256((root / register.REGISTER).read_bytes()),
        "episodes": len(built["episodes"]),
    }
    write_json(root / READINGS / f"{day}.json", reading)
    return reading


def log_detail(reading: dict) -> dict:
    outcomes: dict[str, int] = {}
    for q in reading["queries"]:
        key = q.get("outcome") or q["decision"]
        outcomes[key] = outcomes.get(key, 0) + 1
    return {"date": reading["date"], "ipc": reading["ipc"]["status"],
            "queries": outcomes, "episodes": reading["episodes"],
            "requests": reading["requests"], "http_429": reading["http_429"]}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="The Interval's weekly reading")
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--day", default=dt.datetime.now(dt.timezone.utc)
                        .strftime("%Y-%m-%d"))
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    if (root / READINGS / f"{args.day}.json").exists():
        print(f"{READINGS}/{args.day}.json exists; nothing to do")
        return 0
    reading = run(root, args.day, Client())
    fetched = [q for q in reading["queries"] if q["decision"] == "fetch"]
    autonomy.append(root, "interval-reading", "machine",
                    detail=log_detail(reading))
    print(f"{READINGS}/{args.day}.json: ipc {reading['ipc']['status']}, "
          f"{len(fetched)} fetched, "
          f"{len(reading['queries']) - len(fetched)} frozen, "
          f"{reading['episodes']} episodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
