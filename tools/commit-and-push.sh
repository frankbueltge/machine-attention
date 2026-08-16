#!/usr/bin/env bash
# Shared commit-and-push handshake for the nightly workflows (sentinel, darkocean,
# memoryhole, anchor): stage, commit, then push with the retries every one of
# them already claimed to do.
#
# Repair, 2026-08-16 (discovery pass): the four workflows each carried an
# identical inline loop —
#   for attempt in 1 2 3 4 5; do
#     if git push; then exit 0; fi
#     git pull --rebase
#   done
# — that never actually got five attempts. GitHub Actions runs `run:` steps
# under `bash -eo pipefail`; a `git pull --rebase` that hits a real conflict
# (not a plain fast-forward) returns non-zero, and `set -e` kills the step on
# the spot, on attempt one, discarding whatever the job had computed. It
# happened for real: memoryhole's second scheduled run (2026-08-16T03:25 UTC,
# GitHub Actions run 31924198695) finished a full night's reading, staged it,
# passed verify.py — then died here, conflicting with foreknown's and
# darkocean's own commits from the same morning in the two files every
# nightly job touches: autonomy/log.jsonl (each job appends one line) and
# anchors/ledger.json (each job's own `tools/anchor.py --register` call
# rewrites it from a fresh scan). memoryhole/readings/ shows the casualty
# directly: no 2026-08-15.json, though .github/workflows/memoryhole.yml runs
# nightly and autonomy/log.jsonl's newest memoryhole-run entry is still dated
# 2026-08-14 as of this fix.
#
# Both conflict files have a structural resolution instead of a line-by-line
# one:
#   - autonomy/log.jsonl is declared `merge=union` in .gitattributes — git's
#     built-in union driver keeps both sides' lines, which is exactly correct
#     for an append-only log where a line, once written, is never edited.
#   - anchors/ledger.json is rebuilt, not merged: tools/anchor.py's own
#     register() docstring says it "may only append" and is idempotent over
#     whatever manifests are on disk. On conflict this script keeps THIS
#     job's own ledger (`git checkout --theirs`, which during a rebase means
#     the commit being replayed, i.e. ours — this preserves any real
#     OpenTimestamps stamping only the anchor job does) and re-runs
#     `--register`, safe to call again, to pick up any other register's
#     night the rebase already merged in cleanly as a new file.
#
# Usage: tools/commit-and-push.sh "<commit message>" [pathspec ...]
# pathspec defaults to "-A" (everything); anchor.yml passes "anchors public"
# to keep its own narrower scope (the record trees stay untouched by design).
set -uo pipefail

msg=$1
shift
paths=("$@")
if [ ${#paths[@]} -eq 0 ]; then
  paths=(-A)
fi

git config user.name "Machine Attention"
git config user.email "attention@machine-attention.invalid"
git add "${paths[@]}"
if git diff --cached --quiet; then
  echo "nothing to commit"
  exit 0
fi
git commit -m "$msg"

for attempt in 1 2 3 4 5; do
  if git push; then
    exit 0
  fi
  if git pull --rebase; then
    continue
  fi
  # A real conflict, not a plain fast-forward reject. Handled only for the
  # one shape seen so far — a lone conflict in the rebuildable ledger — so an
  # unfamiliar conflict still aborts loudly instead of being guessed at.
  conflicted=$(git diff --name-only --diff-filter=U)
  if [ "$conflicted" = "anchors/ledger.json" ]; then
    git checkout --theirs -- anchors/ledger.json
    python tools/anchor.py --register
    git add anchors/ledger.json
    git -c core.editor=true rebase --continue
  else
    echo "unresolved conflict on attempt $attempt:" >&2
    echo "$conflicted" >&2
    git rebase --abort
  fi
done

echo "push failed after 5 attempts" >&2
exit 1
