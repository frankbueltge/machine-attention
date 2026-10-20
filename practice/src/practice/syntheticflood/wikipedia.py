"""Register B: the sizes of Wikipedia's dated maintenance categories for
suspected machine-written text — one `allcategories` request, nothing else.

The answer carries category names and sizes only; no page title, no user
name is ever asked for (audit 2026-10-18, finding 4; I8, E-2). A dated
subcategory counts the articles tagged in that month *whose tag still
stands*: the series is a standing backlog by tag month, not an inflow, and
only the daily reading separates inflow from removal.
"""

from __future__ import annotations

import json
import re

HOST = "en.wikipedia.org"
PREFIX = "Articles containing suspected AI"
URL = (f"https://{HOST}/w/api.php?format=json&formatversion=2&action=query"
       "&list=allcategories&acprefix=Articles+containing+suspected+AI"
       "&acprop=size&aclimit=500")
# The operator's policy asks for a contact in the user agent; the public
# repository is one, without a person (audit 2026-10-18, finding 5).
USER_AGENT = ("machine-attention/0.1 (https://github.com/frankbueltge/"
              "machine-attention; public research practice)")
FAMILIES = {"texts": "Articles containing suspected AI-generated texts",
            "sources": "Articles containing suspected AI-generated sources"}
MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")
DATED = re.compile(r"(?P<family>.+) from (?P<month>[A-Z][a-z]+) (?P<year>\d{4})")


def parse(data: bytes) -> dict:
    """Bytes of one answer -> {complete, families, unmatched}. Raises on a
    shape that is not an allcategories answer."""
    doc = json.loads(data)
    rows = doc["query"]["allcategories"]
    families = {key: {"container": None, "months": {}} for key in FAMILIES}
    unmatched = []
    by_name = {name: key for key, name in FAMILIES.items()}
    for row in rows:
        name, size = row["category"], int(row["size"])
        if name in by_name:
            families[by_name[name]]["container"] = {
                "size": size, "pages": int(row["pages"]),
                "subcats": int(row["subcats"])}
            continue
        m = DATED.fullmatch(name)
        if m and m["family"] in by_name and m["month"] in MONTHS:
            month = f"{m['year']}-{MONTHS.index(m['month']) + 1:02d}"
            families[by_name[m["family"]]]["months"][month] = size
        else:
            unmatched.append({"category": name, "size": size})
    for fam in families.values():
        fam["months"] = dict(sorted(fam["months"].items()))
    # One request a day: a continuation is recorded, never followed.
    return {"complete": "continue" not in doc, "families": families,
            "unmatched": unmatched}
