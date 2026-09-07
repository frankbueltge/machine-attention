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
          memoryhole=()) -> Path:
    _mkdir_dated(tmp_path / "foreknown" / "snapshots", *foreknown)
    _mkdir_dated(tmp_path / "foreknown" / "reaction" / "snapshots", *reaction)
    _mkdir_dated(tmp_path / "darkocean" / "snapshots", *darkocean)
    _mkfile_dated(tmp_path / "memoryhole" / "readings", *memoryhole)
    return tmp_path


def test_all_registers_current_when_checked_before_the_days_own_writes(tmp_path):
    root = _repo(tmp_path, foreknown=("2026-09-06",), reaction=("2026-09-06",),
                 darkocean=("2026-09-05",), memoryhole=("2026-09-05",))
    result = check(root, today=TODAY)
    assert result["stale"] == []
    assert set(result["checked"]) == {
        "foreknown/snapshots", "foreknown/reaction/snapshots",
        "darkocean/snapshots", "memoryhole/readings"}


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
    # memoryhole/readings never created at all.
    result = check(tmp_path, today=TODAY)
    assert result["stale"] == [{
        "register": "memoryhole/readings",
        "newest_committed_date": None,
        "days_behind": None,
    }]
