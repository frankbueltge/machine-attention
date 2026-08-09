#!/usr/bin/env python3
"""Build the practice stage deterministically from committed records.

V2 (2026-08-08, after Frank's ten-second test): the first screen must be
understood by a first-time visitor in ten seconds — one plain sentence, one
real phenomenon (the next-expiring warning, ticking), one action. House
vocabulary ("practice", "notarized", "announced futures") appears only after
the plain words, never instead of them.

V3 (2026-08-08, late UTC): the work gains its depths. The stage stays
ATTRACT; below it, three more levels, all static, all derived from the same
committed records: ENTER (future/<id>.html — one dossier per announced
future, its whole life with evidence anchors), INVESTIGATE (ledger.html —
the full register, the nights, and what the machine itself has noticed) and
VERIFY (verify.html — where the claims meet the bytes). Depth on demand:
evidence is infinite, attention is not.

Every figure is a real system state; clocks tick client-side from data
timestamps so the build stays byte-stable for identical data (verify.py
rebuilds and compares — which also makes "no dead ends" testable).
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path

REPO_URL = "https://github.com/frankbueltge/machine-attention"
METHOD_URL = "https://frankbueltge.de/werke/attention"


def read_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def _short(text: str, limit: int = 64) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _gh(path: str) -> str:
    return f"{REPO_URL}/blob/main/{path}"


def _when(ts: str) -> str:
    return (ts or "")[:16].replace("T", " ")


def collect(root: Path) -> dict:
    registry = read_json(root / "foreknown" / "registry.json", {"futures": {}})
    runs = [read_json(p) for p in sorted(root.glob("foreknown/snapshots/*/run.json"))]
    manifests = [read_json(p) for p in
                 sorted(root.glob("foreknown/snapshots/*/manifest.json"))]
    reaction_manifests = [read_json(p) for p in
                          sorted(root.glob("foreknown/reaction/snapshots/*/manifest.json"))]
    first_byte = min((e["retrieved_at"] for m in manifests
                      for e in m.get("entries", [])), default=None)
    futures = registry["futures"]
    open_futures = sorted((f for f in futures.values() if f["status"] == "OPEN"),
                          key=lambda f: (f.get("window", {}).get("to") or "9999",
                                         f["id"]))
    resolutions = {r["future"]: r for r in
                   (read_json(p)
                    for p in sorted(root.glob("foreknown/resolutions/*.json")))
                   if r.get("future")}
    event_pairs = [(h, f) for f in futures.values() for h in f["history"]]
    event_pairs += [({"ts": r["resolved_at"], "event": f"RESOLVED_{r['verdict']}"},
                     futures[r["future"]])
                    for r in resolutions.values() if r.get("future") in futures]
    events = sorted(event_pairs, key=lambda pair: pair[0]["ts"],
                    reverse=True)[:12]

    reading_paths = sorted(root.glob("foreknown/reaction/readings/*.json"))
    reading = read_json(reading_paths[-1]) if reading_paths else None
    plans_meta, funded = _plan_maps(root, reading)
    attention_days = [read_json(p) for p in
                      sorted(root.glob("foreknown/reaction/attention/*.json"))]

    proposals = [read_json(p) for p in
                 sorted(root.glob("foreknown/proposals/*.json"))]
    observations = [p for p in proposals
                    if p and p.get("kind") == "difference_observation"]
    sensors = [p for p in proposals if p and p.get("test_rule")]
    crosswalk = read_json(root / "foreknown" / "reaction" / "iso3-fips.json")

    return {"registry": registry, "runs": runs, "first_byte": first_byte,
            "open": open_futures, "events": events,
            "resolutions": resolutions, "resolved": len(resolutions),
            "total": len(futures),
            "reading": reading, "plans_meta": plans_meta, "funded": funded,
            "attention_days": attention_days,
            "observations": observations, "sensors": sensors,
            "crosswalk": crosswalk,
            "manifests": manifests, "reaction_manifests": reaction_manifests,
            "run_date": runs[-1]["date"] if runs else "",
            "first_run_date": runs[0]["date"] if runs else ""}


def _plan_maps(root: Path, reading: dict | None) -> tuple[dict, dict]:
    """Plan names/requirements and funding, from the reading's own sources —
    the dossiers cite the same bytes the reading was computed from."""
    plans: dict[int, dict] = {}
    funded: dict[int, int] = {}
    sources = (reading or {}).get("sources", {})
    plans_path = root / sources.get("FTS-plans", "__none__")
    if plans_path.exists():
        for plan in (read_json(plans_path) or {}).get("data", []):
            pid = plan.get("id")
            if pid is None:
                continue
            plans[pid] = {
                "name": (plan.get("planVersion") or {}).get("name", f"plan {pid}"),
                "requirements": plan.get("revisedRequirements")
                or plan.get("origRequirements") or 0,
            }
    funding_path = root / sources.get("FTS-funding", "__none__")
    if funding_path.exists():
        report = ((read_json(funding_path) or {}).get("data")
                  or {}).get("report3") or {}
        for obj in report.get("fundingTotals", {}).get("objects", []):
            for entry in obj.get("singleFundingObjects", []):
                if entry.get("id") is not None:
                    funded[entry["id"]] = entry.get("totalFunding") or 0
    return plans, funded


def _usd(value: int) -> str:
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}bn"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.0f}m"
    return f"${value:,}"


def _clock(future: dict) -> str:
    window = future.get("window") or {}
    to, frm = window.get("to"), window.get("from")
    if to:
        return f'<span class="clock" data-to="{esc(to)}">—</span>'
    if frm:
        return f'<span class="clock" data-from="{esc(frm)}">—</span>'
    return ""


def reaction_line(reading: dict | None, future_id: str) -> str:
    """One sentence on what moved while this warning ran — attention first,
    then money. Deliberately not a dashboard: the deep figures live in
    foreknown/reaction/, this is the one line that fits the ten seconds.

    Money is named as the plans' annual figures ("requested for 2026"), never
    as money for this hazard: the plans list the country, not the warning.
    """
    entry = (reading or {}).get("futures", {}).get(future_id)
    if not entry:
        return ""
    parts = []
    attention = entry.get("attention")
    if attention and attention.get("articles"):
        sentence = (f"the world published <strong>{attention['articles']:,}</strong> "
                    f"news mentions from these countries on "
                    f"{esc(reading.get('attention_day', ''))}")
        ratio = attention.get("ratio_to_baseline")
        if ratio:
            sentence += f" — {ratio:.1f}&#215; their 28-day normal"
        parts.append(sentence)
    money = entry.get("money", {})
    if money.get("has_fts_plan_match"):
        count = len(money["plans"])
        parts.append(
            f"{count} UN humanitarian plan{'s' if count != 1 else ''} "
            f"list{'' if count != 1 else 's'} these countries: "
            f"{_usd(money['plan_requirements_usd'])} requested for 2026, "
            f"{_usd(money['plan_funded_usd'])} recorded as funded")
    elif money:
        parts.append("no UN humanitarian plan for 2026 lists these countries")
    if not parts:
        return ""
    sentences = [f"Meanwhile, {parts[0]}."]
    sentences += [f"{clause[0].upper()}{clause[1:]}." for clause in parts[1:]]
    return f'<p class="featured-reaction">{" ".join(sentences)}</p>'


# --- the deeper levels ------------------------------------------------------

EVENT_WORDS = {
    "NOTARIZED": "first seen — the machine preserved the original bytes and "
                 "fixed the announcement time; it never changes again",
    "REAPPEARED": "reappeared in its feed after having closed — itself a "
                  "difference worth the record",
    "CLOSED_BY_SOURCE": "the source let go of this warning",
    "CORRECTED": "the machine corrected its own record — the source said "
                 "nothing new",
    "DISSIPATED": "the forecast dissipated from its feed",
}

VERDICT_LEADS = {
    "EPISODE_ENDED": "The episode ended; its source let go of it.",
    "MATERIALIZED_AS_ALERT": "The forecast materialized: this registry holds "
                             "an alert-grade episode for the same storm.",
    "NO_ALERT_MATCH": "No alert-grade episode for this storm exists in this "
                      "registry — a statement about the record, not about "
                      "the world.",
}


def _correction_words(event: dict) -> str:
    """A CORRECTED event is the register admitting its own error. It reads as
    the machine's mistake, never as news from the feed."""
    iso3 = (event.get("corrections") or {}).get("iso3") or {}
    added = sorted(set(iso3.get("to") or []) - set(iso3.get("from") or []))
    if not added:
        return esc(event.get("cause", EVENT_WORDS["CORRECTED"]))
    return ("the machine corrected its own record: the country list gained "
            + esc(", ".join(added))
            + " — the feed had named it all along, this register had not")


