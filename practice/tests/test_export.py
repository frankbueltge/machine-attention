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


def _catch(product_id: str) -> dict:
    return {"kind": "gone_from_catalog", "id": product_id, "current": None,
            "preserved": {"online": True}}


def test_continuity_divergences_counts_real_catches_instead_of_crashing(tmp_path):
    # Four catches on one night are four products, so the fixture carries four
    # distinct ids -- the shape darkocean/continuity/2026-09-03.json has. The
    # earlier fixture repeated one id four times, which only read as 4 because
    # the figure was summing list lengths and never looked at what was in them.
    four = [_catch("a"), _catch("b"), _catch("c"), _catch("d")]
    root = _repo(tmp_path, [[], four, []])
    figs = {f["key"]: f["value"] for f in figures(root)}
    assert figs["darkocean_continuity_divergences"] == 4


def test_a_product_still_gone_is_not_a_fresh_divergence_each_night(tmp_path):
    """The record's own case: one finding re-caught, not new findings.

    A product gone from the catalog is caught again every night it stays gone.
    The same four ids stand in 2026-09-03, -04 and -05, so summing per-night
    lengths reports 12 for 4 products and climbs by 4 a night while nothing
    new has happened. The figure counts distinct products.
    """
    four = [_catch("a"), _catch("b"), _catch("c"), _catch("d")]
    root = _repo(tmp_path, [list(four), list(four), list(four)])
    figs = {f["key"]: f["value"] for f in figures(root)}
    assert figs["darkocean_continuity_divergences"] == 4


def test_a_genuinely_new_product_raises_the_count(tmp_path):
    root = _repo(tmp_path, [[_catch("a"), _catch("b")],
                            [_catch("a"), _catch("b"), _catch("e")]])
    figs = {f["key"]: f["value"] for f in figures(root)}
    assert figs["darkocean_continuity_divergences"] == 3


def test_catches_without_an_id_are_not_collapsed_into_one(tmp_path):
    """No committed probe lacks an id; if one ever does, it must not vanish."""
    bare = [{"kind": "gone_from_catalog", "current": None, "name": "one"},
            {"kind": "gone_from_catalog", "current": None, "name": "two"}]
    root = _repo(tmp_path, [bare])
    figs = {f["key"]: f["value"] for f in figures(root)}
    assert figs["darkocean_continuity_divergences"] == 2


def test_the_committed_record_agrees_with_an_independent_count():
    """The real files, counted here without going through export.py.

    Deliberately not a literal: the continuity register gains a night every
    time the notary runs, and a figure pinned to today's number is a test that
    fails on a night when nothing is wrong. The expectation is derived from the
    committed probes each run, the way the register's own ledger is.
    """
    repo_root = Path(__file__).resolve().parents[2]
    probes = sorted((repo_root / "darkocean" / "continuity").glob("*.json"))
    ids: set[str] = set()
    events = 0
    for path in probes:
        for entry in json.loads(path.read_text(encoding="utf-8")).get("catches") or []:
            ids.add(str(entry.get("id")))
            events += 1
    figs = {f["key"]: f["value"] for f in figures(repo_root)}
    assert figs["darkocean_continuity_divergences"] == len(ids)
    # While the record carries a product caught on more than one night, summing
    # per-night lengths and counting products give different answers, so this
    # also fails if the figure ever goes back to summing.
    if events > len(ids):
        assert figs["darkocean_continuity_divergences"] < events
