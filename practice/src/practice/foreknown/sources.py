"""Source adapters: deterministic extraction of announced futures from
structured warning feeds. Every adapter maps preserved bytes to future
records — it never invents fields, and a source outage stays an outage.

V0 sources (audited 2026-08-08, both keyless):
- GDACS (EU/JRC): active Orange/Red hazard alert episodes, all types.
- NOAA NHC: tropical-cyclone advisories (genuine forecasts; an empty list
  is the honest quiet state).
"""

from __future__ import annotations

GDACS_URL = ("https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH"
             "?eventlist=EQ,TC,FL,DR,WF&alertlevel=Orange;Red")
NHC_URL = "https://www.nhc.noaa.gov/CurrentStorms.json"
FTS_PLANS_URL = "https://api.hpc.tools/v1/public/plan/year/2026"

HAZARD_NAMES = {"EQ": "earthquake", "TC": "tropical cyclone", "FL": "flood",
                "DR": "drought", "WF": "wildfire"}


def _clean_date(value) -> str | None:
    """GDACS dates come as naive ISO strings; keep them verbatim but typed."""
    if isinstance(value, str) and len(value) >= 10:
        return value
    return None


def primary_iso3(properties: dict) -> set[str]:
    """The feature's top-level singular `iso3` — the event's current reporting
    position — as a set, empty when the feed leaves it blank.

    Kept separate from the extraction so the guard in `run.py` can measure the
    same field the registry is built from, rather than a second reading of it.
    """
    value = str(properties.get("iso3") or "").strip()
    return {value} if value else set()


def gdacs_futures(parsed: dict) -> list[dict]:
    """Map the GDACS active-alert feed to announced-future records.

    The feature's own primary country is folded into `iso3`; see
    `primary_iso3` and the note at the field.

    kind ALERT_EPISODE: GDACS mostly reports hazards already in motion whose
    episode window extends into the future — announced, dated, and revisable.
    """
    futures = []
    for feature in parsed.get("features", []):
        p = feature.get("properties", {})
        event_id = p.get("eventid")
        hazard = p.get("eventtype")
        if event_id is None or hazard not in HAZARD_NAMES:
            continue
        futures.append({
            "id": f"gdacs-{hazard.lower()}-{event_id}",
            "kind": "ALERT_EPISODE",
            "source": "GDACS",
            "hazard": HAZARD_NAMES[hazard],
            "what": str(p.get("name") or p.get("eventname") or "").strip(),
            "where": str(p.get("country") or "").strip(),
            # The feed names the country twice: `affectedcountries` (the
            # episode's footprint) and a top-level singular `iso3` (the event's
            # current reporting position). Reading only the list dropped the
            # primary country of six tropical cyclones — Vietnam never entered
            # the registry although those futures' own `where` text named it.
            # Found by the machine's own discovery pass, obs-2026-08-09-1.
            "iso3": sorted(
                {c.get("iso3", "") for c in p.get("affectedcountries", [])
                 if isinstance(c, dict) and c.get("iso3")}
                | primary_iso3(p)),
            "severity": str(p.get("alertlevel") or ""),
            "window": {"from": _clean_date(p.get("fromdate")),
                       "to": _clean_date(p.get("todate"))},
            "source_ref": str(p.get("url", {}).get("report", "")
                              if isinstance(p.get("url"), dict) else p.get("url") or ""),
        })
    return futures


def nhc_futures(parsed: dict) -> list[dict]:
    """Map NHC current storms to announced-future records (kind FORECAST)."""
    futures = []
    for storm in parsed.get("activeStorms", []):
        storm_id = storm.get("id") or storm.get("binNumber")
        if not storm_id:
            continue
        futures.append({
            "id": f"nhc-{str(storm_id).lower()}",
            "kind": "FORECAST",
            "source": "NHC",
            "hazard": "tropical cyclone",
            "what": str(storm.get("name") or "").strip() + " (" +
                    str(storm.get("classification") or "storm").strip() + ")",
            "where": str(storm.get("binNumber") or ""),
            "iso3": [],
            "severity": str(storm.get("intensity") or ""),
            "window": {"from": _clean_date(storm.get("lastUpdate")), "to": None},
            "source_ref": "https://www.nhc.noaa.gov/",
        })
    return futures
