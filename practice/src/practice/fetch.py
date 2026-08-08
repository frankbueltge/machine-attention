"""Polite HTTP access with throttling, backoff and URL redaction.

Invariant I6: the archive is public — no query string ever reaches an error
message or run record. Invariant I4: an outage raises SourceUnavailable and is
recorded as an outage; nothing is invented. Generic substrate shared by every
project of the practice.
"""

from __future__ import annotations

import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "machine-attention/0.1 (public research practice)"
MIN_INTERVAL_S = 1.2
BACKOFF_S = (30, 60, 120)
RETRIABLE = {429, 500, 502, 503, 504}


def redacted(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


class SourceUnavailable(Exception):
    """A source could not be read after retries. Message is already redacted."""

    def __init__(self, url: str, detail: str):
        self.url = redacted(url)
        self.detail = detail
        super().__init__(f"{self.url}: {detail}")


class Client:
    """Injectable-for-tests HTTP client (see state-before-interface heritage)."""

    def __init__(self, opener=urllib.request.urlopen, sleep=time.sleep,
                 clock=time.monotonic, timeout: int = 90):
        self._opener = opener
        self._sleep = sleep
        self._clock = clock
        self._timeout = timeout
        self._last_request_at: float | None = None
        self.requests = 0
        self.http_429 = 0

    def _throttle(self) -> None:
        if self._last_request_at is not None:
            elapsed = self._clock() - self._last_request_at
            if elapsed < MIN_INTERVAL_S:
                self._sleep(MIN_INTERVAL_S - elapsed)
        self._last_request_at = self._clock()

    def fetch(self, url: str) -> tuple[bytes, int]:
        """Fetch a document. Returns (bytes, status); retries retriable codes."""
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                                   "Accept": "application/json"})
        attempts = [0.0, *BACKOFF_S]
        last_detail = "unknown error"
        for wait in attempts:
            if wait:
                self._sleep(wait)
            self._throttle()
            self.requests += 1
            try:
                with self._opener(req, timeout=self._timeout) as resp:
                    return resp.read(), resp.status
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    self.http_429 += 1
                last_detail = f"HTTP {e.code}"
                if e.code not in RETRIABLE:
                    return b"", e.code
            except urllib.error.URLError as e:
                last_detail = f"network error: {getattr(e, 'reason', e).__class__.__name__}"
            except TimeoutError:
                last_detail = "timeout"
        raise SourceUnavailable(url, f"{last_detail} after {len(attempts)} attempts")