def _revision_words(changes: dict) -> str:
    parts = []
    for field in ("severity", "window", "what", "where"):
        if field not in changes:
            continue
        change = changes[field]
        if field == "window":
            old, new = change.get("from") or {}, change.get("to") or {}
            if old.get("to") != new.get("to"):
                parts.append(f"window end {old.get('to') or '—'} "
                             f"&rarr; {new.get('to') or '—'}")
            if old.get("from") != new.get("from"):
                parts.append(f"window start {old.get('from') or '—'} "
                             f"&rarr; {new.get('from') or '—'}")
        elif field == "severity":
            parts.append(f"alert level {esc(change.get('from'))} "
                         f"&rarr; {esc(change.get('to'))}")
        else:
            parts.append(f"{field} restated: "
                         f"&#8220;{esc(_short(str(change.get('to') or ''), 60))}&#8221;")
    return "revised — " + "; ".join(parts) if parts else "revised"


def _window_to_at_notarization(future: dict) -> str | None:
    for event in future.get("history", []):
        change = (event.get("changes") or {}).get("window")
        if change:
            return (change.get("from") or {}).get("to")
    return (future.get("window") or {}).get("to")


def _overdue_state(future: dict, run_date: str) -> str | None:
    """Deterministic against the last committed run date, never wall clock."""
    to = (future.get("window") or {}).get("to")
    if future["status"] != "OPEN" or not to or to[:10] >= run_date:
        return None
    first_to = _window_to_at_notarization(future)
    announced = future.get("announced_at") or ""
    if first_to and announced and first_to[:19] < announced[:19]:
        return "cold_start"
    return "drift"


def _shell(title: str, description: str, body: str, depth: int = 0) -> str:
    rel = "../" * depth
    nav = "".join(
        f'<a class="enter" href="{href}">{label} &rarr;</a>'
        for label, href in (("Stage", f"{rel}index.html"),
                            ("Ledger", f"{rel}ledger.html"),
                            ("Verify", f"{rel}verify.html"),
                            ("Method", METHOD_URL),
                            ("Archive", REPO_URL)))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="stylesheet" href="{rel}style.css">
</head>
<body>
<div class="stage doc">
  <header>
    <span>The Foreknown — a machine records the world&#8217;s warnings</span>
    <span>every figure on this page is real</span>
  </header>
  <a class="crumb" href="{rel}index.html">&larr; the stage</a>
{body}
  <footer>
    <p class="state-line">Every statement above is derived from committed
    records; the archive is public and the whole chain can be re-run.</p>
    <nav class="enter-nav">{nav}</nav>
  </footer>
