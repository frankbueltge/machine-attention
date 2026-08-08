"""The reaction axis: what moved in the time a warning was already running.

This implements the machine's own proposal `sensor-fts-country-coverage`
(foreknown/proposals/, discovery pass of 2026-08-08). The machine wrote that
sensor before any human had built this axis: a mechanical membership check
between two committed registers — the open alert episodes and OCHA's 2026
response plans — with an explicit refusal to judge funding adequacy. The
proposal's definition, test rule and thresholds are followed as written; the
money and attention figures below are the extension around it.

Two series per announced future, both derived from committed bytes only:

- money — which OCHA/FTS 2026 response plans list the warning's countries,
  what those plans ask for, and what FTS reports as funded. Plan totals are
  the plans' own annual figures for every country they cover; they are NOT
  attributable to the hazard. No adequacy, need or blame verdict is made.
- attention — how much of the world's recorded news volume fell on the
  warning's countries that day, against those countries' own recent median.
  See attention.py for what that number is and is not.

The series are recomputed backwards from the preserved bytes, so a night's
reading is a claim any reader can redo: verify.py does exactly that.
"""

from __future__ import annotations

import argparse
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from ..fetch import Client, SourceUnavailable
from ..preserve import Snapshot, read_json, sha256, utc_now, write_json
from . import attention

# FTS's own year-wide grouping; one request instead of one per plan.
FTS_FUNDING_URL = "https://api.hpc.tools/v1/public/fts/flow?year=2026&groupby=plan"
SNAPSHOT_BASE = "foreknown/reaction/snapshots"

BASELINE_DAYS = 28
# The proposal refuses to set firing thresholds before three nights of
# baseline exist. Kept as the machine wrote it; the sensor arms itself.
BASELINE_NIGHTS_REQUIRED = 3
LOW_MATCH_RATE = 0.25
HIGH_MATCH_RATE = 0.50
MATCH_RATE_JUMP = 0.10

NOTES = [
    "plan requirements and funding are the plans' own annual figures for "
    "every country they list — not attributable to this hazard, and not a "
    "statement about adequacy, need or responsibility",
    "attention counts sum GDELT article mentions across events located in "
    "the country: a volume proxy, not distinct articles",
    "attention is measured for the country, not for the hazard — a country's "
    "news volume moves for many reasons at once, and this axis cannot tell "
    "them apart",
    "a country with no matching plan is a fact about two registers, not a "
    "finding about the world",
]


# --- the two committed registers ------------------------------------------

def plans_index(plans_doc: dict) -> dict[int, dict]:
    """plan id -> name, iso3 coverage and requirements, from the plan list."""
    index: dict[int, dict] = {}
    for plan in plans_doc.get("data", []):
        pid = plan.get("id")
        if pid is None:
            continue
        index[pid] = {
            "name": (plan.get("planVersion") or {}).get("name", ""),
            "iso3": sorted({loc.get("iso3") for loc in plan.get("locations", [])
                            if isinstance(loc, dict) and loc.get("iso3")}),
            "requirements_usd": plan.get("revisedRequirements")
            or plan.get("origRequirements") or 0,
        }
    return index


def funding_index(funding_doc: dict) -> dict[int, int]:
    """plan id -> funding FTS reports for 2026.

    report3 is FTS's destination-side grouping. Checked against the per-plan
    query on 2026-08-08: planid=1498 gives 84,257,438 in both, while report2
    gives 82,346,102 — report3 is the one that matches what FTS publishes.
    """
    report = (funding_doc.get("data") or {}).get("report3") or {}
    out: dict[int, int] = {}
    for obj in report.get("fundingTotals", {}).get("objects", []):
        for entry in obj.get("singleFundingObjects", []):
            pid = entry.get("id")
            if pid is not None:
                out[pid] = entry.get("totalFunding") or 0
    return out


def load_crosswalk(repo_root: Path) -> dict[str, str]:
    """iso3 -> FIPS 10-4, the committed crosswalk record (hand-authored,
    checked against GDELT's own code list; see the record's own notes)."""
    doc = read_json(repo_root / "foreknown" / "reaction" / "iso3-fips.json",
                    {"entries": {}})
    return {iso3: entry["fips"] for iso3, entry in doc["entries"].items()}


def load_attention_days(repo_root: Path) -> dict[str, dict]:
    directory = repo_root / "foreknown" / "reaction" / "attention"
    if not directory.exists():
        return {}
    return {path.stem: read_json(path) for path in sorted(directory.glob("*.json"))}


def readings_dir(repo_root: Path) -> Path:
    return repo_root / "foreknown" / "reaction" / "readings"


# --- the reading ----------------------------------------------------------

def baseline_window(attention_days: dict[str, dict], day: str) -> list[str]:
    """The committed days the median is taken over — written into the reading
    so the number stays recomputable even after older days are backfilled."""
    return [d for d in sorted(attention_days) if d < day][-BASELINE_DAYS:]


