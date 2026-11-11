#!/usr/bin/env bash
# Keeps open discovery/* pull requests mergeable when main moves under them.
# Run by .github/workflows/discovery-sync.yml.
#
# Repair, 2026-11-11: the discovery delivery of that morning (PR #115) sat
# unmerged for two hours. registry-stall, scheduled for 01:00 UTC but started
# by GitHub only at 07:37, appended its line to autonomy/log.jsonl on main;
# the discovery branch, cut before that, appended its own line and opened the
# pull request at 07:42. On a runner that is no conflict at all —
# .gitattributes declares the log `merge=union` — but GitHub's mergeability
# check ignores merge drivers, so the pull request showed as conflicting.
# GitHub starts no pull_request workflow on a conflicting pull request, so ci
# never ran and automerge never fired. The two nights before, the jobs had
# landed the other way round.
#
# For each open discovery/* pull request GitHub calls CONFLICTING, this script
# merges main into the branch (the union driver applies here), rebuilds the
# log as main's lines plus the branch's own (tools/append_on_main.py), pushes,
# and dispatches ci on the branch: a push made with the workflow's token
# starts no workflow by itself, a workflow_dispatch does. ci green → merged,
# by automerge or by this job, whichever is first. A conflict in any other file is left alone and reported — that
# one is for a human.
#
# The branch is worked on in a separate worktree, so nothing from it is ever
# executed: this script and append_on_main.py run from main's checkout.
set -uo pipefail

log=autonomy/log.jsonl
tmp=${RUNNER_TEMP:-$(mktemp -d)}

git config user.name "Machine Attention"
git config user.email "attention@machine-attention.invalid"
git fetch --quiet origin main

prs=$(gh pr list --state open --json number,headRefName,isCrossRepository \
  --jq '.[] | select(.isCrossRepository | not)
             | select(.headRefName | startswith("discovery/"))
             | "\(.number) \(.headRefName)"')
if [ -z "$prs" ]; then
  echo "no open discovery pull request"
  exit 0
fi

status=0
while read -r number branch <&3; do
  # GitHub computes mergeability lazily after main moves; ask until it answers.
  state=UNKNOWN
  for attempt in 1 2 3 4 5 6 7 8 9 10; do
    state=$(gh pr view "$number" --json mergeable --jq .mergeable)
    [ "$state" != UNKNOWN ] && break
    sleep 6
  done
  if [ "$state" != CONFLICTING ]; then
    echo "#$number ($branch): $state, nothing to do"
    continue
  fi

  dir="$tmp/sync-$number"
  git fetch --quiet origin "$branch"
  git worktree add --quiet -B "$branch" "$dir" "origin/$branch"
  base=$(git merge-base origin/main "origin/$branch")

  if ! git -C "$dir" merge --quiet --no-ff --no-edit -m "Merge main into $branch" origin/main; then
    echo "::warning::#$number ($branch) conflicts beyond the append-only log, left for a human:"
    git -C "$dir" diff --name-only --diff-filter=U
    git -C "$dir" merge --abort
    git worktree remove --force "$dir"
    status=1
    continue
  fi

  if ! python3 tools/append_on_main.py \
      <(git show "$base:$log") <(git show "origin/main:$log") \
      <(git show "origin/$branch:$log") > "$tmp/log-$number"; then
    echo "::warning::#$number ($branch): $log is not a pure append, left for a human"
    git worktree remove --force "$dir"
    status=1
    continue
  fi
  cp "$tmp/log-$number" "$dir/$log"
  git -C "$dir" add "$log"
  git -C "$dir" commit --quiet --amend --no-edit

  git -C "$dir" push --quiet origin "HEAD:$branch"
  git worktree remove --force "$dir"

  # automerge listens to ci, but GitHub does not document whether a ci run
  # started with the workflow's own token wakes a workflow_run listener. So
  # this job waits for that run itself and merges on green: the same gate.
  since=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  gh workflow run ci.yml --ref "$branch"
  run=""
  for attempt in $(seq 1 20); do
    run=$(gh run list --workflow ci.yml --branch "$branch" --event workflow_dispatch \
      --json databaseId,createdAt \
      --jq "[.[] | select(.createdAt >= \"$since\")][0].databaseId // empty")
    [ -n "$run" ] && break
    sleep 6
  done
  if [ -z "$run" ]; then
    echo "::warning::#$number ($branch): main merged in, but the dispatched ci run never showed"
    status=1
    continue
  fi
  if gh run watch "$run" --exit-status > /dev/null; then
    gh pr merge "$number" --squash --delete-branch \
      || echo "#$number already merged (automerge was faster)"
    echo "#$number ($branch): main merged in, ci green, merged"
  else
    echo "::warning::#$number ($branch): main merged in, ci red, left for a human"
    status=1
  fi
done 3<<< "$prs"

exit $status