</div>
<script src="{rel}stage.js"></script>
</body>
</html>
"""


def _evidence_links(paths) -> str:
    return "".join(
        f'<span class="evidence">evidence: <a href="{_gh(esc(p))}">{esc(p)}</a></span>'
        for p in paths)


def _dossier_reaction(entry: dict | None, reading: dict | None,
                      plans_meta: dict, funded: dict) -> str:
    if not entry or not reading:
        return ""
    rows = []
    attention = entry.get("attention")
    day = reading.get("attention_day")
    if attention and attention.get("articles") is not None and day:
        line = (f"<strong>{attention['articles']:,}</strong> news mentions "
                f"from these countries on {esc(day)}")
        if attention.get("share_per_10k") is not None:
            line += (f" — {attention['share_per_10k']} of every 10,000 the "
                     f"world&#8217;s monitored press located that day")
        if attention.get("ratio_to_baseline"):
            line += (f", {attention['ratio_to_baseline']:.2f}&#215; their own "
                     f"28-day median")
        rows.append(f"<p>{line}.</p>")
        rows.append('<p class="note">Measured for the countries, not for the '
                    'hazard — a country&#8217;s news volume moves for many '
                    'reasons at once, and this instrument cannot tell them '
                    'apart.</p>')
    if entry.get("unmapped_iso3"):
        gaps = ", ".join(esc(c) for c in entry["unmapped_iso3"])
        rows.append(f'<p class="note">No attention series yet for {gaps} — '
                    f'the country crosswalk does not translate these codes. '
                    f'The gap is recorded, not counted as zero.</p>')
    money = entry.get("money", {})
    if money.get("has_fts_plan_match"):
        count = len(money.get("plans", []))
        plural = "s" if count != 1 else ""
        items = []
        for pid in money.get("plans", []):
            meta = plans_meta.get(pid, {})
            items.append(f'<li>{esc(meta.get("name", f"plan {pid}"))} — '
                         f'{_usd(meta.get("requirements", 0))} requested for '
                         f'2026, {_usd(funded.get(pid, 0))} recorded as '
                         f'funded</li>')
        rows.append(f"<p>{count} UN humanitarian response plan{plural} for "
                    f"2026 list{'' if plural else 's'} these countries:</p>"
                    f'<ul class="plans">{"".join(items)}</ul>')
        rows.append('<p class="note">Plan totals are the plans&#8217; own '
                    'annual figures for every country they list — not money '
                    'raised for this hazard, and no statement about adequacy, '
                    'need or responsibility.</p>')
    elif money:
        rows.append("<p>No UN humanitarian response plan for 2026 lists "
                    "these countries — a fact about two registers, not a "
                    "finding about the world.</p>")
    if not rows:
        return ""
    return ('<section><h2>While this warning runs</h2>'
            + "".join(rows) + "</section>")


def _dossier_verdict(resolution: dict | None) -> str:
    if not resolution:
        return ""
    measured = resolution.get("measured", {})
    lines = [f"<p>{VERDICT_LEADS.get(resolution.get('verdict'), esc(resolution.get('verdict', '')))}</p>"]
    facts = []
    if measured.get("episode_days") is not None:
        facts.append(f"the announced window spanned "
                     f"{measured['episode_days']} days")
    if measured.get("lead_time_hours") is not None:
        facts.append(f"measured lead time {measured['lead_time_hours']} hours")
    if measured.get("matched"):
        matched = esc(measured["matched"])
        facts.append(f'matched episode <a href="{matched}.html">{matched}</a>')
    facts.append(f"{measured.get('revisions', 0)} revision"
                 f"{'s' if measured.get('revisions', 0) != 1 else ''} while fed")
    path = [s for s in (measured.get("severity_path") or []) if s]
    if len(path) > 1:
        facts.append("alert level " + " &rarr; ".join(esc(s) for s in path))
    if measured.get("escalated"):
        facts.append("escalated to Red under watch")
    lines.append(f"<p>{'; '.join(facts)}.</p>")
    if resolution.get("cold_start"):
        lines.append('<p class="note">Cold start: this episode was already '
                     'running when observation began — durations are measured '
                     'from the machine&#8217;s first sight, not the '
                     'issuer&#8217;s first word.</p>')
    lines.append(_evidence_links(resolution.get("evidence", [])))
    return ('<section><h2>The verdict, measured</h2>'
            + "".join(lines) + "</section>")


def dossier_page(future: dict, data: dict) -> str:
    fid = future["id"]
    status = future["status"]
    status_words = {"OPEN": "open", "CLOSED_BY_SOURCE": "closed by its source",
                    "DISSIPATED": "dissipated"}.get(status, status.lower())
    overdue = _overdue_state(future, data["run_date"])
    if overdue:
        status_words = "open — announced window passed"
    kicker = (f"{esc(future.get('severity', ''))} alert · "
              f"{esc(future.get('hazard', ''))} · source "
              f"{esc(future.get('source', ''))} · {status_words}")

    notes = []
    if (future.get("announced_at") or "")[:10] == data["first_run_date"]:
        notes.append('<p class="note">This warning was already public when '
                     'the observatory began on ' + esc(data["first_run_date"])
                     + ' — the recorded time is the machine&#8217;s first '
                     'sight of it, not the issuer&#8217;s first '
                     'announcement.</p>')
    if overdue == "cold_start":
        notes.append('<p class="note">Its announced window already lay in '
                     'the past at first sight — an artefact of when '
                     'observation began, not a measured fact about the '
                     'warning.</p>')
    elif overdue == "drift":
        notes.append('<p class="note">This warning has outlived the window '
                     'it was announced with, under this machine&#8217;s '
                     'watch.</p>')

    items = []
    for event in future.get("history", []):
        kind = event.get("event", "")
        if kind == "REVISED":
            words = _revision_words(event.get("changes", {}))
        elif kind == "CORRECTED":
            words = _correction_words(event)
        else:
            words = esc(EVENT_WORDS.get(kind, kind.replace("_", " ").lower()))
        anchor = event.get("snapshot")
        evidence = _evidence_links([anchor]) if anchor else ""
        items.append(f'<li><span class="when">{esc(_when(event.get("ts")))} '
                     f'UTC</span>{words}{evidence}</li>')
    resolution = data["resolutions"].get(fid)
    if resolution:
        items.append(f'<li><span class="when">'
                     f'{esc(_when(resolution.get("resolved_at")))} UTC</span>'
                     f'resolved — verdict '
                     f'{esc(resolution.get("verdict", "").replace("_", " ").lower())}, '
                     f'measured from committed records only</li>')

    entry = (data["reading"] or {}).get("futures", {}).get(fid)
    clock = _clock(future) if status == "OPEN" else ""

    iso3 = ", ".join(esc(c) for c in future.get("iso3", [])) or "—"
    source_ref = future.get("source_ref") or ""
    source_link = (f' · <a href="{esc(source_ref)}">the source&#8217;s own '
                   f'report &rarr;</a>') if source_ref.startswith("http") else ""

    body = f"""
  <p class="kicker">{kicker}</p>
  <h1>{esc(future.get('what') or fid)}</h1>
  <p class="featured-where">{esc(future.get('where', ''))}</p>
  {clock}
  {''.join(notes)}

  <section>
    <h2>The life of this warning, from the record</h2>
    <ol class="trace-list">{''.join(items)}</ol>
  </section>

  {_dossier_reaction(entry, data['reading'], data['plans_meta'], data['funded'])}
  {_dossier_verdict(resolution)}

  <section>
    <h2>Provenance</h2>
    <p>Record id <code>{esc(fid)}</code> · countries {iso3} · first preserved
    {esc(_when(future.get('announced_at')))} UTC{source_link}</p>
    <p class="note">Every event above is anchored in a preserved snapshot with
    its SHA-256 on file. <a href="../verify.html">How to check any of it
    &rarr;</a></p>
  </section>"""
    return _shell(f"{_short(future.get('what') or fid, 70)} — The Foreknown",
                  "One announced future: its life, the world's reaction, "
                  "and the evidence.", body, depth=1)


def ledger_page(data: dict) -> str:
    futures = data["registry"]["futures"]
    open_futures = data["open"]
    nights = len(data["runs"])
    closed = data["total"] - len(open_futures)

    night_rows = []
    for run in reversed(data["runs"]):
        if not run:
            continue
        reaction = run.get("reaction") or {}
        rate = reaction.get("match_rate")
        night_rows.append(
            f"<tr><td>{esc(run.get('date', ''))}</td>"
            f"<td>{len(run.get('notarized', []))}</td>"
            f"<td>{len(run.get('revised', []))}</td>"
            f"<td>{len(run.get('closed', []))}</td>"
            f"<td>{len(run.get('resolved', []))}</td>"
            f"<td>{f'{rate:.0%}' if rate is not None else '—'}</td></tr>")

    groups: dict[str, list] = {}
    for future in open_futures:
        groups.setdefault(future["hazard"], []).append(future)
    group_html = []
    reading_futures = (data["reading"] or {}).get("futures", {})
    for hazard, members in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        rows = []
        for future in members:
            entry = reading_futures.get(future["id"], {})
            money = entry.get("money", {})
            plan = ("yes" if money.get("has_fts_plan_match")
                    else "no" if money else "—")
            to = ((future.get("window") or {}).get("to") or "")[:10] or "—"
            rows.append(
                f'<tr><td><a href="future/{esc(future["id"])}.html">'
                f'{esc(_short(future.get("what") or future["id"], 56))}</a></td>'
                f'<td>{esc(_short(future.get("where", ""), 36))}</td>'
                f'<td>{esc(future.get("severity", ""))}</td>'
                f'<td>{esc(to)}</td><td>{plan}</td></tr>')
        group_html.append(
            f'<h3 class="kicker">{esc(hazard)} · {len(members)}</h3>'
            f'<table class="tbl"><thead><tr><th>warning</th><th>where</th>'
            f'<th>alert</th><th>window ends</th><th>2026 plan</th></tr>'
            f'</thead><tbody>{"".join(rows)}</tbody></table>')

    closed_rows = []
    for fid, future in sorted(futures.items()):
        if future["status"] == "OPEN":
            continue
        resolution = data["resolutions"].get(fid)
        verdict = (esc(resolution["verdict"].replace("_", " ").lower())
                   if resolution else "verdict pending — the resolver runs "
                   "nightly")
        closed_rows.append(
            f'<tr><td><a href="future/{esc(fid)}.html">'
            f'{esc(_short(future.get("what") or fid, 56))}</a></td>'
            f'<td>{esc(future["status"].replace("_", " ").lower())}</td>'
            f'<td>{verdict}</td></tr>')
    if closed_rows:
        closed_html = ('<table class="tbl"><thead><tr><th>warning</th>'
                       '<th>how it closed</th><th>verdict</th></tr></thead>'
                       f'<tbody>{"".join(closed_rows)}</tbody></table>')
    else:
        closed_html = (f'<p class="trace">No warning has closed yet. The '
                       f'observatory is {nights} night'
                       f'{"s" if nights != 1 else ""} old; verdicts appear '
                       f'here when the sources let go.</p>')

    machine_bits = []
    coverage = (data["reading"] or {}).get("coverage")
    sensor_state = (data["reading"] or {}).get("sensor", {})
    if coverage:
        line = (f"The machine&#8217;s standing sensor measures nightly: "
                f"<strong>{coverage['with_fts_plan_match']} of "
                f"{coverage['open_alert_episodes']}</strong> open alert "
                f"episodes appear in a 2026 UN response plan "
                f"({coverage['match_rate']:.0%}).")
        if sensor_state.get("firing") == "DEFERRED":
            line += (f" Firing is deferred — "
                     f"{esc(sensor_state.get('why', ''))}.")
        machine_bits.append(f"<p>{line}</p>")
    order = {"STANDING": 0, "IMPLEMENTED": 1, "PROPOSED": 2}
    for sensor in sorted(data["sensors"],
                         key=lambda s: (order.get(s.get("status"), 3),
                                        s.get("name", ""))):
        status = sensor.get("status", "PROPOSED")
        badge = ("badge badge-standing" if status == "STANDING" else "badge")
        extra = ""
        if sensor.get("promotion"):
            extra = sensor["promotion"].get("why_standing", "")
        elif sensor.get("implementation"):
            extra = sensor["implementation"].get("not_promoted_because", "")
        elif sensor.get("review"):
            extra = sensor["review"].get("why", "")
        machine_bits.append(
            f'<p><span class="{badge}">{esc(status)}</span> '
            f'<strong>{esc(sensor.get("name", ""))}</strong></p>'
            f'<p>{esc(sensor.get("definition", ""))}</p>'
            + (f'<p class="note">{esc(extra)}</p>' if extra else ""))
    for observation in data["observations"]:
        derived = ", ".join(esc(p) for p in observation.get("derived_from", []))
        machine_bits.append(
            f'<p><strong>{esc(observation.get("title", ""))}</strong></p>'
            f'<p>{esc(observation.get("statement", ""))}</p>'
            f'<p class="note">derived from: {derived}</p>')
    if not data["sensors"] and not data["observations"]:
        machine_bits.append('<p class="trace">Nothing proposed yet — an '
                            'empty night is honest.</p>')

    body = f"""
  <p class="kicker">Investigate — the full record</p>
  <h1>The ledger</h1>
  <p>Everything the machine has recorded so far: <strong>{data['total']}
  announced futures</strong> over {nights} night{'s' if nights != 1 else ''}
  — {len(open_futures)} open, {closed} closed, {data['resolved']} resolved
  with a measured verdict.</p>

  <section>
    <h2>The nights</h2>
    <table class="tbl"><thead><tr><th>night</th><th>notarized</th>
    <th>revised</th><th>closed</th><th>resolved</th><th>plan match</th></tr>
    </thead><tbody>{''.join(night_rows)}</tbody></table>
  </section>

  <section>
    <h2>Open — the clocks still running</h2>
    {''.join(group_html)}
  </section>

  <section>
    <h2>Closed — and what the record says happened</h2>
    {closed_html}
  </section>

  <section>
    <h2>What the machine itself has noticed</h2>
    <p class="note">The nightly discovery pass reads the accumulated record
    and may propose observations and sensors. Everything below was written by
    the machine and cites committed files; promotion to a standing sensor is
    a separate, reasoned commit.</p>
    {''.join(machine_bits)}
  </section>"""
    return _shell("The ledger — The Foreknown",
                  "Every announced future the machine has recorded, night by "
                  "night, with what it noticed on its own.", body)


def verify_page(data: dict) -> str:
    days: dict[str, list] = {}
    for manifest in data["manifests"] + data["reaction_manifests"]:
        if manifest:
            days.setdefault(manifest["run_date"], []).extend(
                manifest.get("entries", []))
    shown_days = sorted(days)[-14:]
    day_html = []
    for day in reversed(shown_days):
        rows = "".join(
            f'<tr><td><a href="{_gh(esc(e["file"]))}">{esc(e["file"])}</a></td>'
            f'<td>{e.get("bytes", "—")}</td>'
            f'<td class="hash">{esc(e["sha256"])}</td></tr>'
            for e in days[day])
        day_html.append(f'<h3 class="kicker">{esc(day)}</h3>'
                        f'<table class="tbl"><thead><tr><th>preserved file'
                        f'</th><th>bytes</th><th>sha-256</th></tr></thead>'
                        f'<tbody>{rows}</tbody></table>')
    cap_note = (f'<p class="note">Showing the newest {len(shown_days)} of '
                f'{len(days)} recorded day{"s" if len(days) != 1 else ""}; '
                f'the full archive is the repository.</p>'
                if len(days) > len(shown_days) else "")

    attention_days = [d for d in data["attention_days"] if d]
    attention_rows = "".join(
        f'<tr><td>{esc(d.get("date", ""))}</td>'
        f'<td>{d.get("world", {}).get("articles", 0):,}</td>'
        f'<td><a href="{esc(d.get("source", {}).get("url", ""))}">source file'
        f'</a></td><td class="hash">{esc(d.get("source", {}).get("sha256", ""))}'
        f'</td></tr>'
        for d in list(reversed(attention_days))[:10])
    attention_note = (f'<p class="note">Showing the newest 10 of '
                      f'{len(attention_days)} committed days; every one '
                      f'carries url, byte count and SHA-256 in '
                      f'<a href="{REPO_URL}/tree/main/foreknown/reaction/attention">'
                      f'foreknown/reaction/attention</a>.</p>'
                      if len(attention_days) > 10 else "")

    crosswalk = data["crosswalk"] or {}
    crosswalk_html = ""
    if crosswalk.get("entries"):
        findings = crosswalk.get("findings", [])
        finding_note = ""
        if findings:
            finding_note = (f' The check against the issuer&#8217;s own code '
                            f'list has recorded {len(findings)} finding'
                            f'{"s" if len(findings) != 1 else ""} about the '
                            f'instrument itself — kept in the file, not '
                            f'silently corrected.')
        crosswalk_html = (
            f'<section><h2>The one hand-authored link</h2>'
            f'<p>The country crosswalk translates {len(crosswalk["entries"])} '
            f'iso3 codes to the FIPS codes GDELT locates events with. It is '
            f'the only hand-written joint in the chain, so it carries its own '
            f'evidence: every code is checked against '
            f'<a href="{_gh("foreknown/reaction/iso3-fips.json")}">the '
            f'committed record</a>, name by name.{finding_note}</p></section>')

    body = f"""
  <p class="kicker">Verify — where the claims meet the bytes</p>
  <h1>Nothing here asks to be believed</h1>
  <p>Every figure on these pages is derived from bytes preserved at the
  moment of reading — hashed, manifested, committed. This page is the bottom
  of the work: the chain itself.</p>

  <section>
    <h2>How the chain holds</h2>
    <p>Each night the machine fetches the public feeds and preserves the
    original bytes with URL, UTC time and SHA-256. The registry of announced
    futures is folded from those bytes; revisions append, nothing is
    overwritten. Verdicts and reaction figures are derived from committed
    records only. The stage — including this page — is a deterministic
    rebuild: the verifier recomputes every page and every reaction figure
    from the bytes and fails if one byte differs.</p>
  </section>

  <section>
    <h2>Run it yourself</h2>
    <pre><code>git clone {REPO_URL}
