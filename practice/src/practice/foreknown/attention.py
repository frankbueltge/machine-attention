"""The attention axis: how much of the world's recorded news volume falls on
each country on a given UTC day.

Source: the GDELT 1.0 daily event export — one file per UTC day, published
the following morning, immutable once published. Not the DOC 2.0 API: that
API rate-limits per IP with sticky, opaque blocks (measured in this house on
2026-08-04/05, see frankbueltge.de/pipelines/newspool), while the raw files
are plain static downloads. Same reasoning, same host, same discipline.

The raw bytes are deliberately NOT stored here: one day is ~6.4 MB and the
file does not change once published. Every derived day record carries the
url, the SHA-256 of the bytes we actually read, their length and the
retrieval time — anyone can re-fetch and verify the derivation. A hash that
stops matching is not a broken link; it is the finding.

Honest limits, kept in every record:
- `articles` sums GDELT's NumArticles across the events located in a country.
  One article covering three events is counted three times. It is a volume
  proxy, not a count of distinct articles.
- Country attribution is GDELT's ActionGeo_CountryCode (FIPS 10-4), i.e. the
  place the event was located in, not the place it was reported from.
- Events with no location are counted in `unlocated`, never redistributed.
"""

from __future__ import annotations

import io
import zipfile
from datetime import date as date_cls
from datetime import timedelta

from ..preserve import sha256, utc_now, write_json

GDELT_DAILY_URL = "http://data.gdeltproject.org/events/{stamp}.export.CSV.zip"
FIPS_LOOKUP_URL = "https://www.gdeltproject.org/data/lookups/FIPS.country.txt"

# GDELT 1.0 event codebook: 58 tab-separated columns, no header row.
COLUMNS = 58
COL_MENTIONS = 31
COL_ARTICLES = 33
COL_ACTION_GEO_COUNTRY = 51

EMPTY = {"events": 0, "articles": 0, "mentions": 0}


def day_url(day: str) -> str:
    return GDELT_DAILY_URL.format(stamp=day.replace("-", ""))


def days_before(day: str, count: int) -> list[str]:
    """The `count` UTC days immediately before `day`, oldest first."""
    anchor = date_cls.fromisoformat(day)
    return [(anchor - timedelta(days=n)).isoformat()
            for n in range(count, 0, -1)]


def aggregate(raw_zip: bytes) -> dict:
    """Fold one day's export into per-country volume. Deterministic."""
    countries: dict[str, dict] = {}
    world = dict(EMPTY)
    unlocated = dict(EMPTY)
    rows = 0
    malformed = 0

    with zipfile.ZipFile(io.BytesIO(raw_zip)) as archive:
        name = archive.namelist()[0]
        with archive.open(name) as handle:
            for line in io.TextIOWrapper(handle, encoding="utf-8",
                                         errors="replace"):
                cols = line.rstrip("\n").split("\t")
                if len(cols) < COLUMNS:
                    malformed += 1
                    continue
                try:
                    mentions = int(cols[COL_MENTIONS] or 0)
                    articles = int(cols[COL_ARTICLES] or 0)
                except ValueError:
                    malformed += 1
                    continue
                rows += 1
                code = cols[COL_ACTION_GEO_COUNTRY].strip()
                bucket = countries.setdefault(code, dict(EMPTY)) if code \
                    else unlocated
                for target in (bucket, world):
                    target["events"] += 1
                    target["articles"] += articles
                    target["mentions"] += mentions

    return {"countries": countries, "world": world, "unlocated": unlocated,
            "rows": rows, "malformed_rows": malformed}


def day_record(day: str, raw_zip: bytes, url: str) -> dict:
    """One committed attention day: the aggregate plus its artifact reference.

    The reference — url, sha256, length, retrieval time — stands in for bytes
    too large to keep in git. It is only worth anything because the file is
    immutable at that url; that claim is itself testable by re-fetching.
    """
    record = aggregate(raw_zip)
    record["date"] = day
    record["source"] = {
        "url": url,
        "sha256": sha256(raw_zip),
        "bytes": len(raw_zip),
        "retrieved_at": utc_now(),
        "media_type": "application/zip",
        "stored": False,
    }
    record["note"] = (
        "GDELT 1.0 daily event export, aggregated by ActionGeo_CountryCode "
        "(FIPS 10-4). `articles` sums NumArticles across events located in "
        "the country — a volume proxy, not distinct articles. Bytes not kept "
        "in this repository: the file is immutable at its url and the sha256 "
        "above lets any reader redo this aggregation.")
    return record


def record_path(repo_root, day: str):
    return repo_root / "foreknown" / "reaction" / "attention" / f"{day}.json"


def write_day(repo_root, day: str, raw_zip: bytes, url: str) -> dict:
    record = day_record(day, raw_zip, url)
    write_json(record_path(repo_root, day), record)
    return record


def articles_for(day_record_: dict, fips_codes) -> int:
    """The day's article volume for a set of FIPS country codes."""
    countries = day_record_.get("countries", {})
    return sum(countries.get(code, EMPTY).get("articles", 0)
               for code in fips_codes)


def median(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2
