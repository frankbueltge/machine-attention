"""The Interval: rule `drivers-grfc-v1` — a driver per episode, read
mechanically from the preserved Global Report on Food Crises database.

Audit and recommendation: docs/2026-10-22-the-interval-treiber-quelle-audit.md
§2; this module writes the rule down as code before any driver is entered
(docs/2026-10-22-the-interval-treiber-regel.md). It reads only committed
bytes; no network, no wall clock. `verify.py` re-derives every entry of
`interval/drivers.json` that names this rule, independently of this package.

1. For an episode (country, t0 = YYYY-MM) the row with `ISO Code 3` = country
   and `Year of reference` = YYYY counts; with two (main edition and the
   mid-year update "MYU"), the later edition. No row → `unassigned`.
2. `driver` is the **primary** driver: `Conflict/insecurity` → `conflict`,
   `Economic shocks` → `economic`, `Weather extremes` → `weather`. `drought`
   and `mixed` are never given: the source does not say them. Any other
   primary (`None`, `N/A`, empty, an unknown word) → `unassigned`.
3. Secondary and tertiary drivers are carried verbatim, never folded into the
   label; `N/A`, `None` and empty cells are dropped.

The xlsx is read with the standard library: the first sheet of the workbook,
shared and inline strings, header row first.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from ..preserve import read_json, sha256

RULE = "drivers-grfc-v1"
PRIMARY = {
    "Conflict/insecurity": "conflict",
    "Economic shocks": "economic",
    "Weather extremes": "weather",
}
EMPTY = ("", "N/A", "None")
COLUMNS = ("ISO Code 3", "GRFC edition", "Year of reference",
           "Primary driver", "Secondary driver", "Tertiary driver")

_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"
_COL = re.compile(r"^([A-Z]+)")
_EDITION = re.compile(r"^(\d{4})( MYU)?$")


def _text(node) -> str:
    return "".join(t.text or "" for t in node.iter(_NS + "t"))


def read_rows(data: bytes) -> list[dict[str, str]]:
    """The first sheet as a list of {header: cell text}, header row dropped."""
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = set(z.namelist())
        shared = []
        if "xl/sharedStrings.xml" in names:
            shared = [_text(si) for si in
                      ET.fromstring(z.read("xl/sharedStrings.xml")).iter(_NS + "si")]
        book = ET.fromstring(z.read("xl/workbook.xml"))
        rid = next(book.iter(_NS + "sheet")).get(_REL + "id")
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = next(r.get("Target") for r in rels.iter(_PKG + "Relationship")
                      if r.get("Id") == rid)
        sheet = ET.fromstring(z.read("xl/" + target.lstrip("/").removeprefix("xl/")))
    table = []
    for row in sheet.iter(_NS + "row"):
        cells = {}
        for c in row.iter(_NS + "c"):
            col = _COL.match(c.get("r")).group(1)
            kind, v = c.get("t"), c.find(_NS + "v")
            if kind == "inlineStr":
                cells[col] = _text(c)
            elif v is not None:
                cells[col] = shared[int(v.text)] if kind == "s" else v.text
        table.append(cells)
    if not table:
        return []
    header = table[0]
    return [{header[k]: r.get(k, "") for k in header} for r in table[1:]]


def edition_key(edition: str) -> tuple[int, int]:
    """`2025` < `2025 MYU` < `2026`; anything else is refused."""
    m = _EDITION.match(edition.strip())
    if not m:
        raise ValueError(f"unknown GRFC edition {edition!r}")
    return int(m.group(1)), 1 if m.group(2) else 0


def _year(cell: str) -> int | None:
    try:
        return int(float(cell))
    except (TypeError, ValueError):
        return None


def assign(rows: list[dict[str, str]], country: str, t0: str) -> dict:
    """The rule for one episode. Returns driver, the primary as written, the
    secondaries verbatim, and the edition and year of the row used."""
    year = int(t0[:4])
    found = [r for r in rows
             if r.get("ISO Code 3", "").strip() == country
             and _year(r.get("Year of reference")) == year]
    if not found:
        return {"driver": "unassigned", "primary": None, "secondary": [],
                "grfc_edition": None, "year_of_reference": year}
    row = max(found, key=lambda r: edition_key(r.get("GRFC edition", "")))
    primary = row.get("Primary driver", "").strip()
    return {
        "driver": PRIMARY.get(primary, "unassigned"),
        "primary": primary or None,
        "secondary": [row.get(k, "").strip()
                      for k in ("Secondary driver", "Tertiary driver")
                      if row.get(k, "").strip() not in EMPTY],
        "grfc_edition": row.get("GRFC edition", "").strip(),
        "year_of_reference": year,
    }


def entry(root: Path, source: str, country: str, t0: str) -> dict:
    """The `interval/drivers.json` entry the rule gives for one episode."""
    path = root / source
    out = {"country": country, "t0": t0}
    out.update(assign(read_rows(path.read_bytes()), country, t0))
    out["source"] = source if out["driver"] != "unassigned" else None
    out["grfc_file"] = source
    out["source_sha256"] = sha256(path.read_bytes())
    out["rule"] = RULE
    return out


def derive(root: Path, source: str) -> list[dict]:
    """The rule over every episode of the committed register. Printed, not
    written: entering drivers is a separate, dated step."""
    reg = read_json(root / "interval/register.json", {"episodes": []})
    return [entry(root, source, e["country"], e["t0"]) for e in reg["episodes"]]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--source", required=True,
                    help="committed GRFC xlsx, relative to the repo root")
    args = ap.parse_args(argv)
    print(json.dumps(derive(Path(args.repo_root), args.source), indent=1,
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