def attention_entry(fips: list[str], attention_days: dict[str, dict],
                    day: str, window: list[str]) -> dict | None:
    if not fips or day not in attention_days:
        return None
    today = attention_days[day]
    articles = attention.articles_for(today, fips)
    world = today.get("world", {}).get("articles", 0)
    baseline = attention.median([float(attention.articles_for(
        attention_days[d], fips)) for d in window if d in attention_days])
    return {
        "articles": articles,
        "share_per_10k": round(articles / world * 10_000, 1) if world else None,
        "baseline_median_articles": baseline,
        "ratio_to_baseline": round(articles / baseline, 2) if baseline else None,
    }


def _sensor_state(match_rate: float, nights: int,
                  prior: dict | None) -> dict:
    """The machine's proposal, applied as written: no firing before three
    nights of baseline, then the thresholds it named."""
    state = {
        "name": "fts-country-coverage",
        "proposal": "foreknown/proposals/sensor-fts-country-coverage.json",
        "nights_recorded": nights,
        "fired": False,
    }
    if nights < BASELINE_NIGHTS_REQUIRED:
        state["firing"] = "DEFERRED"
        state["why"] = (f"the proposal sets no threshold before "
                        f"{BASELINE_NIGHTS_REQUIRED} nights of baseline; "
                        f"night {nights} of {BASELINE_NIGHTS_REQUIRED}")
        return state
    state["firing"] = "ARMED"
    reasons = []
    if match_rate < LOW_MATCH_RATE:
        reasons.append(f"match rate {match_rate:.0%} below "
                       f"{LOW_MATCH_RATE:.0%}")
    if match_rate > HIGH_MATCH_RATE:
        reasons.append(f"match rate {match_rate:.0%} above "
                       f"{HIGH_MATCH_RATE:.0%}")
    prior_rate = (prior or {}).get("coverage", {}).get("match_rate")
    if prior_rate is not None and abs(match_rate - prior_rate) > MATCH_RATE_JUMP:
        reasons.append(f"match rate moved {abs(match_rate - prior_rate):.0%} "
                       f"from the previous reading")
    state["fired"] = bool(reasons)
    state["why"] = "; ".join(reasons) or "inside the proposal's thresholds"
    return state


def build_reading(day: str, registry: dict, plans_doc: dict, funding_doc: dict,
                  crosswalk: dict[str, str], attention_days: dict[str, dict],
                  refs: dict, prior: dict | None = None,
                  nights: int = 1) -> dict:
    plans = plans_index(plans_doc)
    funding = funding_index(funding_doc)
    plan_iso3 = {pid: set(plan["iso3"]) for pid, plan in plans.items()}
    attention_day = max(attention_days) if attention_days else None
    window = baseline_window(attention_days, attention_day) if attention_day else []

    entries: dict[str, dict] = {}
    matched_episodes = 0
    open_episodes = 0
    for fid, future in sorted(registry.get("futures", {}).items()):
        if future.get("status") != "OPEN":
            continue
        iso3 = sorted(future.get("iso3") or [])
        matching = sorted(pid for pid, codes in plan_iso3.items()
                          if codes & set(iso3))
        has_match = bool(matching)
        if future.get("kind") == "ALERT_EPISODE":
            open_episodes += 1
            matched_episodes += int(has_match)
        fips = sorted({crosswalk[code] for code in iso3 if code in crosswalk})
        entries[fid] = {
            "iso3": iso3,
            "fips": fips,
            "unmapped_iso3": [code for code in iso3 if code not in crosswalk],
            # Field names say whose numbers these are: the plans'. A plan
            # listing one of the warning's countries brings its whole annual
            # appeal with it — for a 28-country drought that is most of a
            # continent's humanitarian budget, and none of it was raised for
            # this hazard.
            "money": {
                "has_fts_plan_match": has_match,
                "plans": matching,
                "plan_requirements_usd": sum(plans[pid]["requirements_usd"]
                                             for pid in matching),
                "plan_funded_usd": sum(funding.get(pid, 0) for pid in matching),
            },
            "attention": attention_entry(fips, attention_days, attention_day,
                                         window) if attention_day else None,
        }

    match_rate = round(matched_episodes / open_episodes, 4) if open_episodes else 0.0
    return {
        "date": day,
        "generated_at": utc_now(),
        "attention_day": attention_day,
        "attention_baseline_window": window,
        "attention_days_committed": len(attention_days),
        "sources": refs,
        "coverage": {
            "open_alert_episodes": open_episodes,
            "with_fts_plan_match": matched_episodes,
            "match_rate": match_rate,
        },
        "sensor": _sensor_state(match_rate, nights, prior),
        "notes": NOTES,
        "futures": entries,
    }


# --- the nightly reaction run ---------------------------------------------

