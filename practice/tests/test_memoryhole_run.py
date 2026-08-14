"""The nightly Memory Hole run, end to end, against a scripted archive.

The load-bearing test is the last one: the run writes a reading, and the
verifier — a second implementation that shares no code with it — recomputes
that reading from the preserved bytes and finds nothing to complain about. A
reading only agreeing with the code that produced it would prove nothing.
"""

import json
import sys
import urllib.error
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest

from practice.fetch import Client
from practice.memoryhole.run import run

DAY = "2026-08-14"
BEFORE = "20260810120000"
AFTER = "20260814120000"

PAGE_BEFORE = (
    "The strategy commits the federal government to climate neutrality by "
    "2045. It will reduce emissions by 65 percent before the end of the "
    "decade. The measures are financed from the climate and transformation "
    "fund, and the ministry reports on their progress every year. Further "
    "steps are planned for the coming period, and the responsible department "
    "publishes an annual account of what has been achieved so far.")
PAGE_AFTER = PAGE_BEFORE.replace("65 percent", "55 percent")

CHALLENGE_HTML = (
    b"<html><body><p>Verifying your browser before proceeding... "
    b"Incident ID: e4841cb0-dxzu-4858-bcd7-154223367ef4</p></body></html>")

CONTROLS = [f"https://inst.test/service/imprint-{i}.html" for i in range(15)]


def _html(text: str) -> bytes:
    return (f"<html><head><title>x</title></head><body><main><p>{text}</p>"
            f"</main></body></html>").encode("utf-8")


def _cdx(rows: list[list[str]]) -> bytes:
    header = [["timestamp", "original", "statuscode", "digest"]]
    return json.dumps(header + rows).encode("utf-8")


DISCOVERED = ["https://inst.test/a", "https://inst.test/b",
              "https://inst.test/c", "https://inst.test/d"]

HISTORY = {
    "https://inst.test/a": _cdx([
        [BEFORE, "https://inst.test/a", "200", "D1"],
        [AFTER, "https://inst.test/a", "200", "D2"]]),
    "https://inst.test/b": _cdx([
        [BEFORE, "https://inst.test/b", "200", "D3"],
        [AFTER, "https://inst.test/b", "200", "D4"]]),
    "https://inst.test/c": _cdx([
        [BEFORE, "https://inst.test/c", "200", "D5"],
        [AFTER, "https://inst.test/c", "404", "D6"]]),
    "https://inst.test/d": _cdx([
        [BEFORE, "https://inst.test/d", "200", "D7"],
        [AFTER, "https://inst.test/d", "403", "D8"]]),
}
for _url in CONTROLS:
    HISTORY[_url] = _cdx([["20260801090000", _url, "200", "C1"]])

SNAPSHOTS = {
    (BEFORE, "https://inst.test/a"): _html(PAGE_BEFORE),
    (AFTER, "https://inst.test/a"): _html(PAGE_AFTER),
    (BEFORE, "https://inst.test/b"): _html(PAGE_BEFORE),
    (AFTER, "https://inst.test/b"): CHALLENGE_HTML,
}

LIVE = {"https://inst.test/c": 404,   # really gone
        "https://inst.test/d": 200}   # the archive's 403 was weather


class _Response:
    def __init__(self, status, body):
        self.status = status
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _opener(request, timeout=0):
    url = request.full_url
    if "cdx/search/cdx" in url:
        params = parse_qs(urlsplit(url).query)
        target = params["url"][0]
        if "matchType" in params:
            return _Response(200, _cdx(
                [[AFTER, u, "200", f"X{i}"] for i, u in enumerate(DISCOVERED)]))
        return _Response(200, HISTORY.get(target, _cdx([])))
    if "/web/" in url:
        timestamp, original = url.split("/web/")[1].split("id_/", 1)
        return _Response(200, SNAPSHOTS[(timestamp, original)])
    status = LIVE.get(url, 200)
    if status >= 400:
        raise urllib.error.HTTPError(url, status, "", {}, None)
    return _Response(status, b"ok")


def _watchlist() -> dict:
    return {
        "version": "test-2026-08-15",
        "excluded": {"note": "chamber 1", "urls": ["https://www.who.int/x"]},
        "institutions": [{
            "slug": "testinst", "category": "A", "name": "Test institution",
            "host": "inst.test", "strategy": "domain", "query": "inst.test",
            "probe": {"at": "2026-08-15T00:00:00+00:00", "http_status": 200,
                      "rows": 4, "urls": 4, "latency_s": 1.0},
        }],
        "controls": [{"id": f"c{i}", "institution": "testinst",
                      "category": "E", "kind": "imprint", "url": url,
                      "probe": {"at": "2026-08-15T00:00:00+00:00",
                                "http_status": 200, "urls": 1}}
                     for i, url in enumerate(CONTROLS)],
    }


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    (tmp_path / "memoryhole").mkdir()
    (tmp_path / "memoryhole" / "watchlist.json").write_text(
        json.dumps(_watchlist(), ensure_ascii=False), encoding="utf-8")
    return tmp_path


