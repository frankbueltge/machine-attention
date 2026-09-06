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


def test_continuity_divergences_counts_real_catches_instead_of_crashing(tmp_path):
    catch = {"kind": "gone_from_catalog", "id": "x", "current": None,
             "preserved": {"online": True}}
    root = _repo(tmp_path, [[], [catch, catch, catch, catch], []])
    figs = {f["key"]: f["value"] for f in figures(root)}
    assert figs["darkocean_continuity_divergences"] == 4
