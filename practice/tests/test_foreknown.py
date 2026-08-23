import json
from pathlib import Path

import pytest

from practice.foreknown import sources
from practice.foreknown.futures import (COLD_START_OVERDUE, DRIFT_OVERDUE,
                                        DROUGHT_FROZEN, DROUGHT_IRREGULAR,
                                        DROUGHT_ROLLING, drought_window_class,
                                        drought_window_crossings, is_overdue,
                                        overdue_kind, update_registry,
                                        window_to_at_notarization)
from practice.foreknown.run import run
from practice.preserve import read_json


GDACS_FIXTURE = {"features": [
    {"properties": {"eventid": 1001297, "eventtype": "TC", "alertlevel": "Orange",
                    "name": "Tropical Cyclone DOLPHIN-26",
                    "country": "Marshall Islands, Japan",
                    "affectedcountries": [{"iso3": "MHL"}, {"iso3": "JPN"}],
                    "fromdate": "2026-07-27T00:00:00",
                    "todate": "2026-08-08T12:00:00",
                    "url": {"report": "https://www.gdacs.org/report?eventid=1001297"}}},
    {"properties": {"eventid": 1027450, "eventtype": "DR", "alertlevel": "Orange",
                    "name": "Drought in Ethiopia, Kenya, Somalia",
                    "country": "Ethiopia, Kenya, Somalia",
                    "affectedcountries": [{"iso3": "ETH"}, {"iso3": "KEN"}],
                    "fromdate": "2026-04-21T00:00:00",
                    "todate": "2026-08-06T00:00:00", "url": "plain-string"}},
]}


def test_gdacs_extraction_is_deterministic_and_org_level():
    futures = sources.gdacs_futures(GDACS_FIXTURE)
    assert [f["id"] for f in futures] == ["gdacs-tc-1001297", "gdacs-dr-1027450"]
    tc = futures[0]
    assert tc["kind"] == "ALERT_EPISODE" and tc["hazard"] == "tropical cyclone"
    assert tc["window"]["to"] == "2026-08-08T12:00:00"
    assert tc["iso3"] == ["JPN", "MHL"]


def test_nhc_empty_list_is_the_honest_quiet_state():
    assert sources.nhc_futures({"activeStorms": []}) == []


def test_registry_notarize_revise_close_lifecycle():
    registry = {"futures": {}}
    observed = sources.gdacs_futures(GDACS_FIXTURE)
    anchors = {"GDACS": "foreknown/snapshots/2026-08-08/gdacs.json"}

    summary = update_registry(registry, observed, anchors)
    assert len(summary["notarized"]) == 2
    tc = registry["futures"]["gdacs-tc-1001297"]
    announced_at = tc["announced_at"]
    assert tc["history"][0]["event"] == "NOTARIZED"

    # night 2: the cyclone's window is extended → REVISED, announced_at fixed
    revised = json.loads(json.dumps(GDACS_FIXTURE))
    revised["features"][0]["properties"]["todate"] = "2026-08-10T12:00:00"
    summary = update_registry(registry, sources.gdacs_futures(revised), anchors)
    assert summary["revised"] == ["gdacs-tc-1001297"]
    tc = registry["futures"]["gdacs-tc-1001297"]
    assert tc["announced_at"] == announced_at
    changes = tc["history"][-1]["changes"]
    assert changes["window"]["from"]["to"] == "2026-08-08T12:00:00"

    # night 3: the cyclone leaves the feed → CLOSED_BY_SOURCE
    only_drought = {"features": [GDACS_FIXTURE["features"][1]]}
    summary = update_registry(registry, sources.gdacs_futures(only_drought), anchors)
    assert summary["closed"] == ["gdacs-tc-1001297"]
    assert registry["futures"]["gdacs-tc-1001297"]["status"] == "CLOSED_BY_SOURCE"


def test_absent_source_closes_nothing():
    """A source outage proves nothing (I4): its futures stay OPEN."""
    registry = {"futures": {}}
    update_registry(registry, sources.gdacs_futures(GDACS_FIXTURE),
                    {"GDACS": "a"})
    summary = update_registry(registry, [], {})  # nothing observed, no anchors
    assert summary["closed"] == []
    assert registry["futures"]["gdacs-tc-1001297"]["status"] == "OPEN"


