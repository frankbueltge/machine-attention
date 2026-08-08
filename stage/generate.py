#!/usr/bin/env python3
"""Build the practice stage deterministically from committed records.

V2 (2026-08-08, after Frank's ten-second test): the first screen must be
understood by a first-time visitor in ten seconds — one plain sentence, one
real phenomenon (the next-expiring warning, ticking), one action. House
vocabulary ("practice", "notarized", "announced futures") appears only after
the plain words, never instead of them. Every figure is a real system state;
clocks tick client-side from data timestamps so the build stays byte-stable
for identical data (verify.py rebuilds and compares).
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path


def read_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def _short(text: str, limit: int = 64) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def collect(root: Path) -> dict:
    registry = read_json(root / "foreknown" / "registry.json", {"futures": {}})
    runs = [read_json(p) for p in sorted(root.glob("foreknown/snapshots/*/run.json"))]
    manifests = [read_json(p) for p in
                 sorted(root.glob("foreknown/snapshots/*/manifest.json"))]
    first_byte = min((e["retrieved_at"] for m in manifests
                      for e in m.get("entries", [])), default=None)
    futures = registry["futures"]
    open_futures = sorted((f for f in futures.values() if f["status"] == "OPEN"),
                          key=lambda f: (f.get("window", {}).get("to") or "9999",
                                         f["id"]))
    resolutions = [read_json(p)
                   for p in sorted(root.glob("foreknown/resolutions/*.json"))]
    event_pairs = [(h, f) for f in futures.values() for h in f["history"]]
    event_pairs += [({"ts": r["resolved_at"], "event": f"RESOLVED_{r['verdict']}"},
                     futures[r["future"]])
                    for r in resolutions if r.get("future") in futures]
    events = sorted(event_pairs, key=lambda pair: pair[0]["ts"],
                    reverse=True)[:12]
    return {"registry": registry, "runs": runs, "first_byte": first_byte,
            "open": open_futures, "events": events,
            "resolved": len(resolutions), "total": len(futures)}


def _clock(future: dict) -> str:
    window = future.get("window") or {}
    to, frm = window.get("to"), window.get("from")
    if to:
        return f'<span class="clock" data-to="{esc(to)}">—</span>'
    if frm:
        return f'<span class="clock" data-from="{esc(frm)}">—</span>'
    return ""


def build(root: Path, out: Path | None = None) -> Path:
    out = out or root / "public"
    data = collect(root)
    open_futures = data["open"]

    # Display order: upcoming windows first (soonest deadline leads), then
    # passed-but-still-fed, then windowless. Ranked against the last committed
    # run date, never the wall clock (determinism).
    run_date = data["runs"][-1]["date"] if data["runs"] else ""

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
  <h2>{esc(_short(featured['what'] or featured['id'], 80))}</h2>
  <p class="featured-where">{esc(_short(featured['where'], 90))}</p>
  {_clock(featured)}
  <p class="featured-provenance">warning recorded {esc(announced)} UTC · original bytes preserved, SHA-256 on file</p>
</section>"""

    cards = []
    for f in grid:
        cards.append(f"""
<article class="future">
  <p class="future-kind">{esc(f['hazard'])} · {esc(f['severity'])} · {esc(f['source'])}</p>
  <h3>{esc(_short(f['what'] or f['id']))}</h3>
  <p class="future-where">{esc(_short(f['where'], 52))}</p>
  {_clock(f)}
</article>""")

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
    <p class="label">The ledger — every warning&#8217;s life, on the record</p>
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
      <a class="enter" href="https://frankbueltge.de/werke/attention">Method &rarr;</a>
      <a class="enter" href="https://github.com/frankbueltge/machine-attention">Archive &rarr;</a>
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
.featured-provenance { color: var(--faint); font-size: 0.85em; margin-top: 0.4rem; }
.counts { color: var(--faint); max-width: 90ch; }
.counts strong { color: var(--paper); font-weight: 400; }
.counts #countdown { color: var(--signal); font-variant-numeric: tabular-nums; }
.label { color: var(--faint); letter-spacing: 0.14em;
  text-transform: uppercase; font-size: 0.8em; margin-bottom: 0.35em; display: block; }
.futures { display: grid; grid-template-columns: repeat(auto-fit,minmax(15rem,1fr));
  gap: 1px; background: var(--line); border: 1px solid var(--line); align-self: start; }
.future { background: var(--ink); padding: 0.9rem 1rem; }
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
.enter-nav { display: flex; gap: 1.4rem; }
.enter { font-family: 'Plex Cond','Arial Narrow',sans-serif; font-weight: 600;
  text-transform: uppercase; font-size: clamp(14px,1.5vw,21px); letter-spacing: 0.06em;
  text-decoration: none; border-bottom: 2px solid var(--signal);
  padding-bottom: 2px; white-space: nowrap; }
.enter:hover { color: var(--signal); }
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
  document.getElementById('countdown').textContent = fmt(nextReading(now) - now);
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
