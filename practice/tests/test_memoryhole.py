"""Memory Hole V0 — the units the audit made conditions.

The validity gate exists because the origin published a WAF challenge page as a
270-token removal on 2026-08-14 (finding 1) and a cookie banner as a deletion
(finding 2). These tests hold the gate to both, hold "gone" to a live recheck,
and hold the event classifier to the five operations it may name.
"""

import json

from practice.memoryhole import (cdx, events, model, recheck, textdiff,
                                 validity, watchlist)
from practice.memoryhole.extract import text_of

# The bytes the audit actually met: 118,410 bytes of HTML from which the
# extraction wins eight tokens.
CHALLENGE = (
    "Verifying your browser before proceeding... "
    "Incident ID: e4841cb0-dxzu-4858-bcd7-154223367ef4")

# The shape of the text the origin scored at salience 14 on the BaFin page:
# long enough to clear the length floor, and nothing but the cookie notice.
CONSENT = (
    "Diese Website verwendet Cookies. Wir nutzen Matomo für die Analyse der "
    "Zugriffe und setzen nur essenzielle Cookies ohne Ihre Einwilligung. Sie "
    "können Ihre Einwilligung jederzeit widerrufen. Weitere Hinweise finden "
    "Sie in unserer Datenschutzerklärung. Notwendige Cookies ermöglichen "
    "grundlegende Funktionen und sind für die einwandfreie Funktion der "
    "Website erforderlich. Mit Ihrer Einwilligung erlauben Sie uns die "
    "Verwendung von Cookies zur Reichweitenmessung durch einen Dritten.")

PAGE = (
    "The strategy commits the federal government to climate neutrality by "
    "2045. It will reduce emissions by 65 percent before the end of the "
    "decade. The measures are financed from the climate and transformation "
    "fund, and the ministry reports on their progress every year. Further "
    "steps are planned for the coming period, and the responsible department "
    "publishes an annual account of what has been achieved so far.")


def test_gate_lets_a_real_page_through():
    verdict = validity.check(PAGE, "200")
    assert verdict.valid
    assert verdict.reason == "ok"
    assert verdict.tokens > validity.MIN_TOKENS


def test_gate_stops_the_challenge_page_that_fooled_the_origin():
    verdict = validity.check(CHALLENGE, "200")
    assert not verdict.valid
    assert verdict.reason == "challenge_fingerprint"
    assert "verifying your browser" in verdict.markers


def test_gate_stops_a_challenge_page_extracted_from_real_markup():
    html = (b"<html><head><title>Just a moment...</title></head><body>"
            b"<h1>Attention Required!</h1><p>Checking your browser before "
            b"accessing the site. Ray ID: 8f2c</p></body></html>")
    verdict = validity.check(text_of(html), "200")
    assert not verdict.valid
    assert verdict.reason == "challenge_fingerprint"


def test_gate_stops_consent_boilerplate():
    verdict = validity.check(CONSENT, "200")
    assert not verdict.valid
    assert verdict.reason == "consent_boilerplate"


def test_gate_stops_a_short_page_and_a_non_200():
    assert validity.check("Zu kurz.", "200").reason == "too_short"
    assert validity.check(PAGE, "403").reason == "status_403"


def test_gate_stops_a_navigation_pile():
    nav = " ".join(["Presse Publikationen Termine Kontakt Impressum "
                    "Barrierefreiheit Leichte Sprache"] * 12)
    verdict = validity.check(nav, "200")
    assert not verdict.valid
    assert verdict.reason == "not_prose"


# --- the deletion question -------------------------------------------------

class _FakeResponse:
    def __init__(self, status, body=b""):
        self.status = status
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _client(status):
    import urllib.error

    def opener(request, timeout=0):
        if status >= 400:
            raise urllib.error.HTTPError(request.full_url, status, "", {}, None)
        return _FakeResponse(status, b"<html>still here</html>")

    from practice.fetch import Client
    return Client(opener=opener, sleep=lambda _s: None, clock=lambda: 0.0)


def test_a_4xx_in_the_archive_is_only_a_candidate():
    rows = [cdx.Row("20260801120000", "https://x.test/a", "200", "D1"),
            cdx.Row("20260814120000", "https://x.test/a", "403", "D2")]
    reading = cdx.classify(rows, "2026-08-14")
    assert reading.kind == "deletion_candidate"
    assert reading.reason == "archive_status_403"


