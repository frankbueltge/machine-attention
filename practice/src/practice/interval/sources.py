"""Source adapters for The Interval V0, increment 1: fetch and preserve.

Two public, keyless axes (docs/2026-10-04-kandidat-the-interval.md §2):

- IPC on HDX, CC0 — one file per week: the national long table, resolved
  through the dataset's CKAN record so a moved resource id costs nothing.
  HDX asks crawlers to stay off /api/ and *.csv and documents programmatic
  CKAN use; the weekly cadence, the honest user agent and the skip of
  identical bytes are the politeness. The substrate client does not expose
  response headers, so an ETag cannot be read; identical content is detected
  by SHA-256 against the newest committed snapshot instead.
- OCHA FTS flows, keyless — pages of up to 200 followed through `nextLink`.
  `years` is passed to the source verbatim: a comma list ("2011,2012") and a
  range ("2011-2013") are NOT the same query (probe of 2026-10-09, Somalia
  2011-2013: 1,912 against 13,229 flows), so the form used is part of the
  preserved URL and nothing here normalises it.

The FEWS NET data warehouse is not an axis and is never fetched.
"""

from __future__ import annotations

import json
import urllib.parse
from pathlib import Path

from ..fetch import Client, SourceUnavailable
from ..preserve import Snapshot, read_json, sha256

BASE = "interval/snapshots"
HDX_PACKAGE_URL = ("https://data.humdata.org/api/3/action/package_show"
                   "?id=global-acute-food-insecurity-country-data")
IPC_RESOURCE = "ipc_global_national_long.csv"
FTS_URL = "https://api.hpc.tools/v1/public/fts/flow"
FTS_PAGE_LIMIT = 200
MAX_PAGES = 200  # a runaway nextLink loop ends here, recorded, never silent


def resolve_ipc_url(package: dict, name: str = IPC_RESOURCE) -> str:
    """CKAN package_show payload -> download URL of the named resource."""
    for res in package.get("result", {}).get("resources", []):
        if res.get("name") == name and res.get("download_url"):
            return res["download_url"]
    raise SourceUnavailable(HDX_PACKAGE_URL, f"resource {name} not listed")


def fts_url(country_iso3: str, years: str, *, filter_by: str | None = None,
            limit: int = FTS_PAGE_LIMIT) -> str:
    params = [("countryISO3", country_iso3), ("year", years),
              ("limit", str(limit))]
    if filter_by:
        params.append(("filterBy", filter_by))
    return FTS_URL + "?" + urllib.parse.urlencode(params, safe=",:")


def fts_pages(client: Client, url: str) -> list[tuple[str, bytes, int]]:
    """Follow nextLink. Returns [(url, bytes, status)]; stops at the first
    non-200 (kept, so the failure is in the record) or at MAX_PAGES."""
    pages = []
    seen = set()
    while url and url not in seen and len(pages) < MAX_PAGES:
        seen.add(url)
        data, status = client.fetch(url)
        pages.append((url, data, status))
        if status != 200:
            break
        url = (json.loads(data).get("meta") or {}).get("nextLink")
    return pages


def newest_sha(repo_root: Path, name: str) -> str | None:
    """SHA-256 of the newest committed copy of `name`, if any."""
    root = repo_root / BASE
    for day in sorted((p.name for p in root.glob("*") if p.is_dir()),
                      reverse=True):
        manifest = read_json(root / day / "manifest.json", {"entries": []})
        for entry in reversed(manifest["entries"]):
            if entry["file"].endswith("/" + name):
                return entry["sha256"]
    return None


def snapshot_ipc(repo_root: Path, day: str, client: Client) -> dict:
    """Preserve the IPC national long table; skip when bytes are unchanged."""
    pkg_bytes, status = client.fetch(HDX_PACKAGE_URL)
    if status != 200:
        raise SourceUnavailable(HDX_PACKAGE_URL, f"HTTP {status}")
    url = resolve_ipc_url(json.loads(pkg_bytes))
    data, status = client.fetch(url, headers={"Accept": "text/csv,*/*"})
    if status != 200:
        raise SourceUnavailable(url, f"HTTP {status}")
    if newest_sha(repo_root, IPC_RESOURCE) == sha256(data):
        return {"name": IPC_RESOURCE, "preserved": False,
                "reason": "identical to newest snapshot"}
    snap = Snapshot(repo_root, day, base=BASE)
    snap.preserve("ipc/package_show.json", pkg_bytes, HDX_PACKAGE_URL, 200)
    entry = snap.preserve(f"ipc/{IPC_RESOURCE}", data, url, status)
    snap.write_manifest()
    return {"name": IPC_RESOURCE, "preserved": True, "sha256": entry["sha256"],
            "bytes": entry["bytes"]}


def snapshot_fts(repo_root: Path, day: str, client: Client, country_iso3: str,
                 years: str, *, filter_by: str | None = None) -> dict:
    """Preserve every page of one FTS flow query under fts/<ISO3>/."""
    pages = fts_pages(client, fts_url(country_iso3, years, filter_by=filter_by))
    snap = Snapshot(repo_root, day, base=BASE)
    tag = "fsc" if filter_by else "total"
    for i, (url, data, status) in enumerate(pages, 1):
        snap.preserve(f"fts/{country_iso3}/{tag}-{years.replace(',', '_')}"
                      f"-p{i:03d}.json", data, url, status)
    snap.write_manifest()
    complete = bool(pages) and pages[-1][2] == 200 and not (
        json.loads(pages[-1][1]).get("meta") or {}).get("nextLink")
    return {"country": country_iso3, "pages": len(pages), "complete": complete}
