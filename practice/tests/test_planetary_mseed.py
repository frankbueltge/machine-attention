"""Planetary Listening miniSEED reader: synthetic records and one committed
excerpt of the publisher's bytes. No network."""

import struct
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from practice.planetary import mseed

ROOT = Path(__file__).resolve().parents[2]
EXCERPT = ROOT / "planetary/probes/2026-10-14/GE.RUE.HHZ/20261008T073232.mseed"


def _record(diffs, x0, xn=None, nsamples=None, start=(2026, 281, 7, 30, 0, 0),
            net=b"GE", sta=b"RUE  ", cha=b"HHZ", encoding=11):
    """One 512-byte big-endian record with a single STEIM2 frame packing
    `diffs` as four 8-bit differences per word (nibble 01)."""
    assert len(diffs) % 4 == 0 and len(diffs) <= 52
    samples = [x0]
    for d in diffs[1:]:
        samples.append(samples[-1] + d)
    if xn is None:
        xn = samples[-1]
    if nsamples is None:
        nsamples = len(diffs)
    year, doy, hh, mm, ss, tenk = start
    header = (b"000001D " + sta + b"  " + cha + net
              + struct.pack(">HHBBBBHHhhBBBBiHH", year, doy, hh, mm, ss, 0, tenk,
                            nsamples, 100, 1, 0, 0, 0, 1, 0, 64, 48))
    blk = struct.pack(">HHBBBB", 1000, 0, encoding, 1, 9, 0)
    words, control = [], 0
    words.append(x0 & 0xFFFFFFFF)
    words.append(xn & 0xFFFFFFFF)
    for w, i in enumerate(range(0, len(diffs), 4), start=3):
        word = 0
        for d in diffs[i:i + 4]:
            word = (word << 8) | (d & 0xFF)
        words.append(word)
        control |= 1 << (30 - 2 * w)
    words += [0] * (15 - len(words))
    frame = struct.pack(">16I", control, *words)
    rec = header + blk + b"\0" * (64 - 56) + frame
    return rec + b"\0" * (512 - len(rec))


def test_header_fields_and_time():
    data = _record([0, 1, -2, 3], 100)
    (rec,) = mseed.records(data)
    assert (rec.network, rec.station, rec.channel) == ("GE", "RUE", "HHZ")
    assert rec.start == datetime(2026, 10, 8, 7, 30, tzinfo=timezone.utc)
    assert rec.sample_rate == 100.0 and rec.length == 512
    assert rec.end() - rec.start == timedelta(seconds=0.04)


def test_steim2_differences_accumulate_from_x0():
    data = _record([5, 1, -2, 3, 127, -128, 0, 0], 100)
    assert mseed.decode(data, mseed.records(data)[0]) == \
        [100, 101, 99, 102, 229, 101, 101, 101]


def test_last_sample_is_checked_against_xn():
    data = _record([0, 1, 1, 1], 0, xn=99)
    with pytest.raises(mseed.MseedError, match="Xn"):
        mseed.decode(data, mseed.records(data)[0])


def test_unsupported_encoding_is_refused():
    data = _record([0, 1, 1, 1], 0, encoding=4)
    with pytest.raises(mseed.MseedError, match="encoding"):
        mseed.decode(data, mseed.records(data)[0])


def test_contiguous_records_join_and_gap_splits():
    a = _record([0, 1, 1, 1], 0, start=(2026, 281, 7, 30, 0, 0))
    b = _record([0, 1, 1, 1], 3, start=(2026, 281, 7, 30, 0, 400))
    c = _record([0, 1, 1, 1], 6, start=(2026, 281, 7, 31, 0, 0))
    traces = mseed.traces(a + b + c)
    assert [len(t.samples) for t in traces] == [8, 4]
    assert traces[0].samples == [0, 1, 2, 3, 3, 4, 5, 6]


def test_not_a_record_is_refused():
    with pytest.raises(mseed.MseedError):
        mseed.records(b"x" * 512)


def test_committed_excerpt_decodes_and_cuts_byte_identically():
    data = EXCERPT.read_bytes()
    recs = mseed.records(data)
    assert len(data) == sum(r.length for r in recs)
    assert {(r.network, r.station, r.channel) for r in recs} == {("GE", "RUE", "HHZ")}
    (trace,) = mseed.traces(data, "HHZ")
    assert len(trace.samples) == sum(r.nsamples for r in recs)
    # Cutting the excerpt over its own span returns the same bytes.
    assert mseed.excerpt(data, recs[0].start, recs[-1].end()) == data
    one = mseed.excerpt(data, recs[3].start, recs[3].start + timedelta(microseconds=1))
    assert one == data[recs[3].offset:recs[3].offset + recs[3].length]
