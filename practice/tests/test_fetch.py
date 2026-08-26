"""The substrate client's retry ladder — the errors it must absorb.

Written after the memoryhole run of 2026-08-26 died an hour into the reading of
2026-08-25 with `http.client.RemoteDisconnected` and committed nothing. The
ladder was built for exactly that weather (the CDX server was measured at a
19 % 504 rate under concurrency), and `run.py` catches `SourceUnavailable` at
every call site so one unreachable institution costs one `unverifiable` entry
and never the night. But a connection dropped at the response boundary is not a
`URLError`: CPython's `AbstractHTTPHandler.do_open` wraps only `h.request(...)`
in `except OSError -> URLError`, while `h.getresponse()` sits outside that
guard, so the raw `http.client` exception escapes the ladder, escapes every
`except SourceUnavailable` above it, and takes the whole run with it.

These tests hold the ladder to the two shapes a dropped connection takes —
`RemoteDisconnected` (OSError *and* HTTPException) and `IncompleteRead`
(HTTPException only) — and hold the existing HTTP behaviour unchanged.
"""

import http.client
import urllib.error

import pytest

from practice.fetch import Client, SourceUnavailable


class _FakeResponse:
    def __init__(self, status: int, body: bytes):
        self.status = status
        self._body = body

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _client(opener, backoff=(0.0, 0.0)):
    """No real waiting and no real clock — the ladder's shape is what is
    under test, not its timing."""
    return Client(opener=opener, sleep=lambda _s: None, clock=lambda: 0.0,
                  backoff=backoff)


def _raising_then_ok(exc, failures: int):
    """An opener that raises `exc` the first `failures` times, then answers."""
    state = {"calls": 0}

    def opener(request, timeout=0):
        state["calls"] += 1
        if state["calls"] <= failures:
            raise exc
        return _FakeResponse(200, b"the document")

    return opener, state


def test_a_connection_reset_at_the_response_boundary_is_retried():
    """The failure that killed the reading of 2026-08-25. `RemoteDisconnected`
    is a `ConnectionResetError`, hence an `OSError` — but it is NOT a
    `URLError`, so the ladder used to let it through on the first occurrence."""
    exc = http.client.RemoteDisconnected(
        "Remote end closed connection without response")
    opener, state = _raising_then_ok(exc, failures=1)

    body, status = _client(opener).fetch("https://web.archive.org/cdx?x=1")

    assert (body, status) == (b"the document", 200)
    assert state["calls"] == 2, "the reset must cost a retry, not the run"


def test_a_reset_is_not_a_url_error():
    """Guards the reason the extra handler exists: if a future CPython made
    `RemoteDisconnected` a `URLError`, the handler would be redundant — and if
    someone narrows the handler back to `URLError`, this test says why not."""
    assert not issubclass(http.client.RemoteDisconnected, urllib.error.URLError)
    assert issubclass(http.client.RemoteDisconnected, OSError)


def test_a_persistent_reset_becomes_source_unavailable():
    """What every caller in run.py is written to catch. The outage must arrive
    as `SourceUnavailable` — anything else escapes the per-source handlers and
    ends the night instead of marking one source unverifiable."""
    def opener(request, timeout=0):
        raise http.client.RemoteDisconnected("dropped again")

    with pytest.raises(SourceUnavailable) as caught:
        _client(opener).fetch("https://web.archive.org/cdx?secret=value")

    assert "RemoteDisconnected" in str(caught.value)
    assert "secret" not in str(caught.value), "I6: no query string in an error"


def test_a_truncated_body_becomes_source_unavailable():
    """`IncompleteRead` is an `HTTPException` but not an `OSError` — the other
    shape of a connection dying mid-exchange, and the one an `OSError`-only
    handler would still miss."""
    def opener(request, timeout=0):
        raise http.client.IncompleteRead(b"half a doc", 4096)

    with pytest.raises(SourceUnavailable):
        _client(opener).fetch("https://web.archive.org/cdx?x=1")


def test_a_network_error_is_still_retried():
    """Unchanged behaviour: a `URLError` was always absorbed by the ladder."""
    opener, state = _raising_then_ok(urllib.error.URLError("no route"),
                                     failures=1)

    body, _ = _client(opener).fetch("https://web.archive.org/cdx?x=1")

    assert body == b"the document"
    assert state["calls"] == 2


def test_a_non_retriable_status_returns_rather_than_raising():
    """Unchanged behaviour: a 403 is an answer about the resource, not an
    outage, and the caller decides what it means."""
    def opener(request, timeout=0):
        raise urllib.error.HTTPError(request.full_url, 403, "", {}, None)

    body, status = _client(opener).fetch("https://web.archive.org/cdx?x=1")

    assert (body, status) == (b"", 403)


def test_a_retriable_status_exhausts_the_ladder_as_an_outage():
    """Unchanged behaviour: a persistent 504 is the weather the ladder was
    built for, and it ends as a recorded outage."""
    def opener(request, timeout=0):
        raise urllib.error.HTTPError(request.full_url, 504, "", {}, None)

    with pytest.raises(SourceUnavailable) as caught:
        _client(opener).fetch("https://web.archive.org/cdx?x=1")

    assert "HTTP 504" in str(caught.value)
