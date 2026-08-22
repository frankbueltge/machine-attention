"""Source adapters for Dark Ocean V0 — Coverage vs Declaration.

Two public axes, both keyless (audited 2026-08-08, live probes):

- CDSE OData catalog — which Sentinel-1 GRD scenes looked at the region,
  when, with the issuer's own checksums (BLAKE3/MD5). Scene bytes are never
  fetched: they are 1–2 GB each and login-walled; the catalog row IS the
  notarized act of observation, and its EvictionDate field is the reason it
  must be preserved the day it is seen — the catalog itself forgets.
- Digitraffic (Fintraffic) AIS — the declared ocean, sampled at reading
  time. Coverage is the source's own receiver range (Finnish coastal
  waters), not the whole region: the declared axis carries its own
  visibility boundary, which is part of the subject, not a nuisance.

DMA (Denmark) day dumps would carry the per-moment declared axis; the
source failed its first three probes on 2026-08-08 and has not answered
on any night recorded since (foreknown/proposals/obs-2026-08-22-1.json)
— it is probed (never fetched) each night until it answers; an ongoing
outage is recorded, not bridged.
"""

from __future__ import annotations

import gzip
import urllib.parse
import urllib.request
from datetime import date as date_cls
from datetime import timedelta

from ..fetch import USER_AGENT
from .region import REGION_WKT, cell_id, covered_cells

CDSE_BASE = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
DIGITRAFFIC_URL = "https://meri.digitraffic.fi/api/ais/v1/locations"
DMA_URL = "http://web.ais.dk/aisdata/"

DMA_NOTE = ("would carry the per-moment declared axis (full-day position "
            "dumps); reachability is probed nightly and has not once "
            "answered since probing began (2026-08-08); the adapter is "
            "the recorded next step for the first night the source answers")


def cdse_url(day: str) -> str:
    """Catalog query: every Sentinel-1 GRD product whose acquisition started
    on UTC day `day` and intersects the region."""
    end = (date_cls.fromisoformat(day) + timedelta(days=1)).isoformat()
    query = (f"Collection/Name eq 'SENTINEL-1' and contains(Name,'GRD') "
             f"and ContentDate/Start ge {day}T00:00:00.000Z "
             f"and ContentDate/Start lt {end}T00:00:00.000Z "
             f"and OData.CSC.Intersects(area=geography'SRID=4326;"
             f"{REGION_WKT}')")
    return (f"{CDSE_BASE}?$top=1000&$orderby=ContentDate/Start%20asc"
            f"&$filter=" + urllib.parse.quote(query, safe="(),;=/:$"))


def cdse_scenes(pages: list[dict]) -> list[dict]:
    """Catalog products → scene records, verbatim fields plus derived cells."""
    scenes = []
    for page in pages:
        for product in page.get("value", []):
            name = product.get("Name", "")
            if "GRD" not in name:
                continue
            checksums = {c.get("Algorithm", "?").lower(): c.get("Value", "")
                         for c in (product.get("Checksum") or [])
                         if isinstance(c, dict) and c.get("Value")}
            content_date = product.get("ContentDate") or {}
            scenes.append({
                "name": name,
                "id": product.get("Id", ""),
                "platform": name[:3],
                "start": content_date.get("Start", ""),
                "end": content_date.get("End", ""),
                "bytes": product.get("ContentLength", 0),
                "checksums": checksums,
                "online": product.get("Online"),
                "eviction_date": product.get("EvictionDate"),
                # Recorded since 2026-08-09 so the continuity probe has a
                # preserved baseline to compare against rather than one it
                # established itself (criteria group N).
                "modification_date": product.get("ModificationDate"),
                "publication_date": product.get("PublicationDate"),
                "cells": covered_cells(product.get("GeoFootprint")),
            })
    scenes.sort(key=lambda s: (s["start"], s["name"]))
    return scenes


def acquisitions(scenes: list[dict]) -> list[dict]:
    """The catalog lists one act of observation as several products (formats).
    An acquisition is (platform, start, end); the first product stands for
    it. Both counts appear in the reading — the dedup is visible, not
    silent."""
    seen: dict = {}
    for scene in scenes:
        seen.setdefault((scene["platform"], scene["start"], scene["end"]),
                        scene)
    return [seen[key] for key in sorted(seen)]


def gunzip_if_needed(data: bytes) -> bytes:
    return gzip.decompress(data) if data[:2] == b"\x1f\x8b" else data


def declared_sample(parsed: dict) -> dict:
    """Digitraffic GeoJSON → counts per bin. Counts only: no vessel identity
    leaves this function."""
    counts: dict[str, int] = {}
    total = 0
    in_region = 0
    for feature in parsed.get("features", []):
        coords = (feature.get("geometry") or {}).get("coordinates") or []
        if len(coords) < 2:
            continue
        total += 1
        cid = cell_id(coords[0], coords[1])
        if cid:
            in_region += 1
            counts[cid] = counts.get(cid, 0) + 1
    return {"cells": counts, "vessels_in_feed": total,
            "vessels_in_region": in_region}


def probe_dma(opener=urllib.request.urlopen, timeout: int = 10) -> dict:
    """One reachability probe, one attempt, never a fetch. The state string
    lands in the reading either way."""
    request = urllib.request.Request(DMA_URL,
                                     headers={"User-Agent": USER_AGENT})
    try:
        with opener(request, timeout=timeout) as response:
            state = f"reachable (HTTP {response.status})"
    except Exception as err:  # noqa: BLE001 — any failure is the same fact
        state = f"outage: {err.__class__.__name__}"
    return {"url": DMA_URL, "state": state, "note": DMA_NOTE}
