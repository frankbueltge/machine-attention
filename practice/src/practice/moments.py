"""Stage moments — what the practice's projects offer the shared stage.

The admission path reserved this substrate contract on paper
(docs/2026-08-08-projekt-aufnahme.md §5: projects deliver the shared stage
moments, not cards); this module is the contract made code, activated by the
first real consumer — the practice's own entrance at
frankbueltge.de/machine-attention (docs/2026-08-09-buehnen-ehrlichkeit-und-
momente.md).

Deliberately thin: a moment is one real, dated event with one plain
statement, one subject and one address to enter — never a figure, never
prose about the practice, never a card. The consumer decides freshness and
display; a moment carries no valid_until, so there is one clock (the
consumer's) instead of two disagreeing.

Only projects with a stage claim produce moments. Dark Ocean may dock only
after its E-experiment review admits it to the stage; the instrument never
docks — no stage claim is its definition.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .export import head_commit
from .foreknown import moments as foreknown_moments
from .preserve import write_json

CONTRACT = "stage-moments/1"

# One entry per project admitted to the stage. Extending this tuple is an
# admission decision, not a refactor — the gate is the E-experiment review.
PRODUCERS = (
    ("foreknown", foreknown_moments.moments),
)

# The stage needs the recent past, not the whole archive; the archive is the
# repository. The newest hundred moments are more nights of material than
# the entrance will ever show at once.
LIMIT = 100


def build(repo_root: Path) -> dict:
    collected: list[dict] = []
    for _, produce in PRODUCERS:
        collected.extend(produce(repo_root))
    collected.sort(key=lambda m: (m["occurred_at"], m["enter"], m["mode"]),
                   reverse=True)
    return {
        "$contract": CONTRACT,
        "generated_from": {"repo": "machine-attention",
                           "commit": head_commit(repo_root)},
        "practice": {"id": "machine-attention", "label": "Machine Attention"},
        "moments": collected[:LIMIT],
    }


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Write the shared stage's moments for frankbueltge.de.")
    parser.add_argument("--repo-root", default=".", type=Path)
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()
    payload = build(root)
    write_json(root / "moments.json", payload)
    print(f"moments.json: {len(payload['moments'])} moments, from "
          f"{payload['generated_from']['commit']}")


if __name__ == "__main__":
    main()
