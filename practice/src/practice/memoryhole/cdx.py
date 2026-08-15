"""Wayback CDX access — query forms, row parsing, and the corrected
classification.

Inherited from the origin (`redaction/cdx.py`): the query parameters, the
snapshot and permalink forms, and the rule that only a 4xx counts as a possible
deletion (a 3xx is a move, a 5xx is weather).

Corrected here, per audit finding 2: **a 4xx is a deletion CANDIDATE, never a
deletion.** The origin's `_is_dead` turns the most recent 4xx capture straight
into `kind=deletion`; the BaFin probe of 2026-08-14 showed what that costs — a
403 in the archive, 146 bytes of nginx behind it, and the institution answering
200 to anyone who asks. Nothing leaves this module already called `gone`; the
live recheck decides that (`recheck.py`).

Two query forms, both proven live on 2026-08-14/15 and recorded per watchlist
entry with the probe that justifies them:

  discovery  one query per institution for one UTC day, `matchType=domain` or
             `prefix`, HTML only, one row per URL — this is the domain-scope
             architecture the audit made condition 1
  history    the origin's production form for a single URL: distinct
             consecutive digests, newest 40
"""

from __future__ import annotations

import json
import urllib.parse
from dataclasses import dataclass

CDX_VERSION = "cdx-v1"
CDX_BASE = "https://web.archive.org/cdx/search/cdx"
WAYBACK = "https://web.archive.org/web"

DISCOVERY_FIELDS = "timestamp,original,statuscode,digest"
HISTORY_FIELDS = "timestamp,original,statuscode,digest"
DISCOVERY_LIMIT = 3000
HISTORY_LIMIT = 40


@dataclass(frozen=True)
class Row:
    timestamp: str
    original: str
    statuscode: str
    digest: str


def discovery_url(target: str, match_type: str, day: str) -> str:
    """One institution, one completed UTC day. `collapse=urlkey` makes the
    answer a list of pages the archive touched that day rather than a list of
    captures; the mimetype filter keeps PDFs and images out of a text
    instrument."""
    stamp = day.replace("-", "")
    params = {
        "url": target,
        "matchType": match_type,
        "from": stamp,
        "to": stamp,
        "output": "json",
        "fl": DISCOVERY_FIELDS,
        "filter": "mimetype:text/html",
        "collapse": "urlkey",
        "limit": str(DISCOVERY_LIMIT),
    }
    return f"{CDX_BASE}?{urllib.parse.urlencode(params)}"


def history_url(url: str) -> str:
    """The origin's production form: distinct consecutive digests, newest
    first-40 window. Full history depth, so the "before" of a page the archive
    last touched in 2019 is still findable."""
    params = {
        "url": url,
        "output": "json",
        "fl": HISTORY_FIELDS,
        "collapse": "digest",
        "limit": str(-HISTORY_LIMIT),
    }
    return f"{CDX_BASE}?{urllib.parse.urlencode(params)}"


def snapshot_url(timestamp: str, original: str) -> str:
    """Raw archived resource (id_ modifier) — content without the wrapper."""
    return f"{WAYBACK}/{timestamp}id_/{original}"


def permalink(timestamp: str, original: str) -> str:
    """Human-viewable archived page — the second of the two clicks E-2 owes
    every published record."""
    return f"{WAYBACK}/{timestamp}/{original}"


def redacted(url: str) -> str:
    """Error strings land in a public archive — never leak query params."""
    return url.split("?", 1)[0]


def parse(data: bytes) -> list[Row]:
    """CDX JSON to rows. An empty body is a legitimate answer (no captures);
    the header row is dropped."""
    text = data.decode("utf-8", errors="replace").strip()
    if not text:
        return []
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        return []
    if not raw or len(raw) < 2:
        return []
    rows = []
    for entry in raw[1:]:
        if len(entry) < 4:
            continue
        rows.append(Row(timestamp=str(entry[0]), original=str(entry[1]),
                        statuscode=str(entry[2]), digest=str(entry[3])))
    rows.sort(key=lambda r: r.timestamp)
    return rows


def is_ok(status: str) -> bool:
    return status == "200"


def is_deletion_candidate(status: str) -> bool:
    """4xx only. A 3xx is a move — a page that moved was not redacted. A 5xx is
    the archive having a bad night. Neither is a claim about a publisher."""
    return status.startswith("4")


def within_day(rows: list[Row], day: str) -> list[Row]:
    """Everything up to the end of the completed day. A run happening after
    midnight must not let today's captures decide yesterday's record."""
    end = day.replace("-", "") + "235959"
    return [r for r in rows if r.timestamp <= end]


def on_day(row: Row, day: str) -> bool:
    return row.timestamp.startswith(day.replace("-", ""))


@dataclass(frozen=True)
class Reading:
    kind: str          # changed_candidate | deletion_candidate | unchanged | unverifiable
    reason: str
    before: Row | None = None
    after: Row | None = None


def classify(rows: list[Row], day: str) -> Reading:
    """What the preserved history says about one page on one day.

    `collapse=digest` does the work that matters: a capture whose content
    equals the preceding capture's is folded away, so a day-D row surviving in
    the answer IS a new digest, and a day with no surviving row is a day whose
    capture said the same thing as before.
    """
    rows = within_day(rows, day)
    if not rows:
        return Reading("unverifiable", "no_capture_in_archive")
    newest = rows[-1]
    if not on_day(newest, day):
        return Reading("unchanged", "no_new_digest_on_day", after=newest)
    if is_ok(newest.statuscode):
        earlier_ok = [r for r in rows[:-1] if is_ok(r.statuscode)]
        if not earlier_ok:
            return Reading("unverifiable", "no_earlier_capture", after=newest)
        return Reading("changed_candidate", "new_digest",
                       before=earlier_ok[-1], after=newest)
    if is_deletion_candidate(newest.statuscode):
        earlier_ok = [r for r in rows[:-1] if is_ok(r.statuscode)]
        return Reading("deletion_candidate", f"archive_status_{newest.statuscode}",
                       before=earlier_ok[-1] if earlier_ok else None,
                       after=newest)
    return Reading("unverifiable", f"archive_status_{newest.statuscode}",
                   after=newest)