def test_overdue_is_a_flag_not_a_closure():
    registry = {"futures": {}}
    update_registry(registry, sources.gdacs_futures(GDACS_FIXTURE), {"GDACS": "a"})
    drought = registry["futures"]["gdacs-dr-1027450"]
    assert is_overdue(drought, "2026-08-08T00:00:00+00:00")
    assert drought["status"] == "OPEN"


def test_overdue_splits_cold_start_from_drift():
    """The machine's proposal sensor-cold-start-overdue-drift: an overdue
    flag that cannot tell an artefact of when observation began from a
    warning that outlived its own window states nothing."""
    registry = {"futures": {}}
    update_registry(registry, sources.gdacs_futures(GDACS_FIXTURE), {"GDACS": "a"})

    # The drought's window ended 2026-08-06, before we ever saw it.
    drought = registry["futures"]["gdacs-dr-1027450"]
    drought["announced_at"] = "2026-08-08T05:45:00+00:00"
    drought["history"][0]["ts"] = drought["announced_at"]
    assert overdue_kind(drought, "2026-08-09T00:00:00+00:00") == COLD_START_OVERDUE

    # The cyclone was inside its window when notarized and outlived it.
    cyclone = registry["futures"]["gdacs-tc-1001297"]
    cyclone["announced_at"] = "2026-08-01T05:45:00+00:00"
    cyclone["history"][0]["ts"] = cyclone["announced_at"]
    assert overdue_kind(cyclone, "2026-08-09T00:00:00+00:00") == DRIFT_OVERDUE
    assert overdue_kind(cyclone, "2026-08-08T00:00:00+00:00") is None


def test_a_revised_window_does_not_relabel_a_cold_start():
    """Cold start is decided against the window the warning was announced
    with — revisions are appended, so the original stays readable (I3)."""
    registry = {"futures": {}}
    update_registry(registry, sources.gdacs_futures(GDACS_FIXTURE), {"GDACS": "a"})
    drought = registry["futures"]["gdacs-dr-1027450"]
    drought["announced_at"] = "2026-08-08T05:45:00+00:00"
    drought["history"][0]["ts"] = drought["announced_at"]

    extended = json.loads(json.dumps(GDACS_FIXTURE))
    extended["features"][1]["properties"]["todate"] = "2026-08-20T00:00:00"
    update_registry(registry, sources.gdacs_futures(extended), {"GDACS": "a"})
    assert window_to_at_notarization(drought) == "2026-08-06T00:00:00"
    assert overdue_kind(drought, "2026-08-25T00:00:00+00:00") == COLD_START_OVERDUE


def _drought(window_to, history):
    return {"hazard": "drought", "status": "OPEN",
           "window": {"to": window_to}, "history": history}


_ROLLING_HISTORY = [
    {"ts": "2026-08-08T17:40:00+00:00", "event": "NOTARIZED"},
    {"ts": "2026-08-09T06:27:00+00:00", "event": "REVISED",
     "changes": {"window": {"from": {"to": "2026-08-06T00:00:00"},
                            "to": {"to": "2026-08-07T00:00:00"}}}},
    {"ts": "2026-08-10T05:57:00+00:00", "event": "REVISED",
     "changes": {"window": {"from": {"to": "2026-08-07T00:00:00"},
                            "to": {"to": "2026-08-08T00:00:00"}}}},
]


def test_drought_window_class_needs_two_nights_before_deciding():
    """The proposal's own bar: frozen needs 'at least two consecutive
    preserved snapshots' — a single night is not yet a difference."""
    drought = _drought("2026-04-20T00:00:00",
                       [{"ts": "2026-08-08T17:40:00+00:00", "event": "NOTARIZED"}])
    assert drought_window_class(drought, "2026-08-08") is None


def test_drought_window_class_frozen_when_window_to_never_changes():
    drought = _drought("2026-04-20T00:00:00",
                       [{"ts": "2026-08-08T17:40:00+00:00", "event": "NOTARIZED"}])
    state = drought_window_class(drought, "2026-08-09")
    assert state == {"class": DROUGHT_FROZEN, "nights_observed": 2,
                     "window_to": "2026-04-20T00:00:00"}


