"""The autonomy protocol: every step is attributed, no aggregate score.

Append-only JSONL. Schema per entry:
ts, step, actor (machine|human), model, tokens, cost, currency,
human_intervention, corrected_by, detail.
"""

from __future__ import annotations

import json
from pathlib import Path

from .preserve import utc_now


def append_line(path: Path, step: str, actor: str, *, model: str | None = None,
                tokens: int = 0, cost: float = 0.0, currency: str = "EUR",
                human_intervention: str | None = None,
                corrected_by: str | None = None,
                detail: dict | None = None) -> dict:
    entry = {
        "ts": utc_now(),
        "step": step,
        "actor": actor,
        "model": model,
        "tokens": tokens,
        "cost": cost,
        "currency": currency,
        "human_intervention": human_intervention,
        "corrected_by": corrected_by,
        "detail": detail or {},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    return entry


def append(repo_root: Path, step: str, actor: str, **kwargs) -> dict:
    """Append to the practice-wide protocol at autonomy/log.jsonl."""
    return append_line(repo_root / "autonomy" / "log.jsonl", step, actor, **kwargs)
