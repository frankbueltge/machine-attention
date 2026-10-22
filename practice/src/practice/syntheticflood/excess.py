"""Register A, the derived list: excess against the 2018–2022 trend, not its level.

Committed 2026-10-22 (docs/2026-10-22-synthetic-flood-v0-inkrement-3b.md),
before any derived list is computed for any cohort. Finding 2 of increment 3
(docs/2026-10-21-synthetic-flood-v0-inkrement-3.md): ten fixed words, `delve`
among them, already rose 2018→2022, so a level baseline would count their
pre-2023 drift as a machine trace. The rule therefore extrapolates each
word's own baseline trend, as the neighbour arXiv:2406.07016 does, and
measures the excess over that line. A changed rule is a new RULE id, never an
edit of this one. This module fetches nothing and writes nothing; it is pure.

Per pool word with a baseline verdict other than `rare`:
  trend     ordinary least squares of share_y on y over the baseline years
  position  a year cohort `YYYY` sits at YYYY; a month cohort `YYYY-MM` at
            YYYY + (MM - 0.5) / 12 - 0.5, so a year's mean is its middle
  expected  trend at the cohort's position; a word whose expected share is
            not above zero cannot be extrapolated and is left out (`no_trend`)
  ratio     observed share / expected share, rounded to four places

A pool word enters the month's derived list if ratio >= MIN_RATIO and the
cohort counts it in at least MIN_COUNT abstracts; the list holds at most
MAX_WORDS, highest ratio first, ties by word. The controls are measured the
same way and never enter: if any control's ratio leaves
[1 / CONTROL_BAND, CONTROL_BAND], the month is `control_breach` and its
derived list is reported but not used. The ratio describes a word, not a
text, and not how much was machine-written.
"""

from __future__ import annotations

RULE = "excess-v1"
MIN_RATIO = 2.0
MIN_COUNT = 50
MAX_WORDS = 20
CONTROL_BAND = 1.5


def position(cohort: str) -> float:
    if "-" in cohort:
        year, month = cohort.split("-")
        return int(year) + (int(month) - 0.5) / 12 - 0.5
    return float(int(cohort))


def trend(shares: dict[str, float]) -> tuple[float, float]:
    """(intercept, slope) of the least-squares line through (year, share)."""
    xs = [float(y) for y in shares]
    ys = list(shares.values())
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    return my - slope * mx, slope


def expected(shares: dict[str, float], cohort: str) -> float:
    a, b = trend(shares)
    return a + b * position(cohort)


def measure(word: dict, count: int, total: int, cohort: str) -> dict:
    """One word of one cohort against its baseline entry."""
    out = {"list": word["list"], "word": word["word"], "count": count}
    if word["verdict"] == "rare":
        return {**out, "status": "rare"}
    exp = expected(word["shares"], cohort)
    if exp <= 0:
        return {**out, "status": "no_trend"}
    observed = count / total
    return {**out, "status": "measured", "expected": round(exp, 9),
            "observed": round(observed, 9), "ratio": round(observed / exp, 4)}


def derive(baseline: dict, counts: dict[str, int], total: int, cohort: str) -> dict:
    """The derived list of one cohort. `counts` maps word -> count for every
    word of the baseline's word list, read for this cohort."""
    rows = [measure(w, counts[w["word"]], total, cohort) for w in baseline["words"]]
    controls = [r for r in rows if r["list"] == "controls" and r["status"] == "measured"]
    breach = [r["word"] for r in controls
              if not 1 / CONTROL_BAND <= r["ratio"] <= CONTROL_BAND]
    pool = [r for r in rows if r["list"] == "pool" and r["status"] == "measured"
            and r["ratio"] >= MIN_RATIO and r["count"] >= MIN_COUNT]
    pool.sort(key=lambda r: (-r["ratio"], r["word"]))
    return {
        "rule": {"id": RULE, "min_ratio": MIN_RATIO, "min_count": MIN_COUNT,
                 "max_words": MAX_WORDS, "control_band": CONTROL_BAND},
        "cohort": cohort,
        "control_breach": breach,
        "derived": [r["word"] for r in pool[:MAX_WORDS]],
        "words": rows,
    }