cd machine-attention &amp;&amp; python verify.py --repo-root .
cd practice &amp;&amp; python -m pip install -e '.[dev]' &amp;&amp; python -m pytest</code></pre>
  </section>

  <section>
    <h2>The preserved bytes</h2>
    {cap_note}
    {''.join(day_html)}
  </section>

  <section>
    <h2>Bytes referenced, not stored</h2>
    <p>The attention series reads GDELT&#8217;s daily export — about six
    megabytes a day, immutable once published. The bytes are not kept here;
    each committed day carries the url, length and SHA-256 of what was read,
    so the derivation can be redone by anyone. A hash that stops matching is
    not a broken link — it is the finding.</p>
    <table class="tbl"><thead><tr><th>day</th><th>world articles</th>
    <th>source</th><th>sha-256 of the bytes read</th></tr></thead>
    <tbody>{attention_rows}</tbody></table>
    {attention_note}
  </section>

  {crosswalk_html}

  <section>
    <h2>The machine&#8217;s own steps</h2>
    <p>Every run, every discovery pass and every human intervention appends
    to the <a href="{_gh("autonomy/log.jsonl")}">autonomy protocol</a> —
    actor, model, tokens, cost. No aggregate score is computed, by
    design.</p>
  </section>"""
    return _shell("Verify — The Foreknown",
                  "The provenance level: preserved bytes, hashes, and how to "
                  "re-run the whole chain.", body)


# --- the stage (ATTRACT) ----------------------------------------------------

def build(root: Path, out: Path | None = None) -> Path:
    out = out or root / "public"
    data = collect(root)
    open_futures = data["open"]

    # Display order: upcoming windows first (soonest deadline leads), then
    # passed-but-still-fed, then windowless. Ranked against the last committed
    # run date, never the wall clock (determinism).
    run_date = data["run_date"]

    def display_rank(f):
        to = (f.get("window") or {}).get("to")
        if not to:
            return (2, "", f["id"])
        return (0 if to[:10] >= run_date else 1, to, f["id"])

    display = sorted(open_futures, key=display_rank)
    featured = display[0] if display else None
    grid = display[1:7]

    hazard_counts: dict[str, int] = {}
    for f in open_futures:
        hazard_counts[f["hazard"]] = hazard_counts.get(f["hazard"], 0) + 1
    counts_line = " · ".join(
        f"{n} {h}{'s' if n != 1 and not h.endswith('s') else ''}"
        for h, n in sorted(hazard_counts.items(), key=lambda kv: -kv[1]))

    featured_html = ""
    if featured:
        announced = (featured.get("announced_at") or "")[:16].replace("T", " ")
        featured_html = f"""
