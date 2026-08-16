"""tools/commit-and-push.sh and the .gitattributes fix it depends on.

Repair of 2026-08-16 (discovery pass): the four nightly workflows each carried an
identical inline retry loop that never actually retried, because GitHub Actions runs
`run:` steps under `bash -eo pipefail` and a `git pull --rebase` that hits a real
conflict kills the step on attempt one via `set -e`. It happened for real on
memoryhole's second scheduled run (2026-08-16T03:25 UTC): a full night's reading was
computed and staged, then lost when the commit step died on a rebase conflict against
foreknown's and darkocean's own commits from the same morning. See the script's own
docstring for the fix. What is worth asserting offline, without spinning up GitHub
Actions: that the union merge driver this fix leans on actually resolves the exact
concurrent-append shape that caused the loss, and that the script itself is at least
syntactically sound bash.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools" / "commit-and-push.sh"


def test_script_exists_and_is_executable():
    assert SCRIPT.is_file()
    assert SCRIPT.stat().st_mode & 0o111, "the workflows invoke it directly, not via `bash tools/...`"


def test_script_is_syntactically_valid_bash():
    p = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr


def test_gitattributes_declares_union_merge_for_the_append_only_log():
    """The other half of the fix: without this, the script's rebase-conflict handling
    never even gets called for autonomy/log.jsonl, because every nightly job's line
    lands there too, not only in anchors/ledger.json."""
    attrs = (REPO / ".gitattributes").read_text(encoding="utf-8")
    assert "autonomy/log.jsonl merge=union" in attrs


@pytest.mark.skipif(shutil.which("git") is None, reason="git not on PATH")
def test_union_merge_resolves_two_branches_each_appending_a_line(tmp_path):
    """The exact shape of tonight's conflict, reproduced offline: two commits that each
    append one different line to the end of the same file. Git's default line-based
    merge treats both as "insert after the last line" and refuses to reconcile them —
    proven live by GitHub Actions run 31924198695 (memoryhole, 2026-08-16). With the
    `merge=union` attribute this repository now declares for autonomy/log.jsonl, the
    same rebase must resolve on its own and keep both lines."""
    repo = tmp_path / "repo"
    repo.mkdir()

    def git(*args):
        return subprocess.run(["git", *args], cwd=repo, check=True,
                               capture_output=True, text=True)

    git("init", "-q", "-b", "main")
    git("config", "user.email", "a@example.invalid")
    git("config", "user.name", "test")
    (repo / ".gitattributes").write_text("log.jsonl merge=union\n")
    (repo / "log.jsonl").write_text('{"n": 1}\n')
    git("add", "-A")
    git("commit", "-q", "-m", "base")

    git("checkout", "-q", "-b", "feature")
    with (repo / "log.jsonl").open("a") as fh:
        fh.write('{"n": 2, "who": "feature"}\n')
    git("commit", "-q", "-am", "feature appends")

    git("checkout", "-q", "main")
    with (repo / "log.jsonl").open("a") as fh:
        fh.write('{"n": 3, "who": "main"}\n')
    git("commit", "-q", "-am", "main appends")

    git("checkout", "-q", "feature")
    result = subprocess.run(["git", "rebase", "main"], cwd=repo,
                             capture_output=True, text=True)
    assert result.returncode == 0, (
        "rebase should resolve on its own via the union driver, not conflict:\n"
        + result.stdout + result.stderr
    )
    lines = (repo / "log.jsonl").read_text().splitlines()
    assert '{"n": 1}' in lines
    assert '{"n": 2, "who": "feature"}' in lines
    assert '{"n": 3, "who": "main"}' in lines
    status = git("status", "--short").stdout
    assert status.strip() == "", "the rebase must leave a clean tree, not a stalled conflict"
