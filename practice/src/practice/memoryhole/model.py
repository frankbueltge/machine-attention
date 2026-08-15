"""The model layer — behind the rules, capped, batched, and marked as estimate.

Audit condition 4, and Frank's decision of 2026-08-15: yes to a model layer,
hard nightly ceiling of 40 classifications, batch API, `estimated: true` on
every verdict, a committed token and cost trace, honest degradation when the
ceiling is hit.

Three structural facts, none of them decoration:

  * **The rules go first.** Only abstentions reach this module — passages the
    deterministic classifier declined to type. A verdict here is never merged
    into `events`; it is recorded in its own block. That is what makes E-8's
    criterion 5 checkable at all ("no event type may come from the model
    alone") rather than a promise.
  * **Batch, not live.** The batch API is half price and a nightly run has all
    the latency in the world. Prompt caching is deliberately NOT planned for:
    the cacheable prefix minimum on this model sits far above a ~600 token
    classification prompt, so it would silently never cache, and planning a
    saving that cannot occur is the kind of small lie this practice exists to
    avoid.
  * **No key, no drama.** Without `ANTHROPIC_API_KEY` the module returns a
    stated `off` state that lands in the reading, and the night proceeds. The
    record stands without the semantic layer; that is the point of putting the
    rules first.

Raw HTTP rather than the vendor SDK, deliberately: `practice/` is
dependency-free and its verifier is standard library only. A nightly run that
gains a dependency to reach an optional layer is a worse trade than fifty lines
of urllib.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

MODEL_LAYER_VERSION = "model-v1"
MODEL_ID = "claude-haiku-4-5"
PROMPT_VERSION = "memoryhole-classify-v1"
API_BASE = "https://api.anthropic.com/v1/messages/batches"
API_VERSION = "2023-06-01"

# Frank's ceiling, 2026-08-15. Reached is reached: the remainder is reported as
# unclassified, never silently dropped.
NIGHTLY_CAP = 40
MAX_TOKENS = 300
POLL_INTERVAL_S = 20
POLL_TIMEOUT_S = 1800

# Claude Haiku 4.5 list prices per million tokens, batch API at half.
USD_PER_MTOK_IN = 1.00
USD_PER_MTOK_OUT = 5.00
BATCH_DISCOUNT = 0.5

TYPES = ("number_revised", "date_shifted", "negation_flipped",
         "commitment_removed", "attribution_removed", "none")

SYSTEM_PROMPT = (
    "You classify what was done to a sentence on an institutional web page "
    "between two archived captures. You name text operations only. You never "
    "state or imply intent, motive, or wrongdoing.\n"
    "Answer with one JSON object and nothing else:\n"
    '{"type": <one of '
    + "|".join(TYPES) +
    '>, "confidence": <low|medium|high>, "reason": <max 15 words>}\n'
    "Definitions: number_revised — a figure was rewritten; date_shifted — a "
    "date or year was rewritten; negation_flipped — a negation appeared or "
    "disappeared; commitment_removed — a promise or obligation was dropped; "
    "attribution_removed — an ascription to a person or office was dropped; "
    "none — none of these applies."
)


def api_key(env: dict | None = None) -> str | None:
    return (env or os.environ).get("ANTHROPIC_API_KEY") or None


def cost_usd(input_tokens: int, output_tokens: int) -> float:
    raw = (input_tokens / 1_000_000 * USD_PER_MTOK_IN
           + output_tokens / 1_000_000 * USD_PER_MTOK_OUT)
    return round(raw * BATCH_DISCOUNT, 6)


def off(reason: str, considered: int = 0) -> dict:
    """The state that lands in the reading when the layer does not run."""
    return {
        "state": f"off: {reason}",
        "available": False,
        "model": MODEL_ID,
        "prompt_version": PROMPT_VERSION,
        "cap": NIGHTLY_CAP,
        "considered": considered,
        "submitted": 0,
        "unclassified_at_cap": 0,
        "verdicts": [],
        "usage": {"input_tokens": 0, "output_tokens": 0},
        "cost_usd": 0.0,
        "currency": "USD",
    }


def _prompt(before: str | None, after: str | None) -> str:
    return ("BEFORE: " + (before or "(withheld: the passage carries an "
                          "ascription to a person; only its digest is on "
                          "record)")
            + "\nAFTER: " + (after if after is not None else "(removed)"))


def _request(client: object, method: str, url: str, key: str,
             payload: dict | None = None) -> dict:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, data=body, method=method, headers={
        "x-api-key": key,
        "anthropic-version": API_VERSION,
        "content-type": "application/json",
    })
    with client(request, timeout=120) as response:  # type: ignore[operator]
        return json.loads(response.read().decode("utf-8"))


def classify(abstentions: list[dict], *, key: str | None = None,
             opener=urllib.request.urlopen, sleep=time.sleep,
             clock=time.monotonic) -> dict:
    """Submit the abstentions the rules declined to type. Returns the block
    that goes into the reading, whatever happens."""
    considered = len(abstentions)
    key = key or api_key()
    if not key:
        return off("no key configured", considered)
    if not abstentions:
        return {**off("nothing to classify", 0), "state": "idle: no abstentions",
                "available": True}

    batch = abstentions[:NIGHTLY_CAP]
    over_cap = considered - len(batch)

    requests = [{
        "custom_id": item["before_sha256"][:32],
        "params": {
            "model": MODEL_ID,
            "max_tokens": MAX_TOKENS,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user",
                          "content": _prompt(item.get("before"),
                                             item.get("after"))}],
        },
    } for item in batch]

    try:
        created = _request(opener, "POST", API_BASE, key,
                           {"requests": requests})
        batch_id = created["id"]
        started = clock()
        status = created.get("processing_status")
        while status != "ended":
            if clock() - started > POLL_TIMEOUT_S:
                return {**off(f"batch {batch_id} still running at timeout",
                              considered),
                        "available": True, "submitted": len(batch)}
            sleep(POLL_INTERVAL_S)
            status = _request(opener, "GET", f"{API_BASE}/{batch_id}",
                              key).get("processing_status")
        raw = _request(opener, "GET", f"{API_BASE}/{batch_id}/results", key)
    except (urllib.error.URLError, KeyError, json.JSONDecodeError,
            TimeoutError) as err:
        return {**off(f"batch call failed: {err.__class__.__name__}",
                      considered), "available": True}

    verdicts, tokens_in, tokens_out = _read_results(raw)
    return {
        "state": "on",
        "available": True,
        "model": MODEL_ID,
        "prompt_version": PROMPT_VERSION,
        "batch": True,
        "cap": NIGHTLY_CAP,
        "considered": considered,
        "submitted": len(batch),
        "unclassified_at_cap": over_cap,
        "verdicts": verdicts,
        "usage": {"input_tokens": tokens_in, "output_tokens": tokens_out},
        "cost_usd": cost_usd(tokens_in, tokens_out),
        "currency": "USD",
        "note": ("every verdict is an estimate and stands beside the "
                 "deterministic record, never inside it"),
    }


def _read_results(raw) -> tuple[list[dict], int, int]:
    """Batch results arrive as JSONL (and keyed by custom_id in any order).
    Accept either the parsed list or the raw document."""
    if isinstance(raw, dict):
        raw = [raw]
    verdicts: list[dict] = []
    tokens_in = tokens_out = 0
    for entry in raw:
        result = (entry or {}).get("result") or {}
        custom_id = entry.get("custom_id", "")
        if result.get("type") != "succeeded":
            verdicts.append({"custom_id": custom_id, "type": None,
                             "estimated": True,
                             "error": result.get("type", "unknown")})
            continue
        message = result.get("message") or {}
        usage = message.get("usage") or {}
        tokens_in += int(usage.get("input_tokens") or 0)
        tokens_out += int(usage.get("output_tokens") or 0)
        text = "".join(block.get("text", "")
                       for block in message.get("content", [])
                       if block.get("type") == "text")
        verdicts.append({**parse_verdict(text), "custom_id": custom_id,
                         "estimated": True})
    verdicts.sort(key=lambda v: v["custom_id"])
    return verdicts, tokens_in, tokens_out


def parse_verdict(text: str) -> dict:
    """Read one answer. An answer outside the closed vocabulary is recorded as
    unparsed rather than repaired into something the model did not say."""
    try:
        parsed = json.loads(text.strip())
    except (json.JSONDecodeError, AttributeError):
        return {"type": None, "error": "unparsed"}
    kind = parsed.get("type")
    if kind not in TYPES:
        return {"type": None, "error": "out_of_vocabulary"}
    return {"type": kind,
            "confidence": parsed.get("confidence"),
            "reason": str(parsed.get("reason", ""))[:120]}