def _preserve_once(snap: Snapshot, name: str, data: bytes, url: str,
                   status: int) -> str:
    """Preserve unless these exact bytes are already in tonight's manifest."""
    digest = sha256(data)
    for entry in snap.entries:
        if entry["file"].endswith(f"/{name}") and entry["sha256"] == digest:
            return entry["file"]
    return snap.preserve(name, data, url, status)["file"]


def latest_plans_snapshot(repo_root: Path) -> str | None:
    """The newest plan list the notary preserved — the reaction axis reads
    the notary's bytes rather than fetching the same document twice."""
    candidates = sorted(repo_root.glob("foreknown/snapshots/*/fts-plans-2026.json"))
    return candidates[-1].relative_to(repo_root).as_posix() if candidates else None


def run_reaction(repo_root: Path, day: str, registry: dict,
                 client: Client | None = None, backfill: int = 0) -> dict:
    """Preserve today's money bytes, extend the attention series, write the
    reading. Every source outage is returned, never silently bridged."""
    client = client or Client()
    reading_path = readings_dir(repo_root) / f"{day}.json"
    if reading_path.exists():
        raise SystemExit(f"reaction reading for {day} exists; records are "
                         "append-only (I3)")

    failures: list[dict] = []
    snap = Snapshot(repo_root, day, base=SNAPSHOT_BASE)
    refs: dict = {}

    plans_ref = latest_plans_snapshot(repo_root)
    if plans_ref:
        refs["FTS-plans"] = plans_ref
    else:
        failures.append({"scope": "reaction:FTS-plans",
                         "error": "no preserved plan list in the archive"})

    for label, url, filename in (
            ("FTS-funding", FTS_FUNDING_URL, "fts-funding-2026.json"),
            ("GDELT-fips", attention.FIPS_LOOKUP_URL, "fips-country.txt")):
        try:
            data, status = client.fetch(url)
        except SourceUnavailable as err:
            failures.append({"scope": f"reaction:{label}", "error": str(err)})
            continue
        if status != 200:
            failures.append({"scope": f"reaction:{label}",
                             "error": f"HTTP {status}"})
            continue
        refs[label] = _preserve_once(snap, filename, data, url, status)

    # The attention series: every missing day between backfill and yesterday.
    # GDELT publishes a day's file the following morning, so the most recent
    # day is routinely absent — an absence, not a failure.
    committed = load_attention_days(repo_root)
    fetched = 0
    for target in attention.days_before(day, backfill):
        if target in committed:
            continue
        url = attention.day_url(target)
        try:
            data, status = client.fetch(url)
        except SourceUnavailable as err:
            failures.append({"scope": f"attention:{target}", "error": str(err)})
            continue
        if status == 404:
            failures.append({"scope": f"attention:{target}",
                             "error": "not published yet"})
            continue
        if status != 200:
            failures.append({"scope": f"attention:{target}",
                             "error": f"HTTP {status}"})
            continue
        try:
            committed[target] = attention.write_day(repo_root, target, data, url)
        except (zipfile.BadZipFile, IndexError) as err:
            failures.append({"scope": f"attention:{target}",
                             "error": err.__class__.__name__})
            continue
        fetched += 1

    snap.write_manifest()

    plans_doc = read_json(repo_root / refs["FTS-plans"], {}) \
        if "FTS-plans" in refs else {}
    funding_doc = read_json(repo_root / refs["FTS-funding"], {}) \
        if "FTS-funding" in refs else {}
    prior_readings = sorted(readings_dir(repo_root).glob("*.json")) \
        if readings_dir(repo_root).exists() else []
    prior = read_json(prior_readings[-1]) if prior_readings else None

    reading = build_reading(day, registry, plans_doc, funding_doc,
                            load_crosswalk(repo_root), committed, refs,
                            prior=prior, nights=len(prior_readings) + 1)
    reading["failures"] = failures
    write_json(reading_path, reading)
    return {"attention_days_fetched": fetched,
            "attention_days_committed": len(committed),
            "match_rate": reading["coverage"]["match_rate"],
            "failures": failures}


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Run the reaction axis.")
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--date",
                        default=datetime.now(timezone.utc).date().isoformat())
    parser.add_argument("--backfill", type=int, default=3,
                        help="how many past UTC days of attention to complete")
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    registry = read_json(root / "foreknown" / "registry.json", {"futures": {}})
    summary = run_reaction(root, args.date, registry, backfill=args.backfill)
    print(f"reaction {args.date}: "
          f"{summary['attention_days_fetched']} attention day(s) added, "
          f"{summary['attention_days_committed']} committed, "
          f"plan match rate {summary['match_rate']:.0%}, "
          f"{len(summary['failures'])} failure(s)")
    for failure in summary["failures"]:
        print(f"  - {failure['scope']}: {failure['error']}")


if __name__ == "__main__":
    main()
