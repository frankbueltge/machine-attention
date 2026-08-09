"""The C3 draft for Dark Ocean — built, not promised.

Criterion C3 of the acceptance criteria
(`docs/2026-08-09-dark-ocean-e-experiment-kriterien.md`) requires a *built*
draft at the review of 2026-08-24, not a described one. The One Tap lesson is
the whole reason: good evidence does not automatically make a good work, and
a form that only exists as a paragraph has never been tested against its own
material.

So this writes one, from committed records only, while the window runs. It is
**not** a stage: the admission path forbids public presence before the
E-experiment is passed, so the output lives in `darkocean/draft/`, carries a
banner saying what it is, and is not mirrored to the site.

What it stages is the claim rather than its demonstration (`darkocean/METHOD.md`):
the machine holds the publisher's own checksummed claims and asks again every
night. The per-bin overlap counts appear below as what they are — the
demonstration, and a degraded subset of what Global Fishing Watch publishes.

Deliberately not wired into the nightly workflow: a draft that rewrites itself
every night would fill the history with noise for an artifact nobody reads
until the review. Run it when you want to look:

    python stage/darkocean_draft.py --repo-root .
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

REVIEW_DATE = "2026-08-24"
WINDOW = "2026-08-09/10 → 2026-08-22/23"


def read_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def collect(root: Path) -> dict:
    readings = [read_json(p) for p in sorted((root / "darkocean" / "readings").glob("*.json"))]
    continuity = [read_json(p) for p in sorted((root / "darkocean" / "continuity").glob("*.json"))]

    # Every product the register holds, first sighting wins — the same origin
    # the continuity probe uses.
    held: dict[str, dict] = {}
    for reading in readings:
        for acquisition in reading.get("acquisitions", []):
            pid = acquisition.get("id")
            if pid and pid not in held:
                held[pid] = {"id": pid, "name": acquisition.get("name", ""),
                             "first_seen": reading.get("date", ""),
                             "platform": acquisition.get("platform", ""),
                             "state": "unchecked"}

    catches: list[dict] = []
    baselines = 0
    probes = 0
    for record in continuity:
        probes += record.get("answered", 0)
        baselines += len(record.get("baselines_established", []))
        for catch in record.get("catches", []):
            catches.append(catch)
            entry = held.get(catch.get("id", ""))
            if entry is not None:
                entry["state"] = "diverged"
    if continuity:
        for entry in held.values():
            if entry["state"] == "unchecked":
                entry["state"] = "held"

    return {
        "readings": readings,
        "continuity": continuity,
        "held": [held[k] for k in sorted(held, key=lambda k: held[k]["name"])],
        "catches": catches,
        "baselines": baselines,
        "probes": probes,
        "nights": len(readings),
        "checked_nights": len(continuity),
    }


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def sentence(data: dict) -> str:
    """The ten-second rule's ONE plain sentence. The first draft of this page
    ran to six lines — a paragraph in disguise, which is exactly the failure
    the rule exists to catch. The count belongs under the figure, not inside
    the sentence."""
    if data["catches"]:
        return "A public archive changed its mind. This machine had written down what it said."
    return "Every night this machine asks a public archive whether it still says what it said."


def second_line(data: dict) -> str:
    """The numbers, one line under the sentence — true on a quiet night, which
    is most nights."""
    products = len(data["held"])
    if not data["continuity"]:
        return (f"{products} statements written down. The asking has not run yet in this "
                f"checkout.")
    nights = data["checked_nights"]
    if data["catches"]:
        return (f"{products} statements, {nights} night(s) of asking, "
                f"{len(data['catches'])} changed.")
    return (f"{products} statements, {nights} night(s) of asking, nothing changed — "
            f"and that is a result, not a failure.")


def matrix(data: dict) -> str:
    """One row per NIGHT, one cell per statement — the ledger shape.

    Two drafts were wrong before this one, and both failures were instructive.
    The first was a single row of marks per product: it said "a register
    exists" and could not say the only thing the piece is about, that the same
    question is asked again and again. The second put products down the page
    and nights across — which made the interesting axis the short one and drew
    a tall grey stripe: 79 rows against 3 columns, growing narrower in meaning
    as it grew taller.

    Transposed, it becomes what it actually is: a night is a line, the register
    is its length, and the page grows downward the way a ledger does. A change
    is one coloured cell in the line of the night it happened.
    """
    nights = [record.get("date", "") for record in data["continuity"]]
    if not nights:
        return ('<p class="empty">No line yet: the look-back has not run in this checkout. '
                'The first night of asking writes the first line — and lines are what this '
                'figure is made of.</p>')
    diverged_on = {(c.get("id"), n) for n, record in zip(nights, data["continuity"])
                   for c in record.get("catches", [])}
    rows = []
    for night, record in zip(nights, data["continuity"]):
        cells = []
        for entry in data["held"]:
            if entry["first_seen"] > night:
                state, word = "before", "not yet recorded"
            elif (entry["id"], night) in diverged_on:
                state, word = "diverged", "CHANGED on this night"
            else:
                state, word = "same", "asked; still the same"
            cells.append(f'<i class="c c-{state}" title="{esc(night)} · '
                         f'{esc(entry["name"])} · {word}"></i>')
        changed = len(record.get("catches", []))
        tail = f"{changed} changed" if changed else "nothing changed"
        rows.append(f'<div class="row"><span class="d">{esc(night)}</span>'
                    f'<span class="cells">{"".join(cells)}</span>'
                    f'<span class="t">{esc(tail)}</span></div>')
    return f'<div class="ledger">{"".join(rows)}</div>'


def coverage_rows(data: dict) -> str:
    rows = []
    for reading in data["readings"]:
        c = reading.get("coverage", {})
        declared = reading.get("declared_axis") or {}
        rows.append(
            f"<tr><td>{esc(reading.get('date'))}</td>"
            f"<td>{c.get('acquisitions', '—')}</td>"
            f"<td>{c.get('cells_observed', '—')}</td>"
            f"<td>{c.get('cells_declared_sample', '—')}</td>"
            f"<td>{declared.get('vessels_in_region', '—')}</td>"
            f"<td>{esc((reading.get('moment_axis') or {}).get('dma_probe', {}).get('state', '—'))}</td></tr>")
    return "".join(rows)


def held_rows(data: dict) -> str:
    rows = []
    for entry in data["held"]:
        state = {"held": "held, unchanged", "diverged": "CHANGED",
                 "unchecked": "not yet re-probed"}[entry["state"]]
        rows.append(f"<tr><td>{esc(entry['name'])}</td><td>{esc(entry['first_seen'])}</td>"
                    f"<td>{esc(state)}</td></tr>")
    return "".join(rows)


def build(root: Path) -> str:
    data = collect(root)
    products = len(data["held"])
    catches = len(data["catches"])

    figure_note = (
        f"{products} products held · {data['probes']} re-probes on "
        f"{data['checked_nights']} night(s) · {catches} divergence(s)"
        if data["continuity"] else
        f"{products} products held · the look-back has not run yet in this checkout"
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Dark Ocean — draft (not published)</title>
<style>
  :root {{ color-scheme: light dark; --bg:#fff; --fg:#111; --muted:#555; --faint:#888;
           --line:#ddd; --panel:#f6f6f6; --held:#9aa7b1; --diverged:#c2410c; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#0e0f10; --fg:#eee; --muted:#aaa; --faint:#777; --line:#2a2c2e;
             --panel:#151719; --held:#4a5560; --diverged:#f97316; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--fg);
         font:16px/1.55 ui-monospace, SFMono-Regular, Menlo, monospace; }}
  main {{ max-width:44rem; margin:0 auto; padding:2rem 1.25rem 5rem; }}
  .banner {{ border:1px solid var(--diverged); color:var(--diverged);
             padding:.6rem .8rem; font-size:.72rem; letter-spacing:.12em;
             text-transform:uppercase; }}
  h1 {{ font-size:1.05rem; letter-spacing:.18em; text-transform:uppercase;
        color:var(--faint); font-weight:600; margin:2.5rem 0 .5rem; }}
  .sentence {{ font-size:clamp(1.35rem,3.6vw,2rem); line-height:1.3; margin:.5rem 0 2rem;
               font-weight:600; letter-spacing:-.01em; }}
  .field {{ padding:1rem; border:1px solid var(--line); background:var(--panel);
            overflow-x:auto; }}
  .second {{ color:var(--muted); font-size:.9rem; margin:-1.25rem 0 2rem; }}
  .ledger {{ display:flex; flex-direction:column; gap:6px; min-width:min-content; }}
  .row {{ display:flex; align-items:center; gap:.6rem; }}
  .d {{ font-size:.62rem; color:var(--faint); width:5.2em; flex:none; }}
  .t {{ font-size:.62rem; color:var(--faint); white-space:nowrap; flex:none; }}
  .cells {{ display:flex; gap:1px; flex:none; }}
  .c {{ width:5px; height:16px; display:block; background:var(--held); }}
  .c-before {{ background:transparent; box-shadow:inset 0 0 0 1px var(--line); }}
  .c-diverged {{ background:var(--diverged); }}
  .empty {{ color:var(--faint); font-size:.8rem; margin:0; }}
  .note {{ color:var(--faint); font-size:.78rem; margin-top:.6rem; }}
  table {{ width:100%; border-collapse:collapse; font-size:.8rem; margin-top:.75rem; }}
  th,td {{ text-align:left; padding:.35rem .5rem; border-bottom:1px solid var(--line);
           color:var(--muted); }}
  th {{ color:var(--faint); font-weight:600; font-size:.7rem; letter-spacing:.1em;
        text-transform:uppercase; }}
  details {{ border:1px solid var(--line); padding:.75rem 1rem; margin-top:1rem;
             background:var(--panel); }}
  summary {{ cursor:pointer; font-size:.82rem; color:var(--fg); }}
  .scroll {{ overflow-x:auto; }}
  p {{ color:var(--muted); }}
  code {{ color:var(--fg); }}
</style>
</head>
<body>
<main>
  <p class="banner">Draft for the acceptance review of {REVIEW_DATE} — criterion C3.
  Not published, not a stage. The E-experiment runs {WINDOW}.</p>

  <p class="sentence">{esc(sentence(data))}</p>
  <p class="second">{esc(second_line(data))}</p>

  <h1>Every night, asked again</h1>
  <div class="field">{matrix(data)}</div>
  <p class="note">{esc(figure_note)}. One line per night, one cell per statement held
  that night. A filled cell is a statement the archive still stood by; an outlined one
  did not exist yet. A change would be a single coloured cell in the line of the night
  it happened — this page has no event until the world gives it one, and does not
  manufacture one.</p>

  <details>
    <summary>Open the register — every product, what it said, whether it still says it</summary>
    <div class="scroll">
      <table>
        <tr><th>Product</th><th>First seen</th><th>State</th></tr>
        {held_rows(data)}
      </table>
    </div>
  </details>

  <h1>The demonstration</h1>
  <p>The per-bin overlap counts below are not the claim. Read as a measurement of
  maritime reality they are a degraded subset of what Global Fishing Watch already
  publishes; they exist to show what two committed registers can jointly say.</p>
  <div class="scroll">
    <table>
      <tr><th>Night</th><th>Passes</th><th>Bins observed</th><th>Bins declared</th>
          <th>Vessels declared</th><th>Moment axis</th></tr>
      {coverage_rows(data)}
    </table>
  </div>

  <h1>What this is not</h1>
  <p>The eviction premise is <b>structural, not observed</b>: every product probed so far
  is online with an eviction date of 9999-12-31. Copernicus is not evicting this material
  and names no date — the register measures whether that stays true.</p>
  <p>The declared axis is <b>one agency's receiver range</b> off the Finnish coast, against
  a radar box covering the whole Baltic. Until the discrepancy is reported inside a committed
  declared-coverage envelope, the headline silence number measures receiver geography, not
  disclosure.</p>
  <p>Bins are half-degree cells over a bounding box, not sea masks. Counts only: no vessel
  identity enters a derived record, and an "observed silent" bin is a statement about the
  overlap of two registers, never about ships hiding.</p>

  <h1>Check it</h1>
  <p><code>python verify.py --repo-root .</code> recomputes every figure above from the
  preserved bytes, in a second implementation.</p>
</main>
</body>
</html>
"""


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Build the Dark Ocean C3 draft.")
    parser.add_argument("--repo-root", default=".", type=Path)
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    out = root / "darkocean" / "draft" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(root), encoding="utf-8")
    data = collect(root)
    print(f"draft written to {out} — {len(data['held'])} products, "
          f"{len(data['catches'])} divergence(s), "
          f"{data['checked_nights']} checked night(s)")


if __name__ == "__main__":
    main()
