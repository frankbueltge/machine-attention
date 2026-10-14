"""miniSEED 2 reading, standard library only.

Planetary Listening keeps the publisher's original bytes and claims nothing it
cannot point into them. This module does the two things that requires: it
walks a miniSEED 2 byte string record by record (so an excerpt can be cut as a
record-aligned, byte-identical subset of the day file — audit 2026-08-22,
finding 1), and it decodes the STEIM1/STEIM2/INT32 payloads the FDSN data
centres serve. Every STEIM record carries its own last sample (Xn); decoding
checks it, so a decoder bug cannot pass silently as a quiet day.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

ENC_INT32 = 3
ENC_STEIM1 = 10
ENC_STEIM2 = 11


class MseedError(ValueError):
    """The bytes are not a miniSEED 2 record this module can read."""


@dataclass(frozen=True)
class Record:
    offset: int          # byte offset of the record in the input
    length: int          # record length in bytes
    network: str
    station: str
    location: str
    channel: str
    start: datetime      # UTC, time correction applied when not yet applied
    sample_rate: float
    nsamples: int
    encoding: int
    quality: str

    def end(self) -> datetime:
        """Time of the sample after the last one."""
        return self.start + timedelta(seconds=self.nsamples / self.sample_rate)


def _sample_rate(factor: int, multiplier: int) -> float:
    if factor == 0:
        return 0.0
    rate = float(factor) if factor > 0 else -1.0 / factor
    if multiplier > 0:
        rate *= multiplier
    elif multiplier < 0:
        rate /= -multiplier
    return rate


def _header(data: bytes, offset: int) -> tuple[Record, str, int, int]:
    """Parse the fixed header and blockette 1000 at `offset`.
    Returns (record, byte order, data offset, record length)."""
    if len(data) - offset < 48:
        raise MseedError(f"truncated header at {offset}")
    head = data[offset:offset + 48]
    if head[6:7] not in (b"D", b"R", b"Q", b"M"):
        raise MseedError(f"no data record at {offset}")
    order = ">"
    year, = struct.unpack(">H", head[20:22])
    if not 1900 <= year <= 2100:
        order = "<"
        year, = struct.unpack("<H", head[20:22])
        if not 1900 <= year <= 2100:
            raise MseedError(f"implausible start year at {offset}")
    (year, doy, hour, minute, second, _unused, tenk, nsamples, factor,
     multiplier, activity, _io, _dq, _nblk, correction, data_off,
     blk_off) = struct.unpack(order + "HHBBBBHHhhBBBBiHH", head[20:48])
    encoding = None
    reclen = None
    seen = 0
    while blk_off and seen < 16:
        seen += 1
        at = offset + blk_off
        btype, nxt = struct.unpack(order + "HH", data[at:at + 4])
        if btype == 1000:
            encoding = data[at + 4]
            reclen = 1 << data[at + 6]
        blk_off = nxt
    if encoding is None or reclen is None:
        raise MseedError(f"no blockette 1000 at {offset}")
    start = (datetime(year, 1, 1, tzinfo=timezone.utc)
             + timedelta(days=doy - 1, hours=hour, minutes=minute,
                         seconds=second, microseconds=tenk * 100))
    if correction and not activity & 0x02:
        start += timedelta(microseconds=correction * 100)
    record = Record(
        offset=offset, length=reclen,
        network=head[18:20].decode("ascii").strip(),
        station=head[8:13].decode("ascii").strip(),
        location=head[13:15].decode("ascii").strip(),
        channel=head[15:18].decode("ascii").strip(),
        start=start, sample_rate=_sample_rate(factor, multiplier),
        nsamples=nsamples, encoding=encoding,
        quality=head[6:7].decode("ascii"))
    return record, order, data_off, reclen


def records(data: bytes) -> list[Record]:
    """Every record header in `data`, in byte order."""
    out = []
    offset = 0
    while offset < len(data):
        record, _order, _doff, reclen = _header(data, offset)
        out.append(record)
        offset += reclen
    return out


def _signed(value: int, bits: int) -> int:
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def _steim_diffs(payload: bytes, order: str, version: int
                 ) -> tuple[list[int], int, int]:
    """Differences, X0 and Xn from STEIM frames."""
    diffs: list[int] = []
    x0 = xn = 0
    nframes = len(payload) // 64
    for f in range(nframes):
        words = struct.unpack(order + "16I", payload[f * 64:(f + 1) * 64])
        control = words[0]
        for w in range(1, 16):
            nib = (control >> (30 - 2 * w)) & 0x3
            word = words[w]
            if f == 0 and w == 1:
                x0 = _signed(word, 32)
                continue
            if f == 0 and w == 2:
                xn = _signed(word, 32)
                continue
            if nib == 0:
                continue
            if nib == 1:
                diffs.extend(_signed((word >> s) & 0xFF, 8) for s in (24, 16, 8, 0))
            elif version == 1:
                if nib == 2:
                    diffs.extend(_signed((word >> s) & 0xFFFF, 16) for s in (16, 0))
                else:
                    diffs.append(_signed(word, 32))
            else:
                dnib = word >> 30
                if nib == 2:
                    if dnib == 1:
                        diffs.append(_signed(word & 0x3FFFFFFF, 30))
                    elif dnib == 2:
                        diffs.extend(_signed((word >> s) & 0x7FFF, 15) for s in (15, 0))
                    elif dnib == 3:
                        diffs.extend(_signed((word >> s) & 0x3FF, 10) for s in (20, 10, 0))
                    else:
                        raise MseedError("STEIM2: invalid dnib 0 for nibble 2")
                else:
                    if dnib == 0:
                        diffs.extend(_signed((word >> s) & 0x3F, 6) for s in (24, 18, 12, 6, 0))
                    elif dnib == 1:
                        diffs.extend(_signed((word >> s) & 0x1F, 5) for s in (25, 20, 15, 10, 5, 0))
                    elif dnib == 2:
                        diffs.extend(_signed((word >> s) & 0xF, 4) for s in (24, 20, 16, 12, 8, 4, 0))
                    else:
                        raise MseedError("STEIM2: invalid dnib 3 for nibble 3")
    return diffs, x0, xn


def decode(data: bytes, record: Record) -> list[int]:
    """Samples of one record. STEIM payloads are checked against Xn."""
    _rec, order, data_off, reclen = _header(data, record.offset)
    payload = data[record.offset + data_off:record.offset + reclen]
    n = record.nsamples
    if record.encoding == ENC_INT32:
        return list(struct.unpack(order + f"{n}i", payload[:4 * n]))
    if record.encoding not in (ENC_STEIM1, ENC_STEIM2):
        raise MseedError(f"unsupported encoding {record.encoding}")
    diffs, x0, xn = _steim_diffs(payload, order, 1 if record.encoding == ENC_STEIM1 else 2)
    if n == 0:
        return []
    if len(diffs) < n:
        raise MseedError(f"record at {record.offset}: {len(diffs)} differences for {n} samples")
    samples = [x0]
    value = x0
    for d in diffs[1:n]:
        value += d
        samples.append(value)
    if samples[-1] != xn:
        raise MseedError(f"record at {record.offset}: last sample {samples[-1]} != Xn {xn}")
    return samples


@dataclass
class Trace:
    start: datetime
    sample_rate: float
    samples: list[int]


def traces(data: bytes, channel: str | None = None) -> list[Trace]:
    """Decode a byte string into contiguous traces; a gap or overlap larger
    than half a sample starts a new trace (never interpolated)."""
    out: list[Trace] = []
    for rec in records(data):
        if channel and rec.channel != channel:
            continue
        samples = decode(data, rec)
        if not samples:
            continue
        if out:
            last = out[-1]
            expected = last.start + timedelta(seconds=len(last.samples) / last.sample_rate)
            if (last.sample_rate == rec.sample_rate
                    and abs((rec.start - expected).total_seconds()) < 0.5 / rec.sample_rate):
                last.samples.extend(samples)
                continue
        out.append(Trace(rec.start, rec.sample_rate, samples))
    return out


def excerpt(data: bytes, start: datetime, end: datetime) -> bytes:
    """The records overlapping [start, end), cut byte-identically from `data`.
    No byte is rewritten: the excerpt is a subset of the publisher's file."""
    parts = [data[r.offset:r.offset + r.length] for r in records(data)
             if r.start < end and r.end() > start]
    return b"".join(parts)
