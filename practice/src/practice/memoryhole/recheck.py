"""Live recheck — the step that turns a 4xx in the archive into a statement,
or refuses to.

Directly applicable code from the origin's world chamber
(`redaction/world/recheck.py`, productive since 2026-08-14): the disclosure
classes, the rule that bot-walls and server errors leave the denominator, and
the Wilson interval. Audit condition 3: "gone" is a checked assertion, never a
CDX row.

Classes, and what they honestly are:

  ok           the URL still answers 2xx — the archive's 4xx was weather
  gone_404 /
  gone_410     the page is gone; with the preserved manifest, a receipt
  legal_451    reported as its own number, never folded into the gone rate:
               from a German vantage point 451 can mean EU geo-blocking
  botwall      401/403/429 — the site refuses machines; unverifiable, out of
               the denominator, disclosed as a count (bp.com is the entry the
               watchlist expects here)
  server_error 5xx — indeterminate, excluded like botwall
  unreachable  network failure or timeout — excluded like botwall
"""

from __future__ import annotations

import math

from ..fetch import Client, SourceUnavailable

RECHECK_VERSION = "recheck-v1"

OK = "ok"
GONE_404 = "gone_404"
GONE_410 = "gone_410"
LEGAL_451 = "legal_451"
BOTWALL = "botwall"
SERVER_ERROR = "server_error"
UNREACHABLE = "unreachable"
OTHER = "other"

CLASSES = (OK, GONE_404, GONE_410, LEGAL_451, BOTWALL, SERVER_ERROR,
           UNREACHABLE, OTHER)
GONE = (GONE_404, GONE_410)
EXCLUDED = (BOTWALL, SERVER_ERROR, UNREACHABLE)

# A live page is fetched with a browser-ish Accept; the substrate's JSON
# default earns a 406 from more than one ministry.
HTML_HEADERS = {"Accept": "text/html,application/xhtml+xml,*/*;q=0.8"}


def classify_code(code: int) -> str:
    if 200 <= code < 300:
        return OK
    if code == 404:
        return GONE_404
    if code == 410:
        return GONE_410
    if code == 451:
        return LEGAL_451
    if code in (401, 403, 429):
        return BOTWALL
    if 500 <= code < 600:
        return SERVER_ERROR
    return OTHER


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, center - half), min(1.0, center + half))


def check(client: Client, url: str) -> dict:
    """One live look. The body is read and thrown away — the substrate's client
    has no HEAD path, and adding one for a handful of URLs a night would buy
    less than it costs in surface."""
    try:
        _, status = client.fetch(url, headers=HTML_HEADERS)
    except SourceUnavailable as err:
        return {"class": UNREACHABLE, "http_code": None, "detail": str(err)}
    return {"class": classify_code(status), "http_code": status}


def summarize(results: list[str]) -> dict:
    """Counts, the gone rate over the decided, and its Wilson interval."""
    counts = {cls: 0 for cls in CLASSES}
    for cls in results:
        counts[cls] = counts.get(cls, 0) + 1
    gone = counts[GONE_404] + counts[GONE_410]
    decided = counts[OK] + gone + counts[LEGAL_451] + counts[OTHER]
    excluded = sum(counts[c] for c in EXCLUDED)
    low, high = wilson(gone, decided)
    return {
        "candidates": len(results),
        "counts": counts,
        "decided": decided,
        "excluded_unverifiable": excluded,
        "gone": gone,
        "gone_rate": round(gone / decided, 4) if decided else None,
        "gone_ci95": [round(low, 4), round(high, 4)] if decided else None,
    }
