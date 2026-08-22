"""The reaction axis, joined to the future it belonged to.

Since 2026-08-08 every night measures money and attention for each
source-open future (`foreknown/reaction/readings/`), and until 2026-08-22 not
one resolution carried any of it: E1 asked for a full cycle from warning to
resolution *with* both time series, the data was on the disk every one of
those nights, and nothing joined the two. The E1 review of 2026-08-22 named
that as a build gap rather than a finding; this module closes it.

Two disciplines hold here. The series is read from committed readings only —
never a fresh fetch, so a resolution written today and a resolution rebuilt
in a year read the same bytes. And a future disappears from the reaction
readings the night it stops being source-open, which means the series is
exactly the future's watched life, not its announced window: for a future
that was already historical at first sight the two are very different, and
the record says which one it is showing.
"""

from __future__ import annotations

from pathlib import Path

from ..preserve import read_json

# What the numbers are not — carried in the record, not appended to a page as
# a footnote. The first two are the reaction axis's own limits, restated here
# because a resolution can be read far away from the reading it came from.
LIMITS = (
    "the money figures are the response plans' own annual totals for every "
    "country they list; none of it was raised for this hazard and no part of "
    "it is attributable to this future",
    "attention is measured for the future's countries, not for the hazard — a "
    "second event in the same country moves the same number",
    "the series covers the nights this future was source-open under watch, "
    "which for a cold start is shorter than its announced window",
    "a funding movement inside the watch happened in the same period as the "
    "warning, which is not the same as because of it",
)


def _night(doc: dict, entry: dict) -> dict:
    money = entry.get("money") or {}
    attention = entry.get("attention") or {}
    return {
        "date": doc.get("date"),
        "attention_day": doc.get("attention_day"),
        "articles": attention.get("articles"),
        "ratio_to_baseline": attention.get("ratio_to_baseline"),
        "has_fts_plan_match": money.get("has_fts_plan_match"),
        "plan_requirements_usd": money.get("plan_requirements_usd"),
        "plan_funded_usd": money.get("plan_funded_usd"),
    }


def _peak(nights: list[dict]) -> dict | None:
    """The loudest night by ratio to the country's own baseline. Ratio, not
    article count: a large country is not more newsworthy than a small one."""
    rated = [n for n in nights if n.get("ratio_to_baseline") is not None]
    if not rated:
        return None
    top = max(rated, key=lambda n: (n["ratio_to_baseline"], n["date"]))
    return {"date": top["date"], "articles": top["articles"],
            "ratio_to_baseline": top["ratio_to_baseline"]}


def reaction_series(repo_root: Path, future_id: str) -> dict | None:
    """Every committed reaction night that carried this future, in order.

    Returns None when the future never appeared in a reading — true for
    anything that closed before 2026-08-08, and the honest answer is an
    absent block rather than an empty one that looks measured.
    """
    directory = repo_root / "foreknown" / "reaction" / "readings"
    nights = []
    for path in sorted(directory.glob("*.json")):
        doc = read_json(path, {})
        entry = (doc.get("futures") or {}).get(future_id)
        if entry:
            nights.append(_night(doc, entry))
    if not nights:
        return None

    funded = [n for n in nights if n.get("plan_funded_usd") is not None
              and n.get("has_fts_plan_match")]
    measured: dict = {"nights_watched": len(nights),
                      "attention_peak": _peak(nights)}
    if funded:
        first, last = funded[0], funded[-1]
        measured["money_funded_first_usd"] = first["plan_funded_usd"]
        measured["money_funded_last_usd"] = last["plan_funded_usd"]
        measured["money_funded_delta_usd"] = (last["plan_funded_usd"]
                                              - first["plan_funded_usd"])
        measured["money_requirements_last_usd"] = last["plan_requirements_usd"]
    else:
        # No plan lists any of this future's countries. That is a finding
        # about the register, not a gap in it: on 2026-08-22, 53 of 95 open
        # alert episodes had no plan match at all.
        measured["money_plan_match"] = False
    return {"nights": nights, "measured": measured, "limits": list(LIMITS)}
