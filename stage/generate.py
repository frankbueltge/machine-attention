#!/usr/bin/env python3
"""Build the practice stage deterministically from committed records.

Visual language: Prototype A (2026-08-08, Frank's pick) — a projection
surface, monumental true statements, real clocks, the ledger as fading
traces. Every figure is a real system state; quiet states are shown as
exactly that. Clocks tick client-side from data timestamps, so the build
stays byte-stable for identical data (verify.py rebuilds and compares).
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
    events = sorted(((h, f) for f in futures.values() for h in f["history"]),
                    key=lambda pair: pair[0]["ts"], reverse=True)[:12]
    return {"registry": registry, "runs": runs, "first_byte": first_byte,
            "open": open_futures, "events": events,
            "total": len(futures)}


def build(root: Path, out: Path | None = None) -> Path:
    out = out or root / "public"
    data = collect(root)
    open_futures = data["open"]
    # Derived from the last committed run record, never from the wall clock —
    # the build must be byte-stable for identical data (verify.py rebuilds).
    overdue = (data["runs"][-1].get("overdue", []) if data["runs"] else [])

    statements = ["The machine is watching the world&#8217;s warning systems."]
    if data["total"]:
        statements.append(f"It holds {len(open_futures)} announced futures under watch.")
        statements.append(f"It has notarized {data['total']} warnings, "
                          "each hashed the moment it was issued.")
    if not open_futures:
        statements.append("Nothing is announced tonight. The quiet is real.")

    # Display order: upcoming windows first (soonest deadline leads), then
    # passed-but-still-fed, then windowless. Ranked against the last committed
    # run date, never the wall clock (determinism).
    run_date = data["runs"][-1]["date"] if data["runs"] else ""

    def display_rank(f):
        to = (f.get("window") or {}).get("to")
        if not to:
            return (2, "", f["id"])
        return (0 if to[:10] >= run_date else 1, to, f["id"])

    cards = []
    for f in sorted(open_futures, key=display_rank)[:6]:
        window = f.get("window") or {}
        to, frm = window.get("to"), window.get("from")
        clock = (f'<span class="clock" data-to="{esc(to)}">—</span>' if to else
                 f'<span class="clock" data-from="{esc(frm)}">—</span>' if frm else "")
        cards.append(f"""
<article class="future">
  <p class="future-kind">{esc(f['hazard'])} · {esc(f['severity'])} · {esc(f['source'])}</p>
  <h3>{esc(_short(f['what'] or f['id']))}</h3>
  <p class="future-where">{esc(_short(f['where'], 52))}</p>
  {clock}