def test_drought_window_class_rolling_when_window_to_advances_a_day_a_night():
    drought = _drought("2026-08-08T00:00:00", _ROLLING_HISTORY)
    state = drought_window_class(drought, "2026-08-10")
    assert state == {"class": DROUGHT_ROLLING, "nights_observed": 3,
                     "window_to": "2026-08-08T00:00:00"}


def test_drought_window_class_flags_a_stalled_rolling_drought_as_irregular():
    """A night with no REVISED window event is still an observation: a
    rolling drought whose window.to stops advancing must show up as a
    broken step, not read as an unremarkable silence."""
    drought = _drought("2026-08-08T00:00:00", _ROLLING_HISTORY)
    state = drought_window_class(drought, "2026-08-11")
    assert state["class"] == DROUGHT_IRREGULAR
    assert state["since"] == "2026-08-11"
    assert state["day_delta"] == 1 and state["todate_delta"] == 0


def test_drought_window_class_ignores_non_drought_and_closed_futures():
    cyclone = {"hazard": "tropical cyclone", "status": "OPEN",
              "window": {"to": "2026-04-20T00:00:00"},
              "history": [{"ts": "2026-08-08T17:40:00+00:00", "event": "NOTARIZED"}]}
    assert drought_window_class(cyclone, "2026-08-09") is None
    closed = _drought("2026-04-20T00:00:00",
                      [{"ts": "2026-08-08T17:40:00+00:00", "event": "NOTARIZED"}])
    closed["status"] = "CLOSED_BY_SOURCE"
    assert drought_window_class(closed, "2026-08-09") is None


def test_drought_window_crossings_catches_a_rolling_drought_that_stalls():
    """Implements the machine's own proposal
    sensor-drought-window-class-crossing.json: the crossing it exists to
    catch, recomputed statelessly from the committed history alone."""
    registry = {"futures": {"gdacs-dr-1000001": _drought(
        "2026-08-08T00:00:00", _ROLLING_HISTORY)}}
    assert drought_window_crossings(registry, "2026-08-10") == []
    crossings = drought_window_crossings(registry, "2026-08-11")
    assert crossings == [{"future": "gdacs-dr-1000001",
                          "from_class": DROUGHT_ROLLING,
                          "to_class": DROUGHT_IRREGULAR,
                          "run_date": "2026-08-11"}]


class FakeClient:
    def __init__(self, responses):
        self._responses = responses
        self.requests = 0
        self.http_429 = 0

    def fetch(self, url):
        self.requests += 1
        return self._responses.get(url, (b"", 404))


def test_notary_run_end_to_end(tmp_path: Path):
    responses = {
        sources.GDACS_URL: (json.dumps(GDACS_FIXTURE).encode(), 200),
        sources.NHC_URL: (json.dumps({"activeStorms": []}).encode(), 200),
        sources.NWS_URL: (json.dumps({"features": []}).encode(), 200),
        sources.FTS_PLANS_URL: (json.dumps({"data": []}).encode(), 200),
    }
    summary = run(tmp_path, "2026-08-08", FakeClient(responses))
    assert summary["notarized"] == 2 and summary["failures"] == 0

    manifest = read_json(tmp_path / "foreknown/snapshots/2026-08-08/manifest.json")
    # Three warning feeds and the funding axis, since the third source was
    # added on 2026-08-22.
    assert len(manifest["entries"]) == 4
    registry = read_json(tmp_path / "foreknown/registry.json")
    anchor = registry["futures"]["gdacs-tc-1001297"]["history"][0]["snapshot"]
    assert anchor == "foreknown/snapshots/2026-08-08/gdacs.json"
    log = (tmp_path / "autonomy/log.jsonl").read_text().strip().splitlines()
    assert json.loads(log[-1])["step"] == "foreknown-notary-run"

    with pytest.raises(SystemExit):
        run(tmp_path, "2026-08-08", FakeClient(responses))


# --- the machine's proposal sensor-primary-iso3-gap ----------------------

GDACS_PRIMARY_GAP = {"features": [
    {"properties": {
        "eventid": 1001297, "eventtype": "TC", "alertlevel": "Orange",
        "name": "Storm X", "country": "Marshall Islands, Japan, China",
        "iso3": "MHL",
        "affectedcountries": [{"iso3": "CHN"}, {"iso3": "JPN"}],
        "fromdate": "2026-08-05T00:00:00", "todate": "2026-08-12T00:00:00",
        "url": {"report": "https://gdacs.example/report"}}},
]}