def test_a_live_200_means_the_page_is_not_gone():
    result = recheck.check(_client(200), "https://x.test/a")
    assert result["class"] == recheck.OK
    assert result["class"] not in recheck.GONE


def test_a_live_404_means_gone():
    result = recheck.check(_client(404), "https://x.test/a")
    assert result["class"] == recheck.GONE_404


def test_a_live_403_is_unverifiable_not_gone():
    result = recheck.check(_client(403), "https://x.test/a")
    assert result["class"] == recheck.BOTWALL


def test_botwalls_leave_the_denominator():
    summary = recheck.summarize([recheck.GONE_404, recheck.OK, recheck.BOTWALL,
                                 recheck.LEGAL_451, recheck.SERVER_ERROR])
    assert summary["decided"] == 3
    assert summary["excluded_unverifiable"] == 2
    assert summary["gone"] == 1
    low, high = summary["gone_ci95"]
    assert low < summary["gone_rate"] < high


def test_wilson_matches_the_origin():
    low, high = recheck.wilson(1, 10)
    assert round(low, 4) == 0.0179
    assert round(high, 4) == 0.4042


# --- the history reading ---------------------------------------------------

def test_a_day_without_a_new_digest_is_unchanged():
    rows = [cdx.Row("20260801120000", "https://x.test/a", "200", "D1")]
    assert cdx.classify(rows, "2026-08-14").kind == "unchanged"


def test_a_new_digest_on_the_day_is_a_changed_candidate():
    rows = [cdx.Row("20260801120000", "https://x.test/a", "200", "D1"),
            cdx.Row("20260814090000", "https://x.test/a", "200", "D2")]
    reading = cdx.classify(rows, "2026-08-14")
    assert reading.kind == "changed_candidate"
    assert reading.before.digest == "D1"
    assert reading.after.digest == "D2"


def test_captures_after_the_day_never_decide_the_day():
    rows = [cdx.Row("20260801120000", "https://x.test/a", "200", "D1"),
            cdx.Row("20260815100000", "https://x.test/a", "404", "D3")]
    assert cdx.classify(rows, "2026-08-14").kind == "unchanged"


def test_a_redirect_is_not_a_deletion():
    rows = [cdx.Row("20260801120000", "https://x.test/a", "200", "D1"),
            cdx.Row("20260814120000", "https://x.test/a", "301", "D2")]
    reading = cdx.classify(rows, "2026-08-14")
    assert reading.kind == "unverifiable"
    assert reading.reason == "archive_status_301"


def test_discovery_query_is_the_proven_production_form():
    url = cdx.discovery_url("bundesnetzagentur.de", "domain", "2026-08-14")
    assert "matchType=domain" in url
    assert "from=20260814&to=20260814" in url
    assert "collapse=urlkey" in url
    assert "mimetype%3Atext%2Fhtml" in url


# --- the event classifier --------------------------------------------------

def _classify(before, after):
    found, abstentions = events.classify(textdiff.diff(before, after))
    return [e.type for e in found], abstentions


def test_number_revised():
    types, _ = _classify(
        "The programme will reduce emissions by 65 percent before 2030.",
        "The programme will reduce emissions by 55 percent before 2030.")
    assert types == ["number_revised"]


def test_date_shifted():
    types, _ = _classify(
        "The federal government commits to climate neutrality by 2045.",
        "The federal government commits to climate neutrality by 2050.")
    assert "date_shifted" in types


def test_negation_flipped():
    types, _ = _classify(
        "The authority will not extend the deadline for the reporting duty.",
        "The authority will extend the deadline for the reporting duty.")
    assert "negation_flipped" in types


def test_commitment_removed_in_a_rewrite():
    types, _ = _classify(
        "The company will reach net zero across all of its own operations.",
        "The company considers options across all of its own operations.")
    assert "commitment_removed" in types


def test_commitment_removed_with_the_whole_sentence():
    types, _ = _classify(
        "The company will reach net zero by the middle of the century. "
        "The report describes the current portfolio of the group.",
        "The report describes the current portfolio of the group.")
    assert types == ["commitment_removed"]