</article>""")

    ledger_rows = []
    for event, future in data["events"]:
        label = event["event"].replace("_", " ").lower()
        ledger_rows.append(
            f'<p class="trace" data-cycle><strong>{esc(label)}</strong> — '
            f'{esc(_short(future.get("what") or future["id"], 70))} '
            f'<span class="verdict">{esc(_short(future.get("where", ""), 40))}'
            f' · {esc(event["ts"][:10])}</span></p>')

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>machine attention — the foreknown</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="stage">
  <header>
    <span>machine attention — a machine investigative practice · project 001: the foreknown</span>
    <span>every figure is a real system state</span>
  </header>

  <div class="statement-zone">
    <h1 class="statement" id="statement">{statements[0]}</h1>
    <div class="clocks">
      <div><span class="label">Under observation</span>
        <span id="elapsed" data-first="{esc(data['first_byte'] or '')}">—</span></div>
      <div><span class="label">Next observation</span>
        <span class="next" id="countdown">—</span></div>
      <div><span class="label">Announced futures</span>
        <span>{len(open_futures)} open · {len(overdue)} with windows in question</span></div>
    </div>
  </div>

  <section class="futures" aria-label="Announced futures under watch">
    {''.join(cards) if cards else '<p class="quiet">No announced future is under watch. The quiet is real.</p>'}
  </section>

  <section class="ledger" aria-label="The notary ledger">
    <p class="label">The ledger — notarized, revised, closed</p>
    {''.join(ledger_rows) if ledger_rows else '<p class="trace">The ledger is empty; the first observation has not run.</p>'}
  </section>

  <footer>
    <p class="state-line">Warnings are preserved as original bytes with SHA-256 the
    moment they are issued — the archive proves what was knowable, when. Subject is
    the warning system and institutional time, never the victims.</p>
    <a class="enter" href="https://github.com/frankbueltge/machine-attention">Enter the archive &rarr;</a>
  </footer>
</div>
<script src="stage.js"></script>
<script id="statements" type="application/json">{json.dumps(statements)}</script>
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
  grid-template-rows: auto 1fr auto auto auto;
  padding: clamp(16px,3vmin,40px); gap: clamp(12px,2.2vmin,26px); }
header { display: flex; justify-content: space-between; gap: 2rem; color: var(--faint);
  font-size: clamp(10px,0.9vw,13px); letter-spacing: 0.14em; text-transform: uppercase; }
.statement-zone { display: grid; align-content: center; gap: clamp(16px,3.5vmin,40px); }
.statement { font-family: 'Plex Cond','Arial Narrow',sans-serif; font-weight: 600;
  font-size: clamp(30px,6.4vw,104px); line-height: 0.98; text-transform: uppercase;
  text-wrap: balance; max-width: 19ch; min-height: 2.9em; transition: opacity 1.4s ease; }
.statement.is-fading { opacity: 0; }
.clocks { display: flex; flex-wrap: wrap; gap: 1.2em 3.5em;
  font-variant-numeric: tabular-nums; font-size: clamp(12px,1.25vw,17px); }
.clocks .label, .label { color: var(--faint); letter-spacing: 0.14em;
  text-transform: uppercase; font-size: 0.8em; display: block; margin-bottom: 0.35em; }
.clocks .next { color: var(--signal); }
.futures { display: grid; grid-template-columns: repeat(auto-fit,minmax(15rem,1fr));
  gap: 1px; background: var(--line); border: 1px solid var(--line); }
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
.quiet { color: var(--faint); padding: 1rem; background: var(--ink); }
footer { display: flex; justify-content: space-between; align-items: baseline;
  gap: 2rem; border-top: 1px solid var(--line); padding-top: clamp(10px,2vmin,18px); }
.state-line { color: var(--faint); max-width: 64ch; }
.enter { font-family: 'Plex Cond','Arial Narrow',sans-serif; font-weight: 600;
  text-transform: uppercase; font-size: clamp(15px,1.7vw,24px); letter-spacing: 0.06em;
  text-decoration: none; border-bottom: 2px solid var(--signal);
  padding-bottom: 2px; white-space: nowrap; }
.enter:hover { color: var(--signal); }
@media (prefers-reduced-motion: reduce) { .statement, .trace { transition: none; } }
@media (max-width: 640px) { .trace { white-space: normal; } }
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
function nextObservation(now) {
  var next = new Date(now);
  next.setUTCHours(5, 45, 0, 0);
  if (next.getTime() <= now) next.setUTCDate(next.getUTCDate() + 1);
  return next.getTime();
}
function tick() {
  var now = Date.now();
  var el = document.getElementById('elapsed');
  var first = parseUTC(el.getAttribute('data-first'));
  el.textContent = isNaN(first) ? 'first observation pending' : fmt(now - first);
  document.getElementById('countdown').textContent = fmt(nextObservation(now) - now);
  document.querySelectorAll('.clock').forEach(function (c) {
    var to = parseUTC(c.getAttribute('data-to'));
    var from = parseUTC(c.getAttribute('data-from'));
    if (!isNaN(to)) {
      c.textContent = to > now ? fmt(to - now) + ' remain in the announced window'
        : 'window passed ' + fmt(now - to) + ' ago — still fed';
    } else if (!isNaN(from)) {
      c.textContent = 'ongoing for ' + fmt(now - from);
    }
  });
}
tick(); setInterval(tick, 1000);

var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var statements = JSON.parse(document.getElementById('statements').textContent);
var stmtEl = document.getElementById('statement');
var traces = Array.prototype.slice.call(document.querySelectorAll('.trace[data-cycle]'));
if (!reduced && statements.length > 1) {
  var si = 0;
  setInterval(function () {
    stmtEl.classList.add('is-fading');
    setTimeout(function () {
      si = (si + 1) % statements.length;
      stmtEl.innerHTML = statements[si];
      stmtEl.classList.remove('is-fading');
    }, 1400);
  }, 9500);
}
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