<section class="featured" aria-label="The next warning on the clock">
  <p class="label">Right now — {esc(featured['severity'])} alert · {esc(featured['hazard'])} · source {esc(featured['source'])}</p>
  <h2><a class="plain" href="future/{esc(featured['id'])}.html">{esc(_short(featured['what'] or featured['id'], 80))}</a></h2>
  <p class="featured-where">{esc(_short(featured['where'], 90))}</p>
  {_clock(featured)}
  {reaction_line(data["reading"], featured["id"])}
  <p class="featured-provenance">warning recorded {esc(announced)} UTC · original bytes preserved, SHA-256 on file · <a class="plain" href="future/{esc(featured['id'])}.html">the full dossier &rarr;</a></p>
</section>"""

    cards = []
    for f in grid:
        cards.append(f"""
<a class="future" href="future/{esc(f['id'])}.html">
  <p class="future-kind">{esc(f['hazard'])} · {esc(f['severity'])} · {esc(f['source'])}</p>
  <h3>{esc(_short(f['what'] or f['id']))}</h3>
  <p class="future-where">{esc(_short(f['where'], 52))}</p>
  {_clock(f)}
</a>""")

    ledger_rows = []
    for event, future in data["events"]:
        label = event["event"].replace("_", " ").lower()
        ledger_rows.append(
            f'<p class="trace" data-cycle><strong>{esc(label)}</strong> — '
            f'{esc(_short(future.get("what") or future["id"], 70))} '
            f'<span class="verdict">{esc(_short(future.get("where", ""), 40))}'
            f' · {esc(event["ts"][:10])}</span></p>')

    since = (data["first_byte"] or "")[:10]

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Foreknown — a machine records the world's warnings</title>
<meta name="description" content="Disasters are announced before they happen. This machine preserves every public warning the moment it is issued — so no one can say later that nobody knew.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="stage">
  <header>
    <span>A machine is recording the world&#8217;s warnings</span>
    <span>every figure on this page is real</span>
  </header>

  <div class="hero">
    <h1>Disasters are announced before&nbsp;they&nbsp;happen.</h1>
    <p class="hero-sub">This machine preserves every public warning the moment it is
    issued — timestamped, hashed, beyond later denial — and watches what happens in
    the time that remains. So no one can say: nobody knew.</p>
  </div>

  {featured_html}

  <p class="counts"><strong>{len(open_futures)} warnings under watch right now</strong>
  — {esc(counts_line)}{f" · {data['resolved']} resolved with a measured verdict" if data['resolved'] else ''}
  · recording since {esc(since)} · next reading in
  <span id="countdown">—</span></p>

  <section class="futures" aria-label="More warnings under watch">
    {''.join(cards) if cards else ''}
  </section>

  <section class="ledger" aria-label="The ledger">
    <p class="label">The ledger — every warning&#8217;s life, on the record · <a class="plain" href="ledger.html">all {data['total']} &rarr;</a></p>
    {''.join(ledger_rows) if ledger_rows else '<p class="trace">The ledger is empty; the first reading has not run.</p>'}
  </section>

  <footer>
    <p class="state-line"><strong>What is this?</strong> The Foreknown — the first
    investigation of <em>machine attention</em>, a machine-run investigative practice.
    It applies evidence discipline to the future: warnings are preserved as original
    bytes with SHA-256 the moment they are issued, revisions never overwrite the
    original, and the machine&#8217;s own work is logged step by step. Subject is the
    warning system and institutional time — never the victims.</p>
    <nav class="enter-nav">
      <a class="enter" href="ledger.html">Ledger &rarr;</a>
      <a class="enter" href="verify.html">Verify &rarr;</a>
      <a class="enter" href="{METHOD_URL}">Method &rarr;</a>
      <a class="enter" href="{REPO_URL}">Archive &rarr;</a>
    </nav>
  </footer>
</div>
<script src="stage.js"></script>
</body>
</html>
"""
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "index.html").write_text(page, encoding="utf-8")

    # The deeper levels — every page a deterministic function of the records.
    (out / "future").mkdir()
    for fid, future in sorted(data["registry"]["futures"].items()):
        (out / "future" / f"{fid}.html").write_text(
            dossier_page(future, data), encoding="utf-8")
    (out / "ledger.html").write_text(ledger_page(data), encoding="utf-8")
    (out / "verify.html").write_text(verify_page(data), encoding="utf-8")

    (out / "style.css").write_text(STYLE, encoding="utf-8")
    (out / "stage.js").write_text(SCRIPT, encoding="utf-8")
    fonts_src = Path(__file__).parent / "fonts"
    if fonts_src.exists():
        shutil.copytree(fonts_src, out / "fonts")
    return out