def test_attribution_removed_is_recorded_without_the_person():
    diff = textdiff.diff(
        "According to director Maria Schmidt the target remains in force for "
        "all of the divisions of the group.",
        "The target remains in force for all of the divisions of the group.")
    found, _ = events.classify(diff)
    assert [e.type for e in found] == ["attribution_removed"]
    assert found[0].before is None, "a name must never enter a register line"
    assert found[0].before_sha256


def test_an_untyped_change_becomes_an_abstention_not_an_event():
    types, abstentions = _classify(
        "The office publishes the annual figures for the reporting period 2024.",
        "The office publishes the annual figures for the whole reporting "
        "period 2024.")
    assert types == []
    assert len(abstentions) == 1
    assert abstentions[0].salience > 0


def test_navigation_noise_produces_nothing():
    types, abstentions = _classify(
        "Presse Publikationen Termine Kontakt Impressum",
        "Presse Termine Kontakt Impressum")
    assert types == []
    assert abstentions == []


# --- the model layer -------------------------------------------------------

def test_the_model_layer_degrades_honestly_without_a_key():
    block = model.classify([{"before_sha256": "a" * 64, "before": "x"}],
                           key=None)
    assert block["available"] is False
    assert block["state"] == "off: no key configured"
    assert block["verdicts"] == []
    assert block["cost_usd"] == 0.0


def test_the_model_layer_prices_the_batch_discount():
    assert model.cost_usd(2000, 300) == round(
        (2000 / 1e6 * 1.0 + 300 / 1e6 * 5.0) * 0.5, 6)


def test_a_verdict_outside_the_vocabulary_is_not_repaired():
    assert model.parse_verdict('{"type": "vertuschung"}')["error"] == \
        "out_of_vocabulary"
    assert model.parse_verdict("no json here")["error"] == "unparsed"
    assert model.parse_verdict(
        '{"type": "number_revised", "confidence": "low"}')["type"] == \
        "number_revised"


def test_the_cap_is_franks_forty():
    assert model.NIGHTLY_CAP == 40


# --- the watchlist ---------------------------------------------------------

def _repo_root():
    from pathlib import Path
    return Path(__file__).resolve().parents[2]


def test_the_committed_watchlist_validates():
    doc = json.loads((_repo_root() / watchlist.WATCHLIST_PATH).read_text(
        encoding="utf-8"))
    assert watchlist.validate(doc) == []


def test_the_watchlist_avoids_every_page_chamber_one_watches():
    doc = json.loads((_repo_root() / watchlist.WATCHLIST_PATH).read_text(
        encoding="utf-8"))
    excluded = watchlist.excluded_urls(doc)
    assert len(excluded) == 32, "chamber 1 watches 32 pages"
    watched = {c["url"] for c in doc["controls"]}
    for entry in doc["institutions"]:
        watched |= set(entry.get("urls", []))
    assert not (watched & excluded)


def test_every_institution_carries_the_probe_that_justifies_its_strategy():
    doc = json.loads((_repo_root() / watchlist.WATCHLIST_PATH).read_text(
        encoding="utf-8"))
    for entry in doc["institutions"]:
        probe = entry["probe"]
        assert probe["at"].startswith("2026-08-1")
        assert probe["http_status"] == 200
        assert probe["urls"] > 0
        assert entry["strategy"] in watchlist.STRATEGIES


def test_a_watchlist_without_probes_is_refused():
    bad = {"version": "x", "excluded": {"urls": ["https://a"]},
           "institutions": [{"slug": "s", "category": "A", "strategy": "domain",
                             "query": "s.test"}],
           "controls": []}
    problems = watchlist.validate(bad)
    assert any("live probe" in p for p in problems)
    assert any("control" in p for p in problems)


def test_the_sample_is_deterministic_and_independent_of_input_order():
    from practice.memoryhole.run import sample
    urls = [f"https://x.test/{i}" for i in range(40)]
    first = sample(urls, "2026-08-14", set(), 5)
    second = sample(list(reversed(urls)), "2026-08-14", set(), 5)
    assert first == second
    assert len(first) == 5
    assert sample(urls, "2026-08-15", set(), 5) != first
