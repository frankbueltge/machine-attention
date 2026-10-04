"""The Foreknown retired (2026-10-04): one closing record, read everywhere.

foreknown/RETIRED.json turns the stage into the archive of a finished record,
the export's status into `retired`, the moments' newest entry into the end of
the project — and verify.py into the guard against a silent restart.
"""

import json
from pathlib import Path

from practice import export, moments

from .test_verify_and_stage import _fixture_repo, _load, REPO_ROOT

RECORD = "docs/retired.md"


def _retire(root: Path, last_night: str = "2026-08-08") -> None:
    (root / "docs").mkdir(exist_ok=True)
    (root / RECORD).write_text("why it was retired\n", encoding="utf-8")
    (root / "foreknown" / "RETIRED.json").write_text(json.dumps({
        "project": "foreknown", "status": "RETIRED", "last_night": last_night,
        "decided": "2026-08-09", "decided_by": "the maintainer",
        "record": RECORD, "reason": "The question was put to the wrong clock.",
        "kept": "Nothing is deleted.",
    }), encoding="utf-8")


def test_the_retired_stage_claims_no_present_and_keeps_every_dossier(tmp_path):
    root = _fixture_repo(tmp_path)
    _retire(root)
    stagegen = _load("stagegen_retired", root / "stage" / "generate.py")
    stagegen.build(root)
    page = (root / "public" / "index.html").read_text()
    assert "Then&nbsp;it&nbsp;was&nbsp;stopped." in page
    assert "The question was put to the wrong clock." in page
    assert "Right now" not in page
    assert 'id="countdown"' not in page
    for html in (root / "public").rglob("*.html"):
        text = html.read_text()
        assert "data-to=" not in text and "data-from=" not in text, html.name
    dossiers = list((root / "public" / "future").glob("*.html"))
    assert dossiers
    for dossier in dossiers:
        text = dossier.read_text()
        # the house's globe layer reads these two from every mirrored dossier
        assert "<h1>" in text and 'class="kicker"' in text
    assert "retired 2026-08-09" in (root / "public" / "ledger.html").read_text()

    verify = _load("verify_retired", REPO_ROOT / "verify.py")
    assert verify.check(root) == []


def test_verify_fails_a_night_recorded_after_the_last_one(tmp_path):
    root = _fixture_repo(tmp_path)
    _retire(root, last_night="2026-08-07")
    verify = _load("verify_restart", REPO_ROOT / "verify.py")
    problems = verify.check(root)
    assert any("2026-08-08: recorded after the project was retired" in p
               for p in problems)


def test_verify_fails_a_closing_record_that_points_nowhere(tmp_path):
    root = _fixture_repo(tmp_path)
    _retire(root)
    (root / RECORD).unlink()
    verify = _load("verify_record", REPO_ROOT / "verify.py")
    assert any(f"record {RECORD} does not exist" in p
               for p in verify.check(root))


def test_the_export_says_retired_and_stops_claiming_a_watch(tmp_path):
    root = _fixture_repo(tmp_path)
    before = {f["key"] for f in export.figures(root)}
    assert "futures_under_watch" in before
    _retire(root)
    payload = export.build(root)
    status = {p["id"]: p["status"] for p in payload["projects"]}
    assert status["foreknown"] == "retired"
    keys = {f["key"] for f in payload["figures"]}
    assert not keys & {"futures_under_watch", "futures_window_open",
                       "futures_cold_start", "futures_drift"}
    assert "futures_notarized_total" in keys


def test_the_newest_moment_is_the_end_of_the_project(tmp_path):
    root = _fixture_repo(tmp_path)
    _retire(root)
    newest = moments.build(root)["moments"][0]
    assert newest["mode"] == "retirement"
    assert newest["enter"] == "/attention/"
    assert newest["evidence"] == "foreknown/RETIRED.json"
    assert "stopped recording after 1 night;" in newest["statement"]


def _retire_darkocean(root: Path, last_night: str) -> None:
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "darkocean-retired.md").write_text("why\n", encoding="utf-8")
    (root / "darkocean").mkdir(exist_ok=True)
    (root / "darkocean" / "RETIRED.json").write_text(json.dumps({
        "project": "darkocean", "status": "RETIRED", "last_night": last_night,
        "decided": "2026-08-09", "record": "docs/darkocean-retired.md",
        "reason": "It did not hold the practice's attention."}), encoding="utf-8")


def test_dark_ocean_retires_by_the_same_rule(tmp_path):
    # 2026-10-04: the closing record is per project. Dark Ocean's export status,
    # staleness verdict and verify.py's restart guard follow from its own file.
    from practice.staleness import check
    from datetime import date
    root = _fixture_repo(tmp_path)
    (root / "darkocean" / "continuity").mkdir(parents=True)
    (root / "darkocean" / "continuity" / "2026-08-07.json").write_text(
        json.dumps({"date": "2026-08-07", "answered": 1, "catches": []}), encoding="utf-8")
    _retire_darkocean(root, "2026-08-07")
    status = {p["id"]: p["status"] for p in export.build(root)["projects"]}
    assert status["darkocean"] == "retired"
    assert status["foreknown"] == "running"
    result = check(root, today=date(2026, 9, 1))
    assert "darkocean/snapshots" in [r["register"] for r in result["retired"]]
    verify = _load("verify_darkocean", REPO_ROOT / "verify.py")
    assert [p for p in verify.check(root) if "darkocean" in p] == []
    (root / "darkocean" / "continuity" / "2026-08-08.json").write_text(
        json.dumps({"date": "2026-08-08", "answered": 1, "catches": []}), encoding="utf-8")
    assert any("darkocean/continuity/2026-08-08.json: recorded after the project "
               "was retired" in p for p in verify.check(root))