@pytest.fixture()
def reading(repo: Path) -> dict:
    client = Client(opener=_opener, sleep=lambda _s: None, clock=lambda: 0.0)
    run(repo, DAY, client=client, model_key=None)
    return json.loads((repo / "memoryhole" / "readings" / f"{DAY}.json")
                      .read_text(encoding="utf-8"))


def _by_url(reading: dict) -> dict:
    return {entry["url"]: entry for entry in reading["entries"]}


def test_the_four_classes_are_decided_as_the_audit_requires(reading):
    entries = _by_url(reading)
    assert entries["https://inst.test/a"]["class"] == "changed"
    assert entries["https://inst.test/b"]["class"] == "unverifiable"
    assert entries["https://inst.test/c"]["class"] == "gone"
    assert entries["https://inst.test/d"]["class"] == "unverifiable"
    assert entries[CONTROLS[0]]["class"] == "unchanged"


def test_a_challenge_page_is_never_diffed(reading):
    entry = _by_url(reading)["https://inst.test/b"]
    assert entry["reason"] == "gate_after_challenge_fingerprint"
    assert "events" not in entry
    assert entry["gate"]["before"]["valid"] is True
    assert entry["gate"]["after"]["valid"] is False


def test_a_deletion_candidate_that_answers_200_is_not_gone(reading):
    entry = _by_url(reading)["https://inst.test/d"]
    assert entry["recheck"]["class"] == "botwall" or \
        entry["recheck"]["http_code"] == 200
    assert entry["class"] == "unverifiable"
    assert entry["reason"].startswith("deletion_candidate_survived_recheck")


def test_a_deletion_candidate_that_answers_404_is_gone(reading):
    entry = _by_url(reading)["https://inst.test/c"]
    assert entry["recheck"]["class"] == "gone_404"
    assert entry["class"] == "gone"


def test_the_event_is_typed_and_the_passage_is_on_record(reading):
    entry = _by_url(reading)["https://inst.test/a"]
    assert [e["type"] for e in entry["events"]] == ["number_revised"]
    assert "65 percent" in entry["events"][0]["before"]
    assert "55 percent" in entry["events"][0]["after"]


def test_rates_carry_wilson_intervals_and_a_reason_breakdown(reading):
    rates = reading["rates"]
    assert rates["counts"] == {"unchanged": 15, "changed": 1,
                              "unverifiable": 2, "gone": 1}
    assert rates["examined"] == 19
    low, high = rates["changed_ci95"]
    assert low <= rates["changed_rate"] <= high
    assert rates["deletion"]["gone"] == 1
    assert rates["deletion"]["decided"] == 2
    assert set(rates["unverifiable_reasons"]) == {
        "gate_after_challenge_fingerprint",
        "deletion_candidate_survived_recheck_ok"}


def test_the_model_layer_is_off_and_says_so(reading):
    assert reading["model"]["state"] == "off: no key configured"
    assert reading["model"]["cost_usd"] == 0.0


def test_every_preserved_byte_is_manifested(repo, reading):
    manifest = json.loads(
        (repo / "memoryhole" / "snapshots" / DAY / "manifest.json")
        .read_text(encoding="utf-8"))
    listed = {entry["file"] for entry in manifest["entries"]}
    for entry in reading["entries"]:
        if entry.get("history"):
            assert entry["history"] in listed
        for side in ("before", "after"):
            capture = (entry.get("captures") or {}).get(side)
            if capture:
                assert capture["file"] in listed


def test_records_are_append_only(repo, reading):
    client = Client(opener=_opener, sleep=lambda _s: None, clock=lambda: 0.0)
    with pytest.raises(SystemExit):
        run(repo, DAY, client=client, model_key=None)


def test_an_empty_night_is_still_written(repo):
    def empty(request, timeout=0):
        if "cdx/search/cdx" in request.full_url:
            return _Response(200, b"")
        return _Response(200, b"ok")

    client = Client(opener=empty, sleep=lambda _s: None, clock=lambda: 0.0)
    run(repo, "2026-08-13", client=client, model_key=None)
    reading = json.loads(
        (repo / "memoryhole" / "readings" / "2026-08-13.json")
        .read_text(encoding="utf-8"))
    assert reading["institutions"][0]["urls_seen"] == 0
    assert reading["rates"]["counts"]["changed"] == 0
    # the controls are still asked after, and answer nothing
    assert reading["rates"]["examined"] == len(CONTROLS)


def test_the_verifier_recomputes_the_reading_from_the_preserved_bytes(
        repo, reading):
    """The whole point: an independent second implementation, over the bytes."""
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root))
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "verify_module", root / "verify.py")
        verify = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verify)
    finally:
        sys.path.remove(str(root))
    assert verify.check(repo) == []