STYLE = """\
@font-face { font-family: 'Plex Cond'; src: url(fonts/plexcond600.woff2) format('woff2');
  font-weight: 600; font-display: block; }
@font-face { font-family: 'Plex Mono'; src: url(fonts/plexmono400.woff2) format('woff2');
  font-weight: 400; font-display: block; }
:root { --ink:#0d1014; --paper:#e9e4d8; --faint:#8b867a; --trace:#565a63;
  --line:#23262c; --signal:#e8a03c; }
* { box-sizing: border-box; margin: 0; }
body { background: var(--ink); color: var(--paper);
  font: 400 clamp(12px,1.1vw,15px)/1.5 'Plex Mono', ui-monospace, monospace; }
a { color: inherit; }
a:focus-visible { outline: 2px solid var(--signal); outline-offset: 4px; }
.stage { min-height: 100dvh; display: grid;
  grid-template-rows: auto auto auto auto 1fr auto auto;
  padding: clamp(16px,3vmin,40px); gap: clamp(14px,2.4vmin,30px); }
header { display: flex; justify-content: space-between; gap: 2rem; color: var(--faint);
  font-size: clamp(10px,0.9vw,13px); letter-spacing: 0.14em; text-transform: uppercase; }
.hero h1 { font-family: 'Plex Cond','Arial Narrow',sans-serif; font-weight: 600;
  font-size: clamp(34px,6.8vw,110px); line-height: 0.98; text-transform: uppercase;
  text-wrap: balance; max-width: 16ch; }
.hero-sub { margin-top: clamp(10px,1.8vmin,20px); max-width: 62ch;
  color: var(--paper); font-size: clamp(13px,1.3vw,17px); }
.featured { border-left: 3px solid var(--signal);
  padding: 0.2rem 0 0.2rem clamp(0.9rem,2vw,1.6rem); }
.featured h2 { font-family: 'Plex Cond','Arial Narrow',sans-serif; font-weight: 600;
  font-size: clamp(22px,3.4vw,44px); line-height: 1.05; text-transform: uppercase;
  margin: 0.25rem 0 0.15rem; text-wrap: balance; }
.featured-where { color: var(--trace); }
.featured .clock { font-size: clamp(16px,2vw,26px); }
.featured-reaction { margin-top: 0.55rem; max-width: 74ch; }
.featured-reaction strong { color: var(--signal); font-weight: 400; }
.featured-provenance { color: var(--faint); font-size: 0.85em; margin-top: 0.4rem; }
.counts { color: var(--faint); max-width: 90ch; }
.counts strong { color: var(--paper); font-weight: 400; }
.counts #countdown { color: var(--signal); font-variant-numeric: tabular-nums; }
.label { color: var(--faint); letter-spacing: 0.14em;
  text-transform: uppercase; font-size: 0.8em; margin-bottom: 0.35em; display: block; }
.futures { display: grid; grid-template-columns: repeat(auto-fit,minmax(15rem,1fr));
  gap: 1px; background: var(--line); border: 1px solid var(--line); align-self: start; }
.future { background: var(--ink); padding: 0.9rem 1rem; }
a.future { text-decoration: none; display: block; }
a.future:hover h3 { color: var(--signal); }
.future-kind { color: var(--faint); font-size: 0.78em; letter-spacing: 0.1em;
  text-transform: uppercase; }
.future h3 { font-family: 'Plex Cond','Arial Narrow',sans-serif; font-weight: 600;
  font-size: clamp(15px,1.6vw,21px); line-height: 1.15; margin: 0.3rem 0 0.2rem;
  text-transform: uppercase; }
.future-where { color: var(--trace); font-size: 0.85em; }
.clock { display: block; margin-top: 0.5rem; font-variant-numeric: tabular-nums;
  color: var(--signal); }
.clock[data-from] { color: var(--faint); }
.ledger { border-top: 1px solid var(--line); padding-top: clamp(10px,2vmin,18px); }
.trace { color: var(--trace); overflow: hidden; text-overflow: ellipsis;
  white-space: nowrap; transition: opacity 2.2s ease; }
.trace strong { color: var(--paper); font-weight: 400; letter-spacing: 0.08em; }
.trace .verdict { color: var(--faint); }
.trace.is-hidden { display: none; }
.trace.is-fading { opacity: 0.12; }
footer { display: flex; justify-content: space-between; align-items: flex-end;
  gap: 2rem; border-top: 1px solid var(--line); padding-top: clamp(10px,2vmin,18px); }
.state-line { color: var(--faint); max-width: 72ch; }
.state-line strong, .state-line em { color: var(--paper); font-style: normal; }
.enter-nav { display: flex; gap: 1.4rem; flex-wrap: wrap; }
.enter { font-family: 'Plex Cond','Arial Narrow',sans-serif; font-weight: 600;
  text-transform: uppercase; font-size: clamp(14px,1.5vw,21px); letter-spacing: 0.06em;
  text-decoration: none; border-bottom: 2px solid var(--signal);
  padding-bottom: 2px; white-space: nowrap; }
.enter:hover { color: var(--signal); }
.plain { text-decoration: none; }
.plain:hover { color: var(--signal); }

/* the deeper levels: enter (dossier), investigate (ledger), verify */
.stage.doc { display: block; max-width: 86ch; margin: 0 auto; }
.doc header { margin-bottom: clamp(16px,2.6vmin,28px); }
.crumb { display: inline-block; color: var(--faint); text-decoration: none;
  margin-bottom: 1.2rem; }
.crumb:hover { color: var(--signal); }
.kicker { color: var(--faint); letter-spacing: 0.14em; text-transform: uppercase;
  font-size: 0.8em; margin: 1.2rem 0 0.4rem; }
.doc h1 { font-family: 'Plex Cond','Arial Narrow',sans-serif; font-weight: 600;
  text-transform: uppercase; font-size: clamp(26px,4.6vw,58px); line-height: 1.02;
  margin: 0.1rem 0 0.3rem; text-wrap: balance; }
.doc h2 { color: var(--faint); letter-spacing: 0.14em; text-transform: uppercase;
  font-size: 0.8em; font-weight: 400; margin: 2.2rem 0 0.6rem; }
.doc section p { max-width: 74ch; margin: 0.35rem 0; }
.note { color: var(--faint); font-size: 0.85em; max-width: 70ch; }
.trace-list { list-style: none; padding: 0; margin: 0.4rem 0 0;
  border-left: 2px solid var(--line); }
.trace-list li { padding: 0.5rem 0 0.5rem 1.1rem; position: relative;
  max-width: 72ch; }
.trace-list li::before { content: ''; position: absolute; left: -5px; top: 1.1em;
  width: 8px; height: 8px; background: var(--signal); }
.trace-list .when { color: var(--faint); font-size: 0.8em;
  letter-spacing: 0.08em; display: block; }
.evidence { display: block; color: var(--faint); font-size: 0.78em;
  margin-top: 0.15rem; }
.evidence a { color: inherit; }
.plans { margin: 0.3rem 0 0.4rem 1.1rem; padding: 0; }
.plans li { margin: 0.2rem 0; max-width: 70ch; }
.tbl { width: 100%; border-collapse: collapse; margin: 0.4rem 0 1rem; }
.tbl th { text-align: left; color: var(--faint); font-weight: 400;
  font-size: 0.75em; text-transform: uppercase; letter-spacing: 0.12em; }
.tbl th, .tbl td { padding: 0.4rem 0.9rem 0.4rem 0;
  border-bottom: 1px solid var(--line); vertical-align: top; }
.tbl a { color: inherit; text-decoration: none;
  border-bottom: 1px solid var(--signal); }
.tbl a:hover { color: var(--signal); }
.hash { color: var(--trace); font-size: 0.75em; word-break: break-all; }
.badge { text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.75em;
  color: var(--paper); border: 1px solid var(--line); padding: 0.1rem 0.45rem; }
.badge-standing { color: var(--signal); border-color: var(--signal); }
.doc pre { background: var(--line); padding: 0.8rem 1rem; overflow-x: auto;
  font-size: 0.85em; max-width: 74ch; }
.doc footer { margin-top: 2.6rem; }

@media (prefers-reduced-motion: reduce) { .trace { transition: none; } }
@media (max-width: 640px) {
  .trace { white-space: normal; }
  footer { flex-direction: column; align-items: flex-start; }
}
"""

