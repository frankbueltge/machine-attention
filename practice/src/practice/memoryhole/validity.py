"""The page validity gate — the one genuinely new discipline of this V0.

Audit findings 1 and 2 are its whole justification. The origin, run unchanged
against the BMWE energy-transition dossier on 2026-08-14, reported 270 removed
tokens at salience 20 — and the "after" snapshot was 118,410 bytes of WAF
challenge page that the archive had stored with HTTP 200. Eight tokens of it:
"Verifying your browser before proceeding... Incident ID: …". Nothing was
removed; nothing was captured. The BaFin probe produced the same class of lie
from the other side: a cookie banner passed the salience gate at 14.

So a capture counts as a page only if all four hold:

  (a) statuscode 200;
  (b) the extracted main text reaches a minimum length;
  (c) it carries no challenge/interstitial fingerprint;
  (d) it is not predominantly consent boilerplate, and it contains at least a
      few sentences the prose filter recognises as prose.

Anything else is class `unverifiable`: counted, disclosed, and NEVER diffed.
The constants are versioned, because a gate whose thresholds move silently is
not a gate.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import prose

GATE_VERSION = "gate-v1"

MIN_TOKENS = 60
MIN_PROSE_SENTENCES = 3
# Below this length a text carrying consent markers is taken to BE the consent
# notice rather than a page that mentions cookies (BaFin: 69 tokens).
CONSENT_MAX_TOKENS = 400
CONSENT_MIN_MARKERS = 2

# Verbatim fingerprints of the interstitials the audit met, plus the common
# siblings of the same WAF families. Matched case-insensitively on the
# extracted text.
CHALLENGE_MARKERS = (
    "verifying your browser",
    "incident id",
    "attention required",
    "just a moment",
    "checking your browser",
    "enable javascript and cookies to continue",
    "please enable cookies",
    "ray id",
    "access denied",
    "request unsuccessful",
    "bot detection",
    "ihre anfrage konnte nicht verarbeitet werden",
    "zugriff verweigert",
)

CONSENT_MARKERS = (
    "cookie",
    "cookies",
    "consent",
    "einwilligung",
    "datenschutzerklärung",
    "privacy policy",
    "matomo",
    "google analytics",
    "tracking",
    "opt-out",
    "opt out",
    "notwendige",
    "essenziell",
    "third-party",
)


@dataclass(frozen=True)
class Verdict:
    valid: bool
    reason: str
    tokens: int = 0
    prose_sentences: int = 0
    markers: tuple[str, ...] = ()


def _sentences(text: str) -> list[str]:
    import re
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def challenge_markers(text: str) -> tuple[str, ...]:
    low = text.lower()
    return tuple(m for m in CHALLENGE_MARKERS if m in low)


def consent_markers(text: str) -> tuple[str, ...]:
    low = text.lower()
    return tuple(m for m in CONSENT_MARKERS if m in low)


def check(text: str, http_status: str | int) -> Verdict:
    """Judge one capture's extracted text. Order matters and is part of the
    version: the cheapest, least arguable reason wins, so a record says
    `status_403` rather than `too_short` about a 146-byte nginx page."""
    status = str(http_status)
    if status != "200":
        return Verdict(False, f"status_{status}")

    tokens = len(text.split())
    found = challenge_markers(text)
    if found:
        return Verdict(False, "challenge_fingerprint", tokens, markers=found)

    if tokens < MIN_TOKENS:
        return Verdict(False, "too_short", tokens)

    consent = consent_markers(text)
    if len(consent) >= CONSENT_MIN_MARKERS and tokens < CONSENT_MAX_TOKENS:
        return Verdict(False, "consent_boilerplate", tokens, markers=consent)

    kept = prose.keep_prose(_sentences(text))
    if len(kept) < MIN_PROSE_SENTENCES:
        return Verdict(False, "not_prose", tokens, prose_sentences=len(kept))

    return Verdict(True, "ok", tokens, prose_sentences=len(kept))
