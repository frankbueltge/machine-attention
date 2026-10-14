"""Planetary Listening impulse trigger on synthetic traces. No network."""

import random
from datetime import datetime, timezone

from practice.planetary import detect

T0 = datetime(2026, 10, 8, 0, 0, tzinfo=timezone.utc)


def _noise(n, amp=10, seed=1):
    rng = random.Random(seed)
    return [int(rng.gauss(0, amp)) for _ in range(n)]


def test_envelope_is_rms_of_first_differences():
    env = detect.envelope([0, 1, 3, 6, 10], 4.0, bin_s=0.5)
    assert env == [((1 + 4) / 2) ** 0.5, ((9 + 16) / 2) ** 0.5]


def test_quiet_noise_does_not_trigger():
    x = _noise(100 * 600)
    assert detect.triggers(detect.envelope(x, 100.0), T0) == []


def test_impulse_triggers_once_at_its_onset():
    x = _noise(100 * 600)
    for i in range(30000, 30500):        # 5 s burst at t = 300 s
        x[i] += (-1) ** i * 2000
    found = detect.triggers(detect.envelope(x, 100.0), T0)
    assert len(found) == 1
    onset = datetime.fromisoformat(found[0].onset)
    assert abs((onset - T0).total_seconds() - 300) <= 1.0
    assert found[0].peak_ratio > 50
    assert 3 <= found[0].duration_s <= 8


def test_close_impulses_merge_and_far_ones_do_not():
    x = _noise(100 * 900)
    for start in (20000, 22000, 70000):  # 200 s, 220 s, 700 s
        for i in range(start, start + 200):
            x[i] += (-1) ** i * 2000
    found = detect.triggers(detect.envelope(x, 100.0), T0)
    assert len(found) == 2


def test_parameters_are_recorded():
    p = detect.parameters()
    assert p["version"] == detect.DETECT_VERSION
    assert p["trigger_on"] > p["trigger_off"]
