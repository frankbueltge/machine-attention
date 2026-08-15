"""Memory Hole V0 — the nightly reading: the institutional wording, rechecked.

Seven steps for the completed UTC day, exactly as the audit's §6 sketch has
them, built on the practice substrate rather than beside it:

  1. discover, in domain scope — one proven CDX query per institution, the
     answer preserved as bytes with its manifest;
  2. gate every capture before it is allowed to mean anything (`validity`);
  3. diff deterministically (`textdiff` -> `prose` -> `salience`);
  4. type the events by versioned rules (`events`), model layer only where the
     rules abstain (`model`);
  5. recheck every deletion candidate live (`recheck`) before the word "gone"
     appears anywhere;
  6. write the record — including the empty night, which is a measurement
     (audit finding 5: the archive crawls these pages weekly to never);
  7. `verify.py::check_memoryhole` recomputes all of it from the preserved
     bytes.

What this run does NOT do, and says so: it does not call a night's silence a
finding, does not fetch a page the archive has not seen, does not name a
person, and does not publish anything at all — no stage, no site, no public
presence before a passed E-experiment.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .. import autonomy
from ..fetch import Client, SourceUnavailable
from ..preserve import Snapshot, utc_now, write_json
from . import cdx, events as events_mod, extract, model, recheck, textdiff
from . import validity, watchlist

SNAPSHOT_BASE = "memoryhole/snapshots"
READINGS = "memoryhole/readings"

# Pages sampled per institution from the day's discovered URLs. The sample is
# deterministic (watchlist.rank) so the record can be recomputed, and small
# because every sampled page costs a slow CDX round trip: the audit measured
# 1.3-60 s per query and a 19 % 504 rate at concurrency 4.
SAMPLE_PER_INSTITUTION = 5
# Ceiling on snapshot pairs fetched in one night. Over it, pages are recorded
# as unverifiable with the reason `over_nightly_fetch_cap` — visible, not
# dropped.
MAX_CHANGED_PAGES = 40
# The substrate's ladder (30/60/120 s) was tuned for scarce JSON APIs. The
# archive is not scarce, it is slow and flaky; a shorter ladder keeps a night
# inside its budget. Substrate finding, recorded in the build report.
CDX_BACKOFF = (5.0, 15.0, 30.0)

NOTES = [
    "domain scope: many pages of few institutions, the architecture the audit "
    "made condition 1 — a longer curated list would be the origin with more "
    "rows and belongs in the origin",
    "the archive's cadence is the resolution: institutional pages are crawled "
    "weekly to never, so 'nightly' is the protocol frequency, not the "
    "observation frequency; a night without a finding is a measurement and is "
    "written",
    "a capture counts as a page only after the validity gate; challenge, "
    "consent and bot-wall pages are counted as unverifiable and never diffed",
    "'gone' is a live-rechecked assertion, never a CDX row; bot-walls, server "
    "errors and 451 stay out of the gone-rate denominator and are disclosed "
    "as counts",
    "event types name operations on text, never intent — 'commitment_removed' "
    "says a commitment verb left a sentence, nothing about why",
    "passages carrying an ascription to a person are recorded as digests, not "
    "as text: the name stays in the preserved bytes as evidence and never "
    "becomes the subject of the record",
    "model verdicts, when the layer runs, are estimates recorded beside the "
    "deterministic record and never inside it",
    "control pages (category E) carry no commitments; every event on one is a "
    "fault of the instrument by construction",
]


def readings_dir(repo_root: Path) -> Path:
    return repo_root / READINGS


def _method_versions() -> dict:
    return {
        "cdx": cdx.CDX_VERSION,
        "extract": extract.EXTRACT_VERSION,
        "gate": validity.GATE_VERSION,
        "textdiff": textdiff.TEXTDIFF_VERSION,
        "prose": "prose-v1",
        "salience": "salience-v1",
        "events": events_mod.EVENTS_VERSION,
        "recheck": recheck.RECHECK_VERSION,
        "model_layer": model.MODEL_LAYER_VERSION,
    }


def discover(client: Client, snap: Snapshot, entry: dict, day: str,
             failures: list[dict]) -> tuple[list[str], dict]:
    """One institution, one day. Returns the URLs the archive touched and the
    record of asking."""
    slug = entry["slug"]
    strategy = entry["strategy"]
    if strategy == "single_url":
        return list(entry.get("urls", [])), {
            "slug": slug, "category": entry["category"], "strategy": strategy,
            "urls_seen": len(entry.get("urls", [])), "source": None,
            "note": "single-URL fallback: the host answers no scope query"}

    url = cdx.discovery_url(entry["query"], strategy, day)
    try:
        data, status = client.fetch(url, headers={"Accept": "application/json"})
    except SourceUnavailable as err:
        failures.append({"scope": f"memoryhole:discovery:{slug}",
                         "error": str(err)})
        return [], {"slug": slug, "category": entry["category"],
                    "strategy": strategy, "urls_seen": 0, "source": None,
                    "error": str(err)}

    preserved = snap.preserve(f"discovery-{slug}.json", data,
                              cdx.redacted(url), status)
    if status != 200:
        failures.append({"scope": f"memoryhole:discovery:{slug}",
                         "error": f"HTTP {status}"})
        return [], {"slug": slug, "category": entry["category"],
                    "strategy": strategy, "urls_seen": 0,
                    "source": preserved["file"], "http_status": status,
                    "error": f"HTTP {status}"}

    urls = sorted({row.original for row in cdx.parse(data)})
    return urls, {"slug": slug, "category": entry["category"],
                  "strategy": strategy, "urls_seen": len(urls),
                  "source": preserved["file"], "http_status": status}


def sample(urls: list[str], day: str, excluded: set[str], size: int) -> list[str]:
    """A deterministic pseudo-random sample of the day's pages.

    Random, so the rates mean something; deterministic, so the verifier can
    redraw exactly the same sample from the preserved discovery bytes.
    """
    eligible = [u for u in urls if u not in excluded]
    eligible.sort(key=lambda u: watchlist.rank(day, u))
    return sorted(eligible[:size])


def _page_entry(url: str, institution: str, category: str, kind: str) -> dict:
    return {"id": watchlist.page_id(url), "url": url,
            "institution": institution, "category": category, "kind": kind}


def read_page(client: Client, snap: Snapshot, page: dict, day: str,
              budget: dict, failures: list[dict]) -> dict:
    """History, gate, diff, events — for one page."""
    pid = page["id"]
    url = cdx.history_url(page["url"])
    try:
        data, status = client.fetch(url, headers={"Accept": "application/json"})
    except SourceUnavailable as err:
        failures.append({"scope": f"memoryhole:history:{pid}", "error": str(err)})
        return {**page, "class": "unverifiable", "reason": "history_unavailable"}
    preserved = snap.preserve(f"history-{pid}.json", data, cdx.redacted(url),
                              status)
    page = {**page, "history": preserved["file"]}
    if status != 200:
        return {**page, "class": "unverifiable", "reason": f"cdx_http_{status}"}

    reading = cdx.classify(cdx.parse(data), day)
    if reading.kind == "unchanged":
        return {**page, "class": "unchanged", "reason": reading.reason}
    if reading.kind == "unverifiable":
        return {**page, "class": "unverifiable", "reason": reading.reason}
    if reading.kind == "deletion_candidate":
        return {**page, "class": "deletion_candidate", "reason": reading.reason,
                "archive_status": reading.after.statuscode if reading.after else None,
                "permalink": cdx.permalink(reading.after.timestamp, reading.after.original)
                if reading.after else None}

    # changed candidate: the two snapshots decide whether anything is sayable.
    if budget["fetched"] >= MAX_CHANGED_PAGES:
        budget["over_cap"] += 1
        return {**page, "class": "unverifiable", "reason": "over_nightly_fetch_cap"}
    budget["fetched"] += 1

    captures = {}
    texts = {}
    for side, row in (("before", reading.before), ("after", reading.after)):
        snapshot = cdx.snapshot_url(row.timestamp, row.original)
        try:
            body, http_status = client.fetch(
                snapshot, headers=recheck.HTML_HEADERS)
        except SourceUnavailable as err:
            failures.append({"scope": f"memoryhole:snapshot:{pid}:{side}",
                             "error": str(err)})
            return {**page, "class": "unverifiable",
                    "reason": f"snapshot_unavailable_{side}"}
        entry = snap.preserve(f"{side}-{pid}.html", body, snapshot, http_status)
        captures[side] = {"timestamp": row.timestamp, "digest": row.digest,
                          "archive_status": row.statuscode,
                          "http_status": http_status, "file": entry["file"],
                          "permalink": cdx.permalink(row.timestamp, row.original)}
        texts[side] = extract.text_of(body)

    gates = {side: validity.check(texts[side],
                                  captures[side]["archive_status"])
             for side in ("before", "after")}
    gate_block = {side: {"valid": v.valid, "reason": v.reason,
                         "tokens": v.tokens,
                         "prose_sentences": v.prose_sentences,
                         "markers": list(v.markers)}
                  for side, v in gates.items()}
    page = {**page, "captures": captures, "gate": gate_block}

    if not (gates["before"].valid and gates["after"].valid):
        failed = "before" if not gates["before"].valid else "after"
        return {**page, "class": "unverifiable",
                "reason": f"gate_{failed}_{gates[failed].reason}"}

    diff = textdiff.diff(texts["before"], texts["after"])
    found, abstentions = events_mod.classify(diff)
    return {
        **page,
        "class": "changed",
        "reason": "new digest, both captures passed the gate",
        "removed_tokens": diff.removed_tokens,
        "added_sentences": len(diff.added),
        "rewritten_pairs": len(diff.pairs),
        "events": [_event_json(e) for e in found],
        "abstentions": [_abstention_json(a) for a in abstentions],
    }


def _event_json(event: events_mod.Event) -> dict:
    out = {"type": event.type, "rule": event.rule,
           "before_sha256": event.before_sha256,
           "salience": event.salience, "signals": list(event.signals)}
    if event.after_sha256:
        out["after_sha256"] = event.after_sha256
    if event.before is not None:
        out["before"] = event.before
    if event.after is not None:
        out["after"] = event.after
    if event.before is None:
        out["withheld"] = "passage carries an ascription to a person (I8)"
    return out


def _abstention_json(item: events_mod.Abstention) -> dict:
    out = {"before_sha256": item.before_sha256, "salience": item.salience,
           "signals": list(item.signals)}
    if item.before is not None:
        out["before"] = item.before
    if item.after is not None:
        out["after"] = item.after
    return out


def rates(entries: list[dict], deletion: dict) -> dict:
    counts = {"unchanged": 0, "changed": 0, "unverifiable": 0, "gone": 0}
    for entry in entries:
        counts[entry["class"]] = counts.get(entry["class"], 0) + 1
    examined = sum(counts.values())
    decided = counts["unchanged"] + counts["changed"]
    changed_lo, changed_hi = recheck.wilson(counts["changed"], decided)
    unver_lo, unver_hi = recheck.wilson(counts["unverifiable"], examined)
    reasons: dict[str, int] = {}
    for entry in entries:
        if entry["class"] == "unverifiable":
            reasons[entry["reason"]] = reasons.get(entry["reason"], 0) + 1
    return {
        "examined": examined,
        "counts": counts,
        "decided": decided,
        "changed_rate": round(counts["changed"] / decided, 4) if decided else None,
        "changed_ci95": [round(changed_lo, 4), round(changed_hi, 4)] if decided else None,
        "unverifiable_rate": round(counts["unverifiable"] / examined, 4) if examined else None,
        "unverifiable_ci95": [round(unver_lo, 4), round(unver_hi, 4)] if examined else None,
        "unverifiable_reasons": dict(sorted(reasons.items())),
        "deletion": deletion,
    }


def run(repo_root: Path, day: str, client: Client | None = None,
        live_client: Client | None = None, model_key: str | None = None) -> dict:
    client = client or Client(backoff=CDX_BACKOFF)
    live_client = live_client or client
    reading_path = readings_dir(repo_root) / f"{day}.json"
    if reading_path.exists():
        raise SystemExit(f"memoryhole reading for {day} exists; "
                         "records are append-only (I3)")

    doc = watchlist.load(repo_root)
    excluded = watchlist.excluded_urls(doc)
    failures: list[dict] = []
    snap = Snapshot(repo_root, day, base=SNAPSHOT_BASE)

    institutions: list[dict] = []
    pages: list[dict] = []
    for entry in doc["institutions"]:
        urls, record = discover(client, snap, entry, day, failures)
        drawn = sample(urls, day, excluded, SAMPLE_PER_INSTITUTION)
        record["sampled"] = len(drawn)
        institutions.append(record)
        pages.extend(_page_entry(url, entry["slug"], entry["category"],
                                 "sampled") for url in drawn)

    control_urls = {c["url"] for c in doc["controls"]}
    pages = [p for p in pages if p["url"] not in control_urls]
    pages.extend(_page_entry(c["url"], c.get("institution", "control"), "E",
                             "control") for c in doc["controls"])

    budget = {"fetched": 0, "over_cap": 0}
    entries = [read_page(client, snap, page, day, budget, failures)
               for page in pages]

    # Deletion candidates: nothing is called gone before the live look.
    candidates = [e for e in entries if e["class"] == "deletion_candidate"]
    classes: list[str] = []
    for entry in candidates:
        result = recheck.check(live_client, entry["url"])
        entry["recheck"] = result
        classes.append(result["class"])
        if result["class"] in recheck.GONE:
            entry["class"] = "gone"
            entry["reason"] = f"live {result['http_code']}"
        else:
            entry["class"] = "unverifiable"
            entry["reason"] = f"deletion_candidate_survived_recheck_{result['class']}"
    deletion = recheck.summarize(classes)

    abstentions = sorted(
        (a for e in entries for a in e.get("abstentions", [])),
        key=lambda a: (-a["salience"], a["before_sha256"]))
    model_block = model.classify(abstentions, key=model_key)

    snap.write_manifest()

    reading = {
        "date": day,
        "generated_at": utc_now(),
        "watchlist_version": doc["version"],
        "method_versions": _method_versions(),
        "sampling": {"per_institution": SAMPLE_PER_INSTITUTION,
                     "rank": "sha256(day|url), ascending",
                     "fetch_cap": MAX_CHANGED_PAGES,
                     "pairs_fetched": budget["fetched"],
                     "over_fetch_cap": budget["over_cap"]},
        "institutions": institutions,
        "entries": entries,
        "rates": rates(entries, deletion),
        "model": model_block,
        "failures": failures,
        "notes": NOTES,
    }
    write_json(reading_path, reading)

    counts = reading["rates"]["counts"]
    autonomy.append(repo_root, "memoryhole-run", "machine",
                    model=model_block.get("model") if model_block.get("available") and model_block.get("state") == "on" else None,
                    tokens=(model_block["usage"]["input_tokens"]
                            + model_block["usage"]["output_tokens"]),
                    cost=model_block["cost_usd"], currency="USD",
                    detail={"date": day, "requests": client.requests,
                            "institutions": len(institutions),
                            "examined": reading["rates"]["examined"],
                            "changed": counts["changed"],
                            "unverifiable": counts["unverifiable"],
                            "gone": counts["gone"],
                            "events": sum(len(e.get("events", []))
                                          for e in entries),
                            "model": model_block["state"],
                            "failures": len(failures)})
    return {"date": day, "counts": counts,
            "events": sum(len(e.get("events", [])) for e in entries),
            "model": model_block["state"], "failures": failures}


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Run the nightly Memory Hole reading.")
    parser.add_argument("--repo-root", default=".", type=Path)
    yesterday = (datetime.now(timezone.utc).date()
                 - timedelta(days=1)).isoformat()
    parser.add_argument("--date", default=yesterday,
                        help="UTC day to read (default: yesterday — the last "
                             "completed day)")
    args = parser.parse_args(argv)
    summary = run(args.repo_root.resolve(), args.date)
    counts = summary["counts"]
    print(f"memoryhole {summary['date']}: {counts['unchanged']} unchanged, "
          f"{counts['changed']} changed, {counts['unverifiable']} unverifiable, "
          f"{counts['gone']} gone, {summary['events']} typed event(s), "
          f"model {summary['model']}, {len(summary['failures'])} failure(s)")
    for failure in summary["failures"]:
        print(f"  - {failure['scope']}: {failure['error']}")


if __name__ == "__main__":
    main()
