"""Register A, rule control-check-v1: may a word serve as a control after 2022?

Committed 2026-11-05 (docs/2026-11-05-synthetic-flood-kontrollpruefung.md),
before any 2023–2025 count of any control except `reduced` exists in the
record. Finding of 2026-11-03 (docs/2026-11-03-synthetic-flood-reduced-jahre.md):
the control `reduced` rose in 2024 and 2025, so a control proven stable on
2018–2022 alone is not proven stable after it. Every control of the next word
list must therefore pass this test on the check years; the result of the test
composes `wordlist-v3`. A changed rule is a new RULE id, never an edit of this
one. This module fetches nothing and writes nothing; it is pure.

Per word, given its baseline entry (rule baseline-v1, years 2018–2022) and
its counts in the year cohorts 2023, 2024, 2025:
  expected  the word's 2018–2022 least-squares line at the year (excess-v1)
  ratio     observed share / expected share, rounded to four places
  pass      baseline verdict `stable`, every check year counted in at least
            MIN_COUNT abstracts, and every ratio in [1 / BAND, BAND]

BAND is 1.2, tighter than excess-v1's control band of 1.5 on purpose: on the
committed counts `reduced` lies at 1.0247 / 1.1266 / 1.4445 in 2023 / 24 / 25,
inside 1.5 in every check year and still breaching it at the cohort 2026-09.
A test band equal to the use band would have passed the word that broke it.

Composition of the next control list (`compose`): the current controls that
pass, in their order, without the struck word; then the CANDIDATES that pass,
in their committed order, until the list holds TARGET words again. If fewer
than MIN_CONTROLS pass in all, no next list is composed and that is reported.
The candidates were chosen before any of their counts was read: content words
of the abstracts' own register, on no list of wordlist-v2, none a PubMed
stopword by its published list. A candidate needs a baseline-v1 entry like
every control, so its five baseline years are read along with the check years.
"""

from __future__ import annotations

from . import excess

RULE = "control-check-v1"
CHECK_YEARS = ("2023", "2024", "2025")
BAND = 1.2
MIN_COUNT = 50
STRUCK = ("reduced",)
CANDIDATES = ("samples", "groups", "cases", "performed", "total", "age")
TARGET = 20
MIN_CONTROLS = 15


def check(entry: dict, counts: dict[str, int], totals: dict[str, int]) -> dict:
    """One word against its baseline entry over the check years.

    `entry` carries `word`, `verdict` and `shares` (2018–2022) as in
    syntheticflood/baseline/<wordlist>.json; `counts` and `totals` map each
    check year to the word's count and the cohort's `hasabstract` total."""
    out = {"word": entry["word"], "baseline_verdict": entry["verdict"]}
    missing = [y for y in CHECK_YEARS if counts.get(y) is None or not totals.get(y)]
    if missing:
        return {**out, "pass": False, "reason": "unread", "missing": missing}
    if entry["verdict"] != "stable":
        return {**out, "pass": False, "reason": "baseline_not_stable"}
    years = {}
    for y in CHECK_YEARS:
        exp = excess.expected(entry["shares"], y)
        obs = counts[y] / totals[y]
        years[y] = {"count": counts[y], "observed": round(obs, 9),
                    "expected": round(exp, 9),
                    "ratio": round(obs / exp, 4) if exp > 0 else None}
    out["years"] = years
    if min(counts[y] for y in CHECK_YEARS) < MIN_COUNT:
        return {**out, "pass": False, "reason": "rare"}
    if any(v["ratio"] is None for v in years.values()):
        return {**out, "pass": False, "reason": "no_trend"}
    if not all(1 / BAND <= v["ratio"] <= BAND for v in years.values()):
        return {**out, "pass": False, "reason": "outside_band"}
    return {**out, "pass": True, "reason": None}


def compose(controls: list[str], results: dict[str, dict]) -> dict:
    """The next control list from the current one and the checked words.

    `results` maps every word checked (current controls and candidates) to
    its `check` result; a word without a result counts as not passed."""
    passed = lambda w: bool(results.get(w, {}).get("pass"))
    kept = [w for w in controls if w not in STRUCK and passed(w)]
    added = []
    for w in CANDIDATES:
        if len(kept) + len(added) >= TARGET:
            break
        if w not in controls and passed(w):
            added.append(w)
    new = kept + added
    return {
        "rule": {"id": RULE, "band": BAND, "min_count": MIN_COUNT,
                 "check_years": list(CHECK_YEARS), "target": TARGET,
                 "min_controls": MIN_CONTROLS},
        "struck": [w for w in controls if w in STRUCK],
        "dropped": [w for w in controls if w not in STRUCK and not passed(w)],
        "kept": kept,
        "added": added,
        "controls": new if len(new) >= MIN_CONTROLS else None,
    }
