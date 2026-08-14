"""Main-text extraction — the standard library path of the origin's extractor.

Inherited from frankbueltge.de's `redaction/extract.py`, with one deliberate
narrowing: the origin tries trafilatura first and falls back to this tag strip.
Here the fallback IS the extractor. Two reasons, both structural rather than
aesthetic:

  * the practice substrate is dependency-free and keyless, and a nightly run
    that silently changes behaviour with an optional dependency present is not
    a deterministic run;
  * verify.py must recompute every reading from the preserved bytes with the
    standard library alone. A heuristic the verifier cannot restate is a claim
    nobody can check.

The price is a coarser extraction than the origin's — more navigation and
consent residue survives. That is exactly what the validity gate and the prose
filter are for, and the price is named in the method sheet rather than hidden.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser

EXTRACT_VERSION = "extract-v1"

_WS = re.compile(r"\s+")


def collapse(text: str) -> str:
    return _WS.sub(" ", text).strip()


class _Strip(HTMLParser):
    _SKIP = {"script", "style", "nav", "header", "footer", "aside", "noscript",
             "title", "head", "svg", "form"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip = 0
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in self._SKIP:
            self._skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self._buf.append(data)

    def text(self) -> str:
        return collapse(" ".join(self._buf))


def decode(data: bytes) -> str:
    """Bytes to text. The archive serves whatever the publisher served, so the
    declared charset is a guess as often as a fact; utf-8 with replacement is
    the honest default and never raises."""
    for encoding in ("utf-8", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def main_text(html: str) -> str:
    if not html or not html.strip():
        return ""
    parser = _Strip()
    try:
        parser.feed(html)
    except Exception:  # noqa: BLE001 — malformed markup is a fact, not a crash
        pass
    return parser.text()


def text_of(data: bytes) -> str:
    return main_text(decode(data))