def test_extraction_folds_the_feeds_own_primary_country_into_iso3():
    from practice.foreknown import sources as src

    future = src.gdacs_futures(GDACS_PRIMARY_GAP)[0]
    assert future["iso3"] == ["CHN", "JPN", "MHL"]
    assert src.primary_iso3({"iso3": "  "}) == set()
    assert src.primary_iso3({}) == set()


def test_correction_repairs_committed_futures_as_ours_not_as_a_revision(
        tmp_path):
    """A country the register dropped is a CORRECTED event naming the cause —
    never a REVISED one, which would blame the source for our error."""
    import json as _json

    from practice.foreknown.correct import apply

    (tmp_path / "foreknown/snapshots/2026-08-09").mkdir(parents=True)
    (tmp_path / "foreknown/snapshots/2026-08-09/gdacs.json").write_text(
        _json.dumps(GDACS_PRIMARY_GAP))
    registry = {"futures": {"gdacs-tc-1001297": {
        "id": "gdacs-tc-1001297", "kind": "ALERT_EPISODE", "source": "GDACS",
        "status": "OPEN", "where": "Marshall Islands, Japan, China",
        "iso3": ["CHN", "JPN"],
        "history": [{"ts": "2026-08-08T05:45:00+00:00", "event": "NOTARIZED"}],
    }}}
    (tmp_path / "foreknown").mkdir(exist_ok=True)
    (tmp_path / "foreknown/registry.json").write_text(_json.dumps(registry))

    result = apply(tmp_path)
    assert [c["added"] for c in result["corrected"]] == [["MHL"]]

    repaired = _json.loads(
        (tmp_path / "foreknown/registry.json").read_text())["futures"]
    future = repaired["gdacs-tc-1001297"]
    assert future["iso3"] == ["CHN", "JPN", "MHL"]
    events = [h["event"] for h in future["history"]]
    assert events == ["NOTARIZED", "CORRECTED"]      # never REVISED
    assert "extraction" in future["history"][-1]["cause"]

    # idempotent: nothing is left to correct, and no second event appears
    again = apply(tmp_path)
    assert again["corrected"] == []
    repaired_again = _json.loads(
        (tmp_path / "foreknown/registry.json").read_text())["futures"]
    assert len(repaired_again["gdacs-tc-1001297"]["history"]) == 2

    # a closed future is left alone: the correction touches open records only
    log = (tmp_path / "autonomy/log.jsonl").read_text().splitlines()
    assert _json.loads(log[0])["step"] == "foreknown-correct-primary-iso3"
    assert _json.loads(log[0])["corrected_by"].startswith("the machine's")


# --- the third source, added 2026-08-22 after the E1 review ---------------

def _nws_alert(vtec: str, event: str = "Flood Warning", severity: str = "Severe",
               onset: str = "2026-08-22T10:11:00-05:00",
               ends: str = "2026-08-23T01:00:00-05:00",
               area: str = "Piatt, IL", ident: str = "urn:oid:1.001.1") -> dict:
    return {"properties": {
        "@id": f"https://api.weather.gov/alerts/{ident}", "id": ident,
        "event": event, "severity": severity, "urgency": "Expected",
        "certainty": "Likely", "onset": onset, "effective": onset,
        "ends": ends, "expires": ends, "areaDesc": area,
        "senderName": "NWS Lincoln IL", "messageType": "Alert",
        "parameters": {"VTEC": [vtec]}}}


def test_vtec_identity_follows_the_event_not_the_message():
    # An extension is a new CAP message with a new identifier; the office's own
    # tracking number is the same, and so is the future.
    first = sources.vtec_id("/O.NEW.KILX.FL.W.0039.260822T1511Z-260823T0600Z/")
    extended = sources.vtec_id("/O.EXT.KILX.FL.W.0039.000000T0000Z-260824T0600Z/")
    assert first == extended == "nws-kilx-flw-0039-26"


