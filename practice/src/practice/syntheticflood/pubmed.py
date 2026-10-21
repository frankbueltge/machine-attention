"""PubMed E-utilities counts — one number per query, no text ever fetched.

The esearch count answer is fully determined by the count (audit probes
2026-10-18: every one of the seven count answers is byte-identical to
`canonical(count)`), so a reading stores the query, the count and the SHA-256
of what arrived, and the verifier recomputes the bytes from the count. An
answer that is not canonical is preserved as bytes instead.
"""

from __future__ import annotations

import json
import urllib.parse

HOST = "eutils.ncbi.nlm.nih.gov"
ESEARCH = f"https://{HOST}/entrez/eutils/esearch.fcgi"
TOOL = "machine-attention"


def cohort_term(month: str, word: str | None = None) -> str:
    """month is YYYY-MM, or YYYY for a whole baseline year; word None means
    the whole cohort (the denominator)."""
    if "-" in month:
        year, mm = month.split("-")
        base = f"hasabstract AND {year}/{mm}[dp]"
    else:
        base = f"hasabstract AND {month}[dp]"
    return f"{word}[tiab] AND {base}" if word else base


def count_url(term: str) -> str:
    return (f"{ESEARCH}?db=pubmed&rettype=count&retmode=json&tool={TOOL}"
            f"&term={urllib.parse.quote_plus(term, safe='/[]')}")


def canonical(count: int) -> bytes:
    return ('{"header":{"type":"esearch","version":"0.3"},'
            '"esearchresult":{"count":"%d"}}\n' % count).encode()


def parse_count(data: bytes) -> int:
    doc = json.loads(data)
    result = doc["esearchresult"]
    if "ERROR" in result or "count" not in result:
        raise ValueError("esearch answered without a count")
    return int(result["count"])
