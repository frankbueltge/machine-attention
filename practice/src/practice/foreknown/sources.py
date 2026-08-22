"""Source adapters: deterministic extraction of announced futures from
structured warning feeds. Every adapter maps preserved bytes to future
records — it never invents fields, and a source outage stays an outage.

V0 sources (audited 2026-08-08, both keyless):
- GDACS (EU/JRC): active Orange/Red hazard alert episodes, all types.
- NOAA NHC: tropical-cyclone advisories (genuine forecasts; an empty list
  is the honest quiet state).

Third source (audited 2026-08-22, keyless, US public domain): NWS CAP alerts.
E1 asked for at least three sources and the register had two for fourteen
nights. Of the candidates probed that day, ReliefWeb needs an approved
application name, IFRC GO embeds named individuals' contact details in its
event records, Copernicus EMS publishes no machine-readable activation list,
JTWC publishes free text, and MeteoAlarm — the better geographic diversifier —
states terms "equivalent to CC BY 4.0 with additional requirements for
redistributing" whose text is behind a JavaScript page. An unresolved licence
is not a source; it stays an audit item, and the one whose terms are
unambiguous went first.
"""

from __future__ import annotations

import re

GDACS_URL = ("https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH"
             "?eventlist=EQ,TC,FL,DR,WF&alertlevel=Orange;Red")
NHC_URL = "https://www.nhc.noaa.gov/CurrentStorms.json"
# The floor is applied at the request, not after it: the preserved bytes are
# then exactly what the machine asked to see, and the query string is the
# committed record of the threshold. Without it the feed answers with every
# advisory the country is under — 259 alerts and 1.2 MB on the probe night of
# 2026-08-22, against 49 alerts and 332 KB with the floor.
NWS_URL = ("https://api.weather.gov/alerts/active"
           "?severity=Extreme,Severe&urgency=Immediate,Expected"
           "&certainty=Observed,Likely")
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


# What the floor keeps: a warning (VTEC significance W) that a US forecast
# office has issued for a declared window, at the top two of CAP's five
# severities, expected or already under way, and at least likely. What it
# drops: watches and advisories, "possible", and the three actions that
# announce an ending rather than a future.
NWS_SIGNIFICANCE = "W"
NWS_CLOSING_ACTIONS = frozenset({"CAN", "EXP", "UPG"})
# /O.NEW.KOUN.FF.W.0085.260822T1524Z-260822T1530Z/ — action, office,
# phenomenon, significance, event tracking number, then the window. The ETN
# recycles every calendar year per office, so the year of the window belongs
# in the key or two different events a year apart would collide.
VTEC = re.compile(
    r"^/[A-Z]\.([A-Z]{3})\.([A-Z]{4})\.([A-Z]{2})\.([A-Z])\.(\d{4})\."
    r"(\d{6}|000000)T\d{4}Z-(\d{6})T\d{4}Z/$")


def vtec_id(vtec: str) -> str | None:
    """The stable identity of one warning across all its updates.

    CAP gives every message its own identifier, so a warning that is extended
    four times arrives as five identifiers referencing each other. Keyed that
    way the register would notarize five futures where the office issued one.
    The VTEC event tracking number is the office's own answer to that, so the
    register uses it and follows the event instead of the message.
    """
    match = VTEC.match(vtec.strip())
    if not match:
        return None
    action, office, phenomenon, significance, etn, begins, ends = match.groups()
    if significance != NWS_SIGNIFICANCE or action in NWS_CLOSING_ACTIONS:
        return None
    year = (begins if begins != "000000" else ends)[:2]
    return (f"nws-{office.lower()}-{phenomenon.lower()}"
            f"{significance.lower()}-{etn}-{year}")


def _nws_hazard(event: str) -> str:
    """The issuer's own event name, minus the product word — not a taxonomy of
    ours. GDACS gets a controlled vocabulary because its codes are five; the
    weather service issues over a hundred products and inventing a mapping
    would be us deciding what a Red Flag Warning is about."""
    name = (event or "").strip()
    for suffix in (" Warning", " Watch", " Advisory", " Statement"):
        if name.endswith(suffix):
            return name[: -len(suffix)].lower()
    return name.lower()


def nws_futures(parsed: dict) -> list[dict]:
    """Map NWS CAP alerts to announced-future records (kind ALERT_EPISODE).

    Named limit, so it is not a silent one: severity here is CAP's ladder
    (Extreme/Severe), not GDACS's Orange/Red. An upgrade from Severe to
    Extreme appears in the resolution's severity path and counts as an
    escalation; the two ladders are never mixed into one scale.
    """
    futures = []
    seen: set[str] = set()
    for feature in parsed.get("features", []):
        p = feature.get("properties") or {}
        codes = (p.get("parameters") or {}).get("VTEC") or []
        window_from = p.get("onset") or p.get("effective")
        window_to = p.get("ends") or p.get("expires")
        for code in codes:
            if not isinstance(code, str):
                continue
            fid = vtec_id(code)
            # One alert can carry several VTEC strings, and the same event
            # arrives again as its own update: first message wins, so
            # announced_at stays this practice's first sight of the warning.
            if not fid or fid in seen:
                continue
            seen.add(fid)
            futures.append({
                "id": fid,
                "kind": "ALERT_EPISODE",
                "source": "NWS",
                "hazard": _nws_hazard(str(p.get("event") or "")),
                "what": str(p.get("event") or "").strip(),
                "where": str(p.get("areaDesc") or "").strip(),
                # The alerts are issued for United States territory; the
                # country is the feed's premise, not an inference of ours.
                "iso3": ["USA"],
                "severity": str(p.get("severity") or ""),
                "window": {"from": _clean_date(window_from),
                           "to": _clean_date(window_to)},
                "source_ref": str(p.get("@id") or ""),
            })
    return futures
