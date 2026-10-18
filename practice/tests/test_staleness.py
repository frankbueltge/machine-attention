"""staleness.check() -- sensor-registry-stall.json, promoted 2026-09-07.

The two register-labelling conventions in this repository disagree by one
day (foreknown/snapshots and foreknown/reaction/snapshots label a night by
the day the job ran; darkocean/snapshots and memoryhole/readings label a
night by the day the data is about, since both workflows commit with
`date -u -d 'yesterday'`), so a *healthy* register can sit at 0 or 1 days
behind "yesterday" depending only on which convention it uses -- not a
stall. THRESHOLD_DAYS (1) has to tolerate both without also tolerating a
real gap, which is what these cases check.
"""

from datetime import date
from pathlib import Path

from practice.staleness import check

TODAY = date(2026, 9, 7)  # "yesterday" from TODAY's perspective is 2026-09-06


def _mkdir_dated(base: Path, *dates: str) -> None:
    base.mkdir(parents=True, exist_ok=True)
    for d in dates:
        (base / d).mkdir()


def _mkfile_dated(base: Path, *dates: str) -> None:
    base.mkdir(parents=True, exist_ok=True)
    for d in dates:
        (base / f"{d}.json").write_text("{}", encoding="utf-8")


def _repo(tmp_path: Path, *, foreknown=(), reaction=(), darkocean=(),
          memoryhole=(), planetary=("2026-09-06",)) -> Path:
    _mkdir_dated(tmp_path / "foreknown" / "snapshots", *foreknown)
    _mkdir_dated(tmp_path / "foreknown" / "reaction" / "snapshots", *reaction)
    _mkdir_dated(tmp_path / "darkocean" / "snapshots", *darkocean)
    _mkfile_dated(tmp_path / "memoryhole" / "readings", *memoryhole)
    _mkfile_dated(tmp_path / "planetary" / "readings", *planetary)
    return tmp_path


def test_all_registers_current_when_checked_before_the_days_own_writes(tmp_path):
    root = _repo(tmp_path, foreknown=("2026-09-06",), reaction=("2026-09-06",),
                 darkocean=("2026-09-05",), memoryhole=("2026-09-05",))
    result = check(root, today=TODAY)
    assert result["stale"] == []
    assert set(result["checked"]) == {
        "foreknown/snapshots", "foreknown/reaction/snapshots",
        "darkocean/snapshots", "memoryhole/readings", "planetary/readings"}


def test_one_night_missed_does_not_fire(tmp_path):
    root = _repo(tmp_path, foreknown=("2026-09-05",), reaction=("2026-09-06",),
                 darkocean=("2026-09-05",), memoryhole=("2026-09-05",))
    result = check(root, today=TODAY)
    assert result["stale"] == []


def test_two_nights_missed_fires(tmp_path):
    root = _repo(tmp_path, foreknown=("2026-09-04",), reaction=("2026-09-06",),
                 darkocean=("2026-09-05",), memoryhole=("2026-09-05",))
    result = check(root, today=TODAY)
    assert result["stale"] == [{
        "register": "foreknown/snapshots",
        "newest_committed_date": "2026-09-04",
        "days_behind": 2,
    }]


def test_darkocean_two_nights_behind_its_own_yesterday_labelling_fires(tmp_path):
    root = _repo(tmp_path, foreknown=("2026-09-06",), reaction=("2026-09-06",),
                 darkocean=("2026-09-03",), memoryhole=("2026-09-05",))
    result = check(root, today=TODAY)
    assert [s["register"] for s in result["stale"]] == ["darkocean/snapshots"]
    assert result["stale"][0]["days_behind"] == 3


def test_missing_register_directory_is_maximally_stale(tmp_path):
    _mkdir_dated(tmp_path / "foreknown" / "snapshots", "2026-09-06")
    _mkdir_dated(tmp_path / "foreknown" / "reaction" / "snapshots", "2026-09-06")
    _mkdir_dated(tmp_path / "darkocean" / "snapshots", "2026-09-05")
    _mkfile_dated(tmp_path / "planetary" / "readings", "2026-09-06")
    # memoryhole/readings never created at all.
    result = check(tmp_path, today=TODAY)
    assert result["stale"] == [{
        "register": "memoryhole/readings",
        "newest_committed_date": None,
        "days_behind": None,
    }]


def test_a_retired_project_is_reported_as_retired_never_as_stale(tmp_path):
    # foreknown/RETIRED.json (2026-10-04): the notary stops by design. Its two
    # registers fall behind forever after the last night; the check must say
    # "retired" and keep judging the registers that still run.
    import json
    root = _repo(tmp_path, foreknown=("2026-09-01",), reaction=("2026-09-01",),
                 darkocean=("2026-09-01",), memoryhole=("2026-09-05",))
    (root / "foreknown" / "RETIRED.json").write_text(json.dumps({
        "project": "foreknown", "status": "RETIRED", "last_night": "2026-09-01",
        "decided": "2026-09-02", "record": "docs/x.md", "reason": "r"}),
        encoding="utf-8")
    result = check(root, today=TODAY)
    assert [r["register"] for r in result["retired"]] == [
        "foreknown/snapshots", "foreknown/reaction/snapshots"]
    assert [s["register"] for s in result["stale"]] == ["darkocean/snapshots"]
    assert len(result["checked"]) == 5


def test_planetary_labels_by_run_day_and_fires_after_two_missed_runs(tmp_path):
    # planetary/readings/<run day>.json reads the UTC day before it
    # (2026-10-17.json, commit 934c970, is the reading of 2026-10-16).
    # At the 01:00 check a healthy register is 0 behind; one delayed run is
    # tolerated, two missed runs are a stall.
    base = dict(foreknown=("2026-09-06",), reaction=("2026-09-06",),
                darkocean=("2026-09-05",), memoryhole=("2026-09-05",))
    for newest, stale in (("2026-09-06", False), ("2026-09-05", False),
                          ("2026-09-04", True)):
        root = _repo(tmp_path / newest, planetary=(newest,), **base)
        result = check(root, today=TODAY)
        assert ([s["register"] for s in result["stale"]]
                == (["planetary/readings"] if stale else []))