SCRIPT = """\
'use strict';
function pad(n) { return String(n).padStart(2, '0'); }
function fmt(ms) {
  var s = Math.max(0, Math.floor(ms / 1000));
  var d = Math.floor(s / 86400);
  return (d > 0 ? d + 'd ' : '') + pad(Math.floor(s % 86400 / 3600)) + ':' +
    pad(Math.floor(s % 3600 / 60)) + ':' + pad(s % 60);
}
function parseUTC(iso) {
  if (!iso) return NaN;
  return Date.parse(/Z|[+-]\\d\\d:\\d\\d$/.test(iso) ? iso : iso + 'Z');
}
function nextReading(now) {
  var next = new Date(now);
  next.setUTCHours(5, 45, 0, 0);
  if (next.getTime() <= now) next.setUTCDate(next.getUTCDate() + 1);
  return next.getTime();
}
function tick() {
  var now = Date.now();
  var countdown = document.getElementById('countdown');
  if (countdown) countdown.textContent = fmt(nextReading(now) - now);
  document.querySelectorAll('.clock').forEach(function (c) {
    var to = parseUTC(c.getAttribute('data-to'));
    var from = parseUTC(c.getAttribute('data-from'));
    if (!isNaN(to)) {
      c.textContent = to > now
        ? fmt(to - now) + ' left in the announced danger window'
        : 'danger window passed ' + fmt(now - to) + ' ago — warning still active';
    } else if (!isNaN(from)) {
      c.textContent = 'ongoing for ' + fmt(now - from);
    }
  });
}
tick(); setInterval(tick, 1000);

var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var traces = Array.prototype.slice.call(document.querySelectorAll('.trace[data-cycle]'));
if (!reduced && traces.length > 3) {
  traces.forEach(function (t, i) { if (i >= 3) t.classList.add('is-hidden'); });
  var ti = 0;
  setInterval(function () {
    traces[ti % traces.length].classList.add('is-hidden');
    traces[(ti + 3) % traces.length].classList.remove('is-hidden');
    ti += 1;
  }, 6000);
}
"""


def main(argv=None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", type=Path)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)
    out = build(args.repo_root.resolve(), args.out)
    print(f"stage written to {out}")


if __name__ == "__main__":
    main()
