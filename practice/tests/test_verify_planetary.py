"""The Planetary Listening checks, proven to bite: each test breaks one thing
in a copy of a committed excerpt and asserts the verifier names it."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EXCERPT = REPO / "planetary/probes/2026-10-14/GE.RUE.HHZ/20261008T073232.mseed"


def load_verify():
    spec = importlib.util.spec_from_file_location("verifymod_pl", REPO / "verify.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verifymod_pl"] = mod
    spec.loader.exec_module(mod)
    return mod


verify = load_verify()


def place(tmp: Path, data: bytes, station="GE.RUE.HHZ", name="20261008T073232.mseed"):
    d = tmp / "planetary/probes/2026-10-14" / station
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_bytes(data)


def run(tmp: Path) -> list[str]:
    problems: list[str] = []
    verify.check_planetary(tmp, {}, problems)
    return problems


def test_committed_excerpt_passes(tmp_path):
    place(tmp_path, EXCERPT.read_bytes())
    assert run(tmp_path) == []


def test_citizen_station_is_refused(tmp_path):
    data = bytearray(EXCERPT.read_bytes())
    for off in range(0, len(data), 512):
        data[off + 18:off + 20] = b"AM"
    place(tmp_path, bytes(data))
    assert any("outside the declared theatre" in p for p in run(tmp_path))


def test_truncated_excerpt_is_refused(tmp_path):
    place(tmp_path, EXCERPT.read_bytes()[:-100])
    assert any("record-aligned" in p for p in run(tmp_path))


def test_more_than_four_excerpts_per_station_day(tmp_path):
    for i in range(5):
        place(tmp_path, EXCERPT.read_bytes(), name=f"20261008T07{i:02d}00.mseed")
    assert any("more than 4" in p for p in run(tmp_path))