def test_vtec_identity_refuses_watches_endings_and_nonsense():
    # A watch is not a warning; CAN/EXP/UPG announce an ending, not a future.
    assert sources.vtec_id("/O.CON.KMFR.FW.A.0012.260822T2100Z-260823T0400Z/") is None
    assert sources.vtec_id("/O.EXP.KOUN.FF.W.0085.000000T0000Z-260822T1530Z/") is None
    assert sources.vtec_id("/O.CAN.KOUN.FF.W.0085.260822T1524Z-260822T1530Z/") is None
    assert sources.vtec_id("no vtec here") is None


def test_nws_extraction_keeps_one_future_per_event():
    feed = {"features": [
        _nws_alert("/O.NEW.KILX.FL.W.0039.260822T1511Z-260823T0600Z/"),
        # the same event, extended: one future, not two
        _nws_alert("/O.EXT.KILX.FL.W.0039.000000T0000Z-260824T0600Z/",
                   ends="2026-08-24T01:00:00-05:00", ident="urn:oid:1.002.1"),
        _nws_alert("/O.NEW.KMSO.FW.W.0009.260822T2300Z-260823T1200Z/",
                   event="Red Flag Warning", area="Western Lolo"),
        # a watch never enters the register
        _nws_alert("/O.NEW.KMFR.FW.A.0012.260822T2100Z-260823T0400Z/",
                   event="Fire Weather Watch"),
    ]}
    futures = sources.nws_futures(feed)
    assert [f["id"] for f in futures] == ["nws-kilx-flw-0039-26",
                                          "nws-kmso-fww-0009-26"]
    flood = futures[0]
    assert flood["source"] == "NWS" and flood["kind"] == "ALERT_EPISODE"
    assert flood["hazard"] == "flood" and flood["what"] == "Flood Warning"
    assert flood["iso3"] == ["USA"]
    # First message wins: the window is the one this practice first saw.
    assert flood["window"]["to"] == "2026-08-23T01:00:00-05:00"
    assert sources.nws_futures({"features": []}) == []


def test_an_alert_without_a_vtec_number_is_not_notarized():
    alert = _nws_alert("/O.NEW.KILX.FL.W.0039.260822T1511Z-260823T0600Z/")
    alert["properties"]["parameters"] = {}
    assert sources.nws_futures({"features": [alert]}) == []


def test_a_warning_extended_over_two_nights_is_revised_not_renotarized(tmp_path: Path):
    night_one = {"features": [
        _nws_alert("/O.NEW.KILX.FL.W.0039.260822T1511Z-260823T0600Z/")]}
    night_two = {"features": [
        _nws_alert("/O.EXT.KILX.FL.W.0039.000000T0000Z-260824T0600Z/",
                   ends="2026-08-24T01:00:00-05:00", ident="urn:oid:1.002.1")]}
    quiet = {"activeStorms": []}
    announced_at_after_night_one = None
    for day, feed in (("2026-08-22", night_one), ("2026-08-23", night_two)):
        responses = {
            sources.GDACS_URL: (json.dumps({"features": []}).encode(), 200),
            sources.NHC_URL: (json.dumps(quiet).encode(), 200),
            sources.NWS_URL: (json.dumps(feed).encode(), 200),
            sources.FTS_PLANS_URL: (json.dumps({"data": []}).encode(), 200),
        }
        summary = run(tmp_path, day, FakeClient(responses))
        if announced_at_after_night_one is None:
            registry = read_json(tmp_path / "foreknown/registry.json")
            announced_at_after_night_one = (
                registry["futures"]["nws-kilx-flw-0039-26"]["announced_at"])
    registry = read_json(tmp_path / "foreknown/registry.json")
    assert list(registry["futures"]) == ["nws-kilx-flw-0039-26"]
    future = registry["futures"]["nws-kilx-flw-0039-26"]
    assert [e["event"] for e in future["history"]] == ["NOTARIZED", "REVISED"]
    # announced_at is the retrieval time of the first sighting (futures.py's
    # module docstring) and never changes afterwards (I3) -- checked against
    # what night one actually recorded, not a hardcoded calendar date, since
    # update_registry stamps it from the real clock (utc_now()) rather than
    # from the `day` argument, and a literal date here would only ever be
    # true on the one real-world day this test happened to be written on.
    assert future["announced_at"] == announced_at_after_night_one
    assert future["window"]["to"] == "2026-08-24T01:00:00-05:00"
