"""export.figures() recounts darkocean's continuity notary from committed
probe files. `catches` in a continuity probe is a list of catch objects
(darkocean/continuity/<date>.json, `continuity.py`'s own output shape) --
never a count -- so summing it as a number breaks the moment a probe ever
records one. It never had, from 2026-08-11 through 2026-09-02: every
committed probe's `catches` was `[]`, which `int([] or 0)` silently reads
as zero. darkocean/continuity/2026-09-03.json was the first to carry any
(4, all kind gone_from_catalog -- see foreknown/proposals/obs-2026-09-05-1.json),
and every sentinel run since (2026-09-04, 2026-09-05) has crashed inside
`practice.export.figures` with `TypeError: int() argument must be a
string, a bytes-like object or a real number, not 'list'` for exactly this
reason -- reproduced here against the same shape, not just asserted."""

import json
from pathlib import Path

from practice import export
from practice.export import figures


def _repo(tmp_path: Path, continuity_catches: list[list[dict]]) -> Path:
    (tmp_path / "foreknown").mkdir()
    (tmp_path / "foreknown" / "registry.json").write_text(
        json.dumps({"futures": {}}), encoding="utf-8")
    (tmp_path / "foreknown" / "resolutions").mkdir()
    (tmp_path / "foreknown" / "snapshots").mkdir()
    (tmp_path / "darkocean" / "readings").mkdir(parents=True)
    (tmp_path / "darkocean" / "continuity").mkdir(parents=True)
    (tmp_path / "memoryhole" / "readings").mkdir(parents=True)
    for i, catches in enumerate(continuity_catches):
        probe = {"date": f"2026-08-{11 + i:02d}", "answered": 1004,
                 "probed": 1008, "batches": 26, "failures": [],
                 "baselines_established": [], "notes": [],
                 "products_unchanged": 1004 - len(catches),
                 "sources": {}, "generated_at": "2026-08-11T00:00:00+00:00",
                 "catches": catches}
        (tmp_path / "darkocean" / "continuity" / f"2026-08-{11 + i:02d}.json"
         ).write_text(json.dumps(probe), encoding="utf-8")
    return tmp_path


def test_continuity_divergences_counts_every_committed_night_with_zero_catches(tmp_path):
    root = _repo(tmp_path, [[], [], []])
    figs = {f["key"]: f["value"] for f in figures(root)}
    assert figs["darkocean_continuity_divergences"] == 0
    assert figs["darkocean_continuity_rechecks"] == 3 * 1004


def _catch(product: str) -> dict:
    return {"kind": "gone_from_catalog", "id": product, "current": None,
            "preserved": {"online": True}}


def test_continuity_divergences_counts_real_catches_instead_of_crashing(tmp_path):
    root = _repo(tmp_path, [[], [_catch(f"x{i}") for i in range(4)], []])
    figs = {f["key"]: f["value"] for f in figures(root)}
    assert figs["darkocean_continuity_divergences"] == 4


def test_a_product_caught_on_many_nights_is_one_divergence(tmp_path):
    # 2026-10-04 (settling #49): a product gone from the catalog is caught again
    # every night it stays gone. Summing the nightly lists counted 32 products as
    # 614 divergences; the figure counts products.
    root = _repo(tmp_path, [[_catch("a")], [_catch("a"), _catch("b")],
                            [_catch("a"), _catch("b")]])
    figs = {f["key"]: f["value"] for f in figures(root)}
    assert figs["darkocean_continuity_divergences"] == 2


def test_the_running_projects_are_named_and_the_interval_carries_no_figure(tmp_path):
    # 2026-10-18: the export knew four projects, two of them retired, while
    # the practice built The Interval and Planetary Listening every night.
    # Both are named now, without a route. The Interval's criterion C allows
    # the site its name and nothing else before the review, and Planetary
    # Listening's audit keeps everything beyond the name for RUNNING: no
    # figure of either may reach the house, however much their records hold.
    root = _repo(tmp_path, [])
    for project in ("interval", "planetary"):
        (root / project / "readings").mkdir(parents=True)
        (root / project / "readings" / "2026-10-13.json").write_text(
            json.dumps({"date": "2026-10-13"}), encoding="utf-8")
    (root / "interval" / "experiment.json").write_text(
        json.dumps({"schema": "interval-experiment-v1"}), encoding="utf-8")

    payload = export.build(root)
    projects = {p["id"]: p for p in payload["projects"]}
    assert projects["interval"]["site_route"] is None
    assert projects["planetary"]["site_route"] is None
    # The word is read from the committed criteria, not typed.
    assert projects["interval"]["status"] == "e-experiment"
    assert projects["planetary"]["status"] == "v0"
    keys = [f["key"] for f in payload["figures"]]
    assert not [k for k in keys if "interval" in k or "planetary" in k]


def test_the_protocol_counts_say_how_many_model_steps_carry_a_cost(tmp_path):
    # The house's page said every step's cost was measured; the protocol
    # writes a token count or a cost only where a step reported one.
    root = _repo(tmp_path, [])
    steps = [
        {"ts": "2026-10-16T06:37:00+00:00", "step": "a", "model": "m",
         "tokens": 90000, "cost": 0.0},
        {"ts": "2026-10-17T06:40:00+00:00", "step": "b", "model": "m",
         "tokens": 0, "cost": 0.0},
        {"ts": "2026-10-17T07:00:00Z", "step": "c", "model": "m",
         "tokens": None, "cost": 2.99},
        {"ts": "2026-10-18T08:49:11+00:00", "step": "d", "model": None,
         "tokens": 0, "cost": 0.0},
    ]
    (root / "autonomy").mkdir()
    (root / "autonomy" / "log.jsonl").write_text(
        "".join(json.dumps(s) + "\n" for s in steps), encoding="utf-8")
    figs = {f["key"]: f for f in figures(root)}
    assert figs["protocol_steps"]["value"] == 4
    assert figs["protocol_model_steps"]["value"] == 3
    assert figs["protocol_model_steps_with_tokens"]["value"] == 1
    assert figs["protocol_model_steps_with_cost"]["value"] == 1
    # The day of the newest step, so the house can tell the practice moves.
    assert {f["as_of"] for k, f in figs.items() if k.startswith("protocol_")} \
        == {"2026-10-18"}
