"""Impulse detection by symbolic thresholds (no learned classifier — audit
2026-08-22, "Bewusst nicht").

The trace is high-passed by first differences, reduced to an RMS envelope in
fixed bins, and scanned with a classic STA/LTA trigger. Every parameter is a
named constant here and is written into each result, so a reading can be
recomputed from the preserved bytes and the version. A trigger is an
impulse, not a blast: the class is decided later against the declaration,
never here.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

DETECT_VERSION = "stalta-v1"
BIN_S = 0.25        # envelope bin
STA_S = 1.0         # short window
LTA_S = 60.0        # long window, strictly before the short one
TRIGGER_ON = 5.0    # STA/LTA ratio that opens a trigger
TRIGGER_OFF = 1.5   # ratio that closes it
MIN_GAP_S = 60.0    # triggers closer than this merge into one


def parameters() -> dict:
    return {"version": DETECT_VERSION, "bin_s": BIN_S, "sta_s": STA_S,
            "lta_s": LTA_S, "trigger_on": TRIGGER_ON,
            "trigger_off": TRIGGER_OFF, "min_gap_s": MIN_GAP_S}


def envelope(samples: list[int], sample_rate: float,
             bin_s: float = BIN_S) -> list[float]:
    """RMS of first differences per bin. A partial last bin is dropped."""
    per = max(1, int(round(bin_s * sample_rate)))
    out = []
    for i in range(1, len(samples) - per + 1, per):
        acc = 0
        prev = samples[i - 1]
        for x in samples[i:i + per]:
            d = x - prev
            acc += d * d
            prev = x
        out.append(math.sqrt(acc / per))
    return out


@dataclass(frozen=True)
class Trigger:
    onset: str            # ISO UTC of the bin where the ratio crossed TRIGGER_ON
    duration_s: float
    peak_ratio: float
    peak_rms: float       # counts per sample (first-difference RMS)
    background_rms: float  # LTA at onset

    def to_dict(self) -> dict:
        return asdict(self)


def triggers(env: list[float], start: datetime, bin_s: float = BIN_S,
             sta_s: float = STA_S, lta_s: float = LTA_S,
             on: float = TRIGGER_ON, off: float = TRIGGER_OFF,
             min_gap_s: float = MIN_GAP_S) -> list[Trigger]:
    nsta = max(1, int(round(sta_s / bin_s)))
    nlta = max(1, int(round(lta_s / bin_s)))
    # Prefix sums keep the scan linear.
    prefix = [0.0]
    for v in env:
        prefix.append(prefix[-1] + v)

    found: list[list] = []   # [onset_i, end_i, peak_ratio, peak_rms, lta]
    active = None
    for i in range(nlta + nsta, len(env) + 1):
        sta = (prefix[i] - prefix[i - nsta]) / nsta
        lta = (prefix[i - nsta] - prefix[i - nsta - nlta]) / nlta
        if active is not None:
            # While triggered, the background is frozen at onset.
            ratio = sta / active[4] if active[4] > 0 else math.inf
            if ratio > active[2]:
                active[2] = ratio
            active[3] = max(active[3], max(env[i - nsta:i]))
            if ratio < off:
                active[1] = i
                found.append(active)
                active = None
            continue
        if lta <= 0:
            continue
        ratio = sta / lta
        if ratio >= on:
            active = [i - nsta, i, ratio, max(env[i - nsta:i]), lta]
    if active is not None:
        active[1] = len(env)
        found.append(active)

    merged: list[list] = []
    gap_bins = min_gap_s / bin_s
    for t in found:
        if merged and t[0] - merged[-1][1] < gap_bins:
            last = merged[-1]
            last[1] = t[1]
            last[2] = max(last[2], t[2])
            last[3] = max(last[3], t[3])
        else:
            merged.append(list(t))
    return [Trigger(onset=(start + timedelta(seconds=t[0] * bin_s)).isoformat(),
                    duration_s=round((t[1] - t[0]) * bin_s, 2),
                    peak_ratio=round(t[2], 2), peak_rms=round(t[3], 1),
                    background_rms=round(t[4], 1))
            for t in merged]
