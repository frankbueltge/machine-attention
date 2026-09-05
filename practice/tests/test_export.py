"""export.py's darkocean figures, proven against the shape the records actually have.

`darkocean/continuity/*.json` has carried `catches` as a LIST of catch objects
in every one of its nights. export.py read it as a count:

    divergences = sum(int(probe.get("catches") or 0) for probe in probes)

An empty list is falsy, so `[] or 0` gave 0 and the expression looked correct
for the 24 consecutive nights (2026-08-11 through 2026-09-02) in which no
catch existed. It could not have given anything but 0 in that whole stretch —
the figure was not measuring, it was reporting the only value it could reach.

The first real catches landed in darkocean/continuity/2026-09-03.json (4, all
kind gone_from_catalog) and `int([...])` raised, taking the sentinel run down
with it on 2026-09-04 and 2026-09-05.

The count is over DISTINCT products, not over catch events. A product gone
from the catalog is re-caught every night it stays gone: the same four ids
appear in both 2026-09-03 and 2026-09-04. Summing per-night lengths would
report 8 for 4 products and climb by 4 a night while nothing new happened.
Distinct ids give the figure the surrounding comment asks for — a divergence,
once found, stays on the record — without inventing arrivals.
"""
from __future__ import annotations

import json
from pathlib import Path

from practice.export import figures


def write(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def catch(product_id: str) -> dict:
    return {"id": product_id, "kind": "gone_from_catalog",
            "name": f"{product_id}.SAFE", "current": None,
            "first_seen": "2026-08-16", "preserved": {"online": True}}


def repo_with(tmp_path: Path, nights: dict[str, dict]) -> Path:
    """A repo root carrying only what the darkocean figures read."""
    write(tmp_path / "foreknown" / "registry.json", {"futures": {}})
    (tmp_path / "foreknown" / "snapshots" / "2026-09-03").mkdir(parents=True)
    for date, payload in nights.items():
        write(tmp_path / "darkocean" / "continuity" / f"{date}.json", payload)
    return tmp_path


def figure(repo_root: Path, key: str) -> int:
    for item in figures(repo_root):
        if item["key"] == key:
            return item["value"]
    raise AssertionError(f"no figure {key!r}")


def test_a_night_with_no_catches_reports_no_divergence(tmp_path):
    root = repo_with(tmp_path, {
        "2026-09-01": {"answered": 1000, "catches": []},
        "2026-09-02": {"answered": 1002, "catches": []},
    })
    assert figure(root, "darkocean_continuity_divergences") == 0
    assert figure(root, "darkocean_continuity_rechecks") == 2002


def test_a_night_with_catches_is_counted_rather_than_raising(tmp_path):
    root = repo_with(tmp_path, {
        "2026-09-03": {"answered": 1004,
                       "catches": [catch("a"), catch("b"),
                                   catch("c"), catch("d")]},
    })
    assert figure(root, "darkocean_continuity_divergences") == 4


def test_one_product_still_gone_is_not_a_second_divergence(tmp_path):
    """The exact pair that broke the export: four ids, both nights, one finding."""
    four = [catch("a"), catch("b"), catch("c"), catch("d")]
    root = repo_with(tmp_path, {
        "2026-09-03": {"answered": 1004, "catches": list(four)},
        "2026-09-04": {"answered": 1047, "catches": list(four)},
    })
    assert figure(root, "darkocean_continuity_divergences") == 4
    assert figure(root, "darkocean_continuity_rechecks") == 2051


def test_a_genuinely_new_product_raises_the_count(tmp_path):
    root = repo_with(tmp_path, {
        "2026-09-03": {"answered": 1004, "catches": [catch("a"), catch("b")]},
        "2026-09-04": {"answered": 1047, "catches": [catch("a"), catch("b"),
                                                     catch("e")]},
    })
    assert figure(root, "darkocean_continuity_divergences") == 3


def test_the_committed_record_is_read_without_raising():
    """The real nights, against the real files — the case that went red."""
    repo_root = Path(__file__).resolve().parents[2]
    assert figure(repo_root, "darkocean_continuity_divergences") == 4
