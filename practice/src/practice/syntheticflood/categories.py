"""Register B reader: one request a day, the answer kept as bytes.

    python -m practice.syntheticflood.categories --repo-root .

writes syntheticflood/categories/<date>.json and preserves the answer
(about 4 KB) under syntheticflood/snapshots/<date>-categories/. The reading
is derived from the preserved bytes; the verifier derives it again.
"""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .. import autonomy
from ..fetch import Client, SourceUnavailable
from ..preserve import Snapshot, utc_now, write_json
from . import wikipedia

SCHEMA = "syntheticflood-categories-v1"
SNAP_BASE = "syntheticflood/snapshots"


def read(repo_root: Path, read_on: str, client: Client | None = None) -> dict:
    client = client or Client()
    started = utc_now()
    reading = {"schema": SCHEMA, "date": read_on, "source": wikipedia.HOST,
               "url": wikipedia.URL, "user_agent": wikipedia.USER_AGENT,
               "started_at": started}
    try:
        data, status = client.fetch(wikipedia.URL,
                                    headers={"User-Agent": wikipedia.USER_AGENT})
    except SourceUnavailable as e:
        data, status = None, None
        reading["error"] = e.detail
    if data is not None:
        snap = Snapshot(repo_root, f"{read_on}-categories", base=SNAP_BASE)
        entry = snap.preserve("allcategories.json", data, wikipedia.URL, status)
        snap.write_manifest()
        reading.update(file=entry["file"], sha256=entry["sha256"])
        if status == 200:
            try:
                reading.update(wikipedia.parse(data))
            except (ValueError, KeyError, TypeError) as e:
                reading["error"] = f"unparsed answer: {e.__class__.__name__}"
    reading.update(status=status, finished_at=utc_now(),
                   requests=client.requests, http_429=client.http_429)
    return reading


def reading_path(repo_root: Path, read_on: str) -> Path:
    return repo_root / "syntheticflood" / "categories" / f"{read_on}.json"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--date", default=date.today().isoformat())
    args = p.parse_args(argv)
    root = args.repo_root.resolve()
    out = reading_path(root, args.date)
    if out.exists():
        print(f"{out.relative_to(root)} exists; a reading is never rewritten")
        return 1
    reading = read(root, args.date)
    write_json(out, reading)
    texts = (reading.get("families") or {}).get("texts", {}).get("months", {})
    autonomy.append(root, "syntheticflood-category-reading", "machine", detail={
        "date": args.date, "status": reading["status"],
        "requests": reading["requests"], "http_429": reading["http_429"],
        "texts_months": len(texts), "texts_pages": sum(texts.values()),
        "error": reading.get("error")})
    print(f"{out.relative_to(root)}: status {reading['status']}, "
          f"{len(texts)} dated months, {sum(texts.values())} tagged pages, "
          f"{reading['http_429']} x 429")
    return 0 if "families" in reading else 2


if __name__ == "__main__":
    raise SystemExit(main())
