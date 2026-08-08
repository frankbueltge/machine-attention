import importlib.util
import json
import shutil
from pathlib import Path

from practice.foreknown import sources
from practice.foreknown.run import run

from .test_foreknown import GDACS_FIXTURE, FakeClient

REPO_ROOT = Path(__file__).parents[2]


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fixture_repo(tmp_path: Path) -> Path:
    shutil.copytree(REPO_ROOT / "stage", tmp_path / "stage",
                    ignore=shutil.ignore_patterns("__pycache__"))
    responses = {
        sources.GDACS_URL: (json.dumps(GDACS_FIXTURE).encode(), 200),
        sources.NHC_URL: (json.dumps({"activeStorms": []}).encode(), 200),
        sources.FTS_PLANS_URL: (json.dumps({"data": []}).encode(), 200),
    }
    run(tmp_path, "2026-08-08", FakeClient(responses))
    return tmp_path


def test_stage_builds_from_real_records_and_verifies_clean(tmp_path):
    root = _fixture_repo(tmp_path)
    stagegen = _load("stagegen_t", root / "stage" / "generate.py")
    stagegen.build(root)
    page = (root / "public" / "index.html").read_text()
    assert "DOLPHIN-26" in page
    assert "warnings under watch" in page.lower()
    # the ten-second rule: plain words before house vocabulary
    assert "Disasters are announced before" in page
    assert (root / "public" / "fonts" / "plexcond600.woff2").exists()

    verify = _load("verify_t", REPO_ROOT / "verify.py")
    assert verify.check(root) == []


def test_verify_catches_tampering_and_stale_stage(tmp_path):
    root = _fixture_repo(tmp_path)
    stagegen = _load("stagegen_t2", root / "stage" / "generate.py")
    stagegen.build(root)
    verify = _load("verify_t2", REPO_ROOT / "verify.py")
    assert verify.check(root) == []

    preserved = root / "foreknown/snapshots/2026-08-08/gdacs.json"
    original = preserved.read_bytes()
    preserved.write_bytes(b"{}")
    assert any("do not match manifest sha256" in p for p in verify.check(root))

    preserved.write_bytes(original)
    (root / "public" / "index.html").write_text("edited by hand")
    assert any("deterministic rebuild" in p for p in verify.check(root))
