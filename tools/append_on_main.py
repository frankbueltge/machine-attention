"""Rebuild a delivery branch's autonomy/log.jsonl as main's log plus the
branch's own new lines — the exact append a fresh branch cut from main would
have made.

Used by tools/sync-discovery.sh after it merges main into a discovery branch.
The union driver (.gitattributes) already keeps both sides' lines, but in
"ours, then theirs" order: on 2026-11-11 that put the discovery line of 07:41
UTC ahead of registry-stall's line of 07:37, a line main already had now moved
in the pull request's diff. Rebuilding from the three versions instead leaves
every line main has where it is and appends only what the branch wrote.

Usage: python tools/append_on_main.py BASE MAIN BRANCH > autonomy/log.jsonl
       (three paths: the log at the merge base, on main, on the branch)
"""
from __future__ import annotations

import sys


def _lines(text: str) -> list[str]:
    return [line if line.endswith("\n") else line + "\n"
            for line in text.splitlines(keepends=True)]


def append_on_main(base: str, main: str, branch: str) -> str:
    base_lines, main_lines, branch_lines = _lines(base), _lines(main), _lines(branch)
    for side, lines in (("main", main_lines), ("branch", branch_lines)):
        if lines[:len(base_lines)] != base_lines:
            raise ValueError(
                f"{side} changed a line the merge base already had; "
                "autonomy/log.jsonl is append-only, so this is for a human")
    on_main = set(main_lines)
    own = [line for line in branch_lines[len(base_lines):] if line not in on_main]
    return "".join(main_lines + own)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    base, on_main, branch = (open(p, encoding="utf-8").read() for p in argv)
    try:
        sys.stdout.write(append_on_main(base, on_main, branch))
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
