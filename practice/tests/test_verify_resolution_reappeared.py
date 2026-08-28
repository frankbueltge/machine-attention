"""The resolution-vs-status check, proven to bite on the right thing.

futures.py already treats a closed future reappearing in its own feed as a
legitimate difference (REAPPEARED, status flips back to OPEN) — recorded
in verify.py's own VALID_EVENTS, narrated in stage/generate.py and
moments.py. The resolution check must not treat that same reappearance as
a provenance hole: a resolution is a claim about the moment it was written
(resolved_at), not a promise that the future stays closed forever. What the
check must still catch is a resolution with no matching closure in history
at all — a genuine bug, not a later reappearance.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def load_verify():
    spec = importlib.util.spec_from_file_location("verifymod", REPO / "verify.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verifymod"] = mod
    spec.loader.exec_module(mod)
    return mod


verify = load_verify()

FID = "gdacs-tc-1001305"
CLOSED_TS = "2026-08-25T06:04:45+00:00"


def _write(tmp: Path, future: dict, resolution: dict) -> Path:
    registry_dir = tmp / "foreknown"
    (registry_dir / "resolutions").mkdir(parents=True)
    (registry_dir / "registry.json").write_text(
        json.dumps({"futures": {FID: future}}), encoding="utf-8")
    (registry_dir / "resolutions" / f"{FID}.json").write_text(
        json.dumps(resolution), encoding="utf-8")
    return tmp


def _future(*, reappeared: bool) -> dict:
    history = [
        {"ts": "2026-08-22T05:58:52+00:00", "event": "NOTARIZED",
         "snapshot": "foreknown/snapshots/2026-08-22/gdacs.json"},
        {"ts": CLOSED_TS, "event": "CLOSED_BY_SOURCE"},
    ]
    status = "CLOSED_BY_SOURCE"
    if reappeared:
        history.append({"ts": "2026-08-27T05:58:00+00:00", "event": "REAPPEARED",
                        "snapshot": "foreknown/snapshots/2026-08-27/gdacs.json"})
        status = "OPEN"
    return {"id": FID, "hazard": "tropical cyclone", "kind": "ALERT_EPISODE",
            "severity": "Orange", "source": "GDACS", "source_ref": "x",
            "what": "Tropical Cyclone SAUDEL-26", "where": "Japan",
            "window": {"from": "2026-08-18T12:00:00", "to": "2026-08-24T00:00:00"},
            "announced_at": "2026-08-22T05:58:52+00:00",
            "status": status, "history": history}


def _resolution(*, resolved_at: str) -> dict:
    return {"future": FID, "resolved_at": resolved_at, "cold_start": False,
            "verdict": "EPISODE_ENDED", "measured": {}, "evidence": []}


def test_a_future_closed_at_resolution_and_since_reappeared_is_not_a_hole(tmp_path):
    root = _write(tmp_path, _future(reappeared=True), _resolution(resolved_at=CLOSED_TS))
    problems = verify.check(root)
    assert not any("still OPEN" in p for p in problems), problems


def test_a_future_that_never_closed_is_still_a_hole(tmp_path):
    root = _write(tmp_path, _future(reappeared=False), _resolution(resolved_at=CLOSED_TS))
    # Force the corruption this check exists to catch: a resolution filed
    # against a future whose history never actually shows the closure it
    # claims to resolve.
    future = json.loads((root / "foreknown" / "registry.json").read_text())
    future["futures"][FID]["status"] = "OPEN"
    future["futures"][FID]["history"] = future["futures"][FID]["history"][:1]
    (root / "foreknown" / "registry.json").write_text(json.dumps(future), encoding="utf-8")
    problems = verify.check(root)
    assert any(f"resolution {FID}: future is still OPEN" in p for p in problems), problems


def test_a_currently_closed_future_with_a_resolution_is_still_clean(tmp_path):
    root = _write(tmp_path, _future(reappeared=False), _resolution(resolved_at=CLOSED_TS))
    problems = verify.check(root)
    assert not any("still OPEN" in p for p in problems), problems
