"""tools/sync-discovery.sh, tools/append_on_main.py and the workflow that runs them.

Repair of 2026-11-11: the discovery delivery of that morning (PR #115) sat
unmerged because registry-stall had appended to autonomy/log.jsonl on main while
the pass was out. GitHub ignores the union driver when it decides mergeability,
called the pull request conflicting, and started neither ci nor automerge. What is
worth asserting offline: that the log is rebuilt as a pure append on main, that a
rewritten line is refused rather than guessed at, and that the dispatch path from
the sync to ci to automerge is wired.
"""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools" / "sync-discovery.sh"
WORKFLOWS = REPO / ".github" / "workflows"


def _load():
    spec = importlib.util.spec_from_file_location("append_on_main", REPO / "tools" / "append_on_main.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


append_on_main = _load().append_on_main

BASE = '{"step": "memoryhole-run", "ts": "2026-11-10T11:33:25+00:00"}\n'
STALL = '{"step": "registry-stall-check", "ts": "2026-11-11T07:37:32+00:00"}\n'
DISCOVERY = '{"step": "discovery", "ts": "2026-11-11T07:41:13+00:00"}\n'


def test_the_morning_of_2026_11_11_becomes_a_pure_append_on_main():
    """main gained registry-stall's line, the branch its own: main's lines stay where
    they are and only the branch's line follows them."""
    result = append_on_main(BASE, BASE + STALL, BASE + DISCOVERY)
    assert result == BASE + STALL + DISCOVERY


def test_a_line_main_already_has_is_not_written_twice():
    result = append_on_main(BASE, BASE + STALL, BASE + STALL + DISCOVERY)
    assert result == BASE + STALL + DISCOVERY


def test_a_missing_final_newline_does_not_glue_two_lines_together():
    result = append_on_main(BASE, BASE + STALL.rstrip("\n"), BASE + DISCOVERY)
    assert result.splitlines() == [BASE.strip(), STALL.strip(), DISCOVERY.strip()]


@pytest.mark.parametrize("side", ["main", "branch"])
def test_a_rewritten_line_is_refused_not_merged(side):
    edited = BASE.replace("memoryhole-run", "memoryhole-rerun")
    on_main, branch = (edited + STALL, BASE + DISCOVERY) if side == "main" \
        else (BASE + STALL, edited + DISCOVERY)
    with pytest.raises(ValueError, match=side):
        append_on_main(BASE, on_main, branch)


def test_script_exists_and_is_executable():
    assert SCRIPT.is_file()
    assert SCRIPT.stat().st_mode & 0o111, "the workflow invokes it directly"


def test_script_is_syntactically_valid_bash():
    p = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


def test_script_touches_only_conflicting_same_repo_discovery_branches():
    text = SCRIPT.read_text(encoding="utf-8")
    assert 'startswith("discovery/")' in text
    assert "isCrossRepository | not" in text
    assert '"$state" != CONFLICTING' in text


def test_the_sync_reaches_automerge_through_a_ci_dispatch():
    """A push made with the workflow's token starts no workflow; a dispatch does.
    So the script dispatches ci, ci accepts the dispatch with its append-only guard
    still running, and automerge listens to ci whatever started it."""
    assert "gh workflow run ci.yml --ref" in SCRIPT.read_text(encoding="utf-8")
    ci = (WORKFLOWS / "ci.yml").read_text(encoding="utf-8")
    assert "workflow_dispatch:" in ci
    assert "if: github.event_name != 'push'" in ci, "the I3 guard must not skip a dispatched run"
    automerge = (WORKFLOWS / "automerge.yml").read_text(encoding="utf-8")
    assert "workflows: [ci]" in automerge


def test_the_workflow_runs_when_main_moves_and_when_a_delivery_arrives():
    text = (WORKFLOWS / "discovery-sync.yml").read_text(encoding="utf-8")
    assert "pull_request_target:" in text, "a conflicting pull request gets no pull_request run"
    assert "types: [opened, reopened]" in text
    assert "branches: [main]" in text
    assert "ref: main" in text, "the script runs from main, never from the delivery branch"
    assert "run: tools/sync-discovery.sh" in text


@pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")
def test_the_script_end_to_end_against_a_local_origin(tmp_path):
    """The whole sync, offline: a bare repository stands in for GitHub, a stub for
    `gh` answers that the delivery is conflicting and records the dispatch. The
    delivery branch must come back carrying main, its log a pure append on main."""
    origin, work = tmp_path / "origin.git", tmp_path / "work"

    def git(*args, cwd=work):
        return subprocess.run(["git", *args], cwd=cwd, check=True,
                              capture_output=True, text=True).stdout

    git("init", "-q", "--bare", "-b", "main", str(origin), cwd=tmp_path)
    git("clone", "-q", str(origin), str(work), cwd=tmp_path)
    git("config", "user.email", "t@example.invalid")
    git("config", "user.name", "test")
    (work / "tools").mkdir()
    for name in ("append_on_main.py", "sync-discovery.sh"):
        shutil.copy2(REPO / "tools" / name, work / "tools" / name)
    (work / "autonomy").mkdir()
    (work / ".gitattributes").write_text("autonomy/log.jsonl merge=union\n")
    (work / "autonomy" / "log.jsonl").write_text(BASE)
    git("add", "-A")
    git("commit", "-q", "-m", "base")
    git("push", "-q", "origin", "main")

    git("checkout", "-q", "-b", "discovery/2026-11-11")
    with (work / "autonomy" / "log.jsonl").open("a") as fh:
        fh.write(DISCOVERY)
    git("commit", "-q", "-am", "discovery: 2026-11-11")
    git("push", "-q", "origin", "discovery/2026-11-11")

    git("checkout", "-q", "main")
    with (work / "autonomy" / "log.jsonl").open("a") as fh:
        fh.write(STALL)
    git("commit", "-q", "-am", "registry-stall: check of 2026-11-11")
    git("push", "-q", "origin", "main")
    git("branch", "-q", "-D", "discovery/2026-11-11")

    bin_dir, calls = tmp_path / "bin", tmp_path / "gh-calls"
    bin_dir.mkdir()
    (bin_dir / "gh").write_text(
        "#!/usr/bin/env bash\n"
        f'echo "$*" >> "{calls}"\n'
        'case "$1 $2" in\n'
        '  "pr list") echo "115 discovery/2026-11-11" ;;\n'
        '  "pr view") echo CONFLICTING ;;\n'
        "esac\n")
    (bin_dir / "gh").chmod(0o755)

    env = {"PATH": f"{bin_dir}:/usr/bin:/bin:/usr/local/bin", "HOME": str(tmp_path),
           "RUNNER_TEMP": str(tmp_path / "runner")}
    (tmp_path / "runner").mkdir()
    p = subprocess.run(["tools/sync-discovery.sh"], cwd=work, env=env,
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr

    git("fetch", "-q", "origin")
    assert git("show", "origin/discovery/2026-11-11:autonomy/log.jsonl") == BASE + STALL + DISCOVERY
    git("merge-base", "--is-ancestor", "origin/main", "origin/discovery/2026-11-11")
    assert "workflow run ci.yml --ref discovery/2026-11-11" in calls.read_text()
    assert git("worktree", "list").count("\n") == 1, "the temporary worktree is removed"
