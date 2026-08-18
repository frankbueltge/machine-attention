"""The reaction axis — what moved while a warning was already running.

The money half implements the machine's own proposal
`sensor-fts-country-coverage`; these tests hold it to the proposal's text,
including its refusal to fire before three nights of baseline exist.
"""

import io
import json
import zipfile

from practice.foreknown import attention, reaction

# GDELT 1.0 event rows: 58 tab-separated columns, no header. Only the four
# columns this instrument reads are filled; the rest stand as the real file
# has them — present and mostly empty.
def _row(country: str, mentions: int, articles: int) -> str:
    cols = [""] * attention.COLUMNS
    cols[attention.COL_MENTIONS] = str(mentions)
    cols[attention.COL_ARTICLES] = str(articles)
    cols[attention.COL_ACTION_GEO_COUNTRY] = country
    return "\t".join(cols)


def gdelt_zip(rows: list[str]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("20260807.export.CSV", "\n".join(rows) + "\n")
    return buffer.getvalue()


PLANS = {"data": [
    {"id": 1516, "revisedRequirements": 900, "origRequirements": 800,
     "planVersion": {"name": "Somalia 2026"},
     "locations": [{"iso3": "SOM"}, {"iso3": "KEN"}]},
    {"id": 1520, "revisedRequirements": 500,
     "planVersion": {"name": "Yemen 2026"}, "locations": [{"iso3": "YEM"}]},
]}
FUNDING = {"data": {"report3": {"fundingTotals": {"objects": [
    {"type": "Plan", "direction": "destination", "singleFundingObjects": [
        {"name": "Not specified", "totalFunding": 42},
        {"id": 1516, "totalFunding": 300},
        {"id": 1520, "totalFunding": 100},
    ]}]}}}}
CROSSWALK = {"SOM": "SO", "KEN": "KE", "DEU": "GM"}


def registry_with(*futures) -> dict:
    return {"futures": {f["id"]: f for f in futures}}


def episode(fid, iso3, status="OPEN", kind="ALERT_EPISODE"):
    return {"id": fid, "kind": kind, "status": status, "iso3": iso3,
            "hazard": "flood", "what": fid, "where": "", "severity": "Orange",
            "window": {"from": None, "to": None}, "announced_at": "2026-08-08",
            "history": []}


def test_aggregate_counts_by_country_and_keeps_the_unlocated_apart():
    raw = gdelt_zip([_row("SO", 3, 2), _row("SO", 1, 1), _row("KE", 5, 4),
                     _row("", 9, 7), "too\tshort"])
    day = attention.aggregate(raw)

    assert day["countries"]["SO"] == {"events": 2, "articles": 3, "mentions": 4}
    assert day["countries"]["KE"]["articles"] == 4
    assert day["unlocated"] == {"events": 1, "articles": 7, "mentions": 9}
    assert day["malformed_rows"] == 1
    # The world total is everything GDELT recorded, unlocated included —
    # never redistributed onto countries to make the shares look tidy.
    assert day["world"] == {"events": 4, "articles": 14, "mentions": 18}


def test_day_record_carries_a_verifiable_reference_to_bytes_it_does_not_keep():
    raw = gdelt_zip([_row("SO", 1, 1)])
    record = attention.day_record("2026-08-07", raw, "http://example.invalid/x")

    assert record["source"]["stored"] is False
    assert record["source"]["bytes"] == len(raw)
    assert len(record["source"]["sha256"]) == 64
    assert record["source"]["url"] == "http://example.invalid/x"


def test_plan_and_funding_indices_read_fts_as_fts_publishes_it():
    plans = reaction.plans_index(PLANS)
    assert plans[1516]["iso3"] == ["KEN", "SOM"]
    assert plans[1516]["requirements_usd"] == 900  # revised wins over original

    funding = reaction.funding_index(FUNDING)
    assert funding == {1516: 300, 1520: 100}  # "Not specified" has no plan id


def test_reading_joins_futures_to_plans_by_iso3_and_keeps_totals_the_plans_own():
    registry = registry_with(episode("a", ["SOM"]), episode("b", ["DEU"]))
    reading = reaction.build_reading(
        "2026-08-08", registry, PLANS, FUNDING, CROSSWALK, {}, {})

    somalia = reading["futures"]["a"]["money"]
    assert somalia["has_fts_plan_match"] is True
    assert somalia["plans"] == [1516]
    assert somalia["plan_requirements_usd"] == 900
    assert somalia["plan_funded_usd"] == 300

    germany = reading["futures"]["b"]["money"]
    assert germany["has_fts_plan_match"] is False
    assert germany["plans"] == [] and germany["plan_funded_usd"] == 0
    assert reading["coverage"] == {"open_alert_episodes": 2,
                                   "with_fts_plan_match": 1,
                                   "match_rate": 0.5}


def test_closed_futures_leave_the_reading_and_unmapped_countries_are_recorded():
    registry = registry_with(episode("a", ["SOM"], status="CLOSED_BY_SOURCE"),
                             episode("b", ["SOM", "ZZZ"]))
    reading = reaction.build_reading(
        "2026-08-08", registry, PLANS, FUNDING, CROSSWALK, {}, {})

    assert list(reading["futures"]) == ["b"]
    # An iso3 with no crosswalk entry is named in the record rather than
    # quietly reading as zero attention.
    assert reading["futures"]["b"]["unmapped_iso3"] == ["ZZZ"]
    assert reading["futures"]["b"]["fips"] == ["SO"]


def test_attention_is_measured_against_the_countries_own_median():
    days = {
        "2026-08-01": attention.aggregate(gdelt_zip([_row("SO", 1, 10),
                                                     _row("XX", 1, 90)])),
        "2026-08-02": attention.aggregate(gdelt_zip([_row("SO", 1, 30),
                                                     _row("XX", 1, 70)])),
        "2026-08-03": attention.aggregate(gdelt_zip([_row("SO", 1, 40),
                                                     _row("XX", 1, 60)])),
    }
    for day, record in days.items():
        record["date"] = day
    window = reaction.baseline_window(days, "2026-08-03")
    entry = reaction.attention_entry(["SO"], days, "2026-08-03", window)

    assert window == ["2026-08-01", "2026-08-02"]
    assert entry["articles"] == 40
    assert entry["baseline_median_articles"] == 20.0  # median of 10 and 30
    assert entry["ratio_to_baseline"] == 2.0
    assert entry["share_per_10k"] == 4000.0  # 40 of the day's 100 articles


def test_a_country_without_a_crosswalk_entry_gets_no_invented_attention():
    days = {"2026-08-03": attention.aggregate(gdelt_zip([_row("SO", 1, 5)]))}
    days["2026-08-03"]["date"] = "2026-08-03"
    assert reaction.attention_entry([], days, "2026-08-03", []) is None


def test_the_sensor_refuses_to_fire_before_the_baseline_the_proposal_demands():
    registry = registry_with(episode("a", ["SOM"]), episode("b", ["DEU"]))
    first = reaction.build_reading("2026-08-08", registry, PLANS, FUNDING,
                                   CROSSWALK, {}, {}, nights=1)
    assert first["sensor"]["firing"] == "DEFERRED"
    assert first["sensor"]["fired"] is False

    # Night three: armed, and 50% sits inside the proposal's own band.
    third = reaction.build_reading("2026-08-10", registry, PLANS, FUNDING,
                                   CROSSWALK, {}, {}, nights=3,
                                   prior={"coverage": {"match_rate": 0.5}})
    assert third["sensor"]["firing"] == "ARMED"
    assert third["sensor"]["fired"] is False

    # A ten-point move between nights is what the proposal asked to be told.
    moved = reaction.build_reading("2026-08-10", registry, PLANS, FUNDING,
                                   CROSSWALK, {}, {}, nights=3,
                                   prior={"coverage": {"match_rate": 0.2}})
    assert moved["sensor"]["fired"] is True
    assert "moved" in moved["sensor"]["why"]


def test_catchup_sensor_defers_before_five_nights_of_history():
    registry = registry_with(episode("a", ["SOM"]))
    reading = reaction.build_reading("2026-08-14", registry, PLANS, FUNDING,
                                     CROSSWALK, {}, {},
                                     failures=[{"scope": "attention:2026-08-13",
                                               "error": "not published yet"}],
                                     catchup_history=[
                                         {"date": "2026-08-12",
                                          "attention_day": "2026-08-11",
                                          "failures": []},
                                     ])
    assert reading["catchup_sensor"]["firing"] == "DEFERRED"
    assert reading["catchup_sensor"]["fired"] is False
    assert reading["catchup_sensor"]["nights_recorded"] == 2


def test_catchup_sensor_fires_on_five_consecutive_matching_nights():
    # Mirrors the committed record 2026-08-14 through 2026-08-18: attention_day
    # two days behind the run date every night, each with a "not published
    # yet" failure for the newest missing day (foreknown/reaction/readings/).
    prior = [
        {"date": "2026-08-14", "attention_day": "2026-08-12",
         "failures": [{"scope": "attention:2026-08-13",
                      "error": "not published yet"}]},
        {"date": "2026-08-15", "attention_day": "2026-08-13",
         "failures": [{"scope": "attention:2026-08-14",
                      "error": "not published yet"}]},
        {"date": "2026-08-16", "attention_day": "2026-08-14",
         "failures": [{"scope": "attention:2026-08-15",
                      "error": "not published yet"}]},
        {"date": "2026-08-17", "attention_day": "2026-08-15",
         "failures": [{"scope": "attention:2026-08-16",
                      "error": "not published yet"}]},
    ]
    registry = registry_with(episode("a", ["SOM"]))
    days = {"2026-08-16": attention.aggregate(gdelt_zip([_row("SO", 1, 1)]))}
    days["2026-08-16"]["date"] = "2026-08-16"
    reading = reaction.build_reading("2026-08-18", registry, PLANS, FUNDING,
                                     CROSSWALK, days, {},
                                     failures=[{"scope": "attention:2026-08-17",
                                               "error": "not published yet"}],
                                     catchup_history=prior)
    sensor = reading["catchup_sensor"]
    assert sensor["firing"] == "ARMED"
    assert sensor["fired"] is True
    assert sensor["gap_days"] == 2


def test_catchup_sensor_does_not_fire_when_the_gap_closes_early():
    prior = [
        {"date": "2026-08-14", "attention_day": "2026-08-12",
         "failures": [{"scope": "attention:2026-08-13",
                      "error": "not published yet"}]},
        {"date": "2026-08-15", "attention_day": "2026-08-13",
         "failures": [{"scope": "attention:2026-08-14",
                      "error": "not published yet"}]},
        {"date": "2026-08-16", "attention_day": "2026-08-14",
         "failures": [{"scope": "attention:2026-08-15",
                      "error": "not published yet"}]},
        # the gap closes: this night's run reaches yesterday after all.
        {"date": "2026-08-17", "attention_day": "2026-08-16", "failures": []},
    ]
    registry = registry_with(episode("a", ["SOM"]))
    reading = reaction.build_reading("2026-08-18", registry, PLANS, FUNDING,
                                     CROSSWALK, {}, {},
                                     failures=[{"scope": "attention:2026-08-17",
                                               "error": "not published yet"}],
                                     catchup_history=prior)
    sensor = reading["catchup_sensor"]
    assert sensor["firing"] == "ARMED"
    assert sensor["fired"] is False


def test_reading_states_what_its_numbers_are_not(tmp_path):
    reading = reaction.build_reading("2026-08-08", registry_with(
        episode("a", ["SOM"])), PLANS, FUNDING, CROSSWALK, {}, {})
    joined = " ".join(reading["notes"])
    assert "adequacy" in joined and "not distinct articles" in joined
    assert "for the country, not for the hazard" in joined


def test_reaction_run_records_outages_and_refuses_to_overwrite(tmp_path):
    class FakeClient:
        requests = 0
        http_429 = 0

        def fetch(self, url):
            if url == reaction.FTS_FUNDING_URL:
                return json.dumps(FUNDING).encode(), 200
            return b"", 404  # GDELT day not published yet, lookup gone

    (tmp_path / "foreknown/snapshots/2026-08-08").mkdir(parents=True)
    (tmp_path / "foreknown/snapshots/2026-08-08/fts-plans-2026.json").write_text(
        json.dumps(PLANS), encoding="utf-8")
    registry = registry_with(episode("a", ["SOM"]))

    summary = reaction.run_reaction(tmp_path, "2026-08-08", registry,
                                    client=FakeClient(), backfill=2)
    scopes = sorted(f["scope"] for f in summary["failures"])
    assert scopes == ["attention:2026-08-06", "attention:2026-08-07",
                      "reaction:GDELT-fips"]
    assert summary["match_rate"] == 1.0

    reading = json.loads((tmp_path / "foreknown/reaction/readings/"
                          "2026-08-08.json").read_text())
    assert reading["attention_day"] is None
    assert reading["futures"]["a"]["attention"] is None
    assert reading["sources"]["FTS-plans"] == \
        "foreknown/snapshots/2026-08-08/fts-plans-2026.json"

    try:
        reaction.run_reaction(tmp_path, "2026-08-08", registry,
                              client=FakeClient(), backfill=0)
    except SystemExit as err:
        assert "append-only" in str(err)
    else:
        raise AssertionError("a second reading for the same day must be refused")


def test_reaction_run_widens_the_window_past_a_multi_night_gap(tmp_path):
    """A fixed `backfill`-day trailing window forgets a day older than that,
    even one GDELT has since published, once enough nights pass without a
    run (e.g. the anchor deadlock of 2026-08-10/11 — obs-2026-08-12-2). The
    window must widen to reach a day still missing since the newest one
    already committed, not just the last `backfill` nights before today."""
    attention_dir = tmp_path / "foreknown/reaction/attention"
    attention_dir.mkdir(parents=True)
    (attention_dir / "2026-08-07.json").write_text(json.dumps({
        "date": "2026-08-07", "source": {"url": attention.day_url("2026-08-07")},
        "world": dict(attention.EMPTY), "unlocated": dict(attention.EMPTY),
        "countries": {},
    }), encoding="utf-8")

    fetched = []

    class FakeClient:
        requests = 0
        http_429 = 0

        def fetch(self, url):
            if url == reaction.FTS_FUNDING_URL:
                return json.dumps(FUNDING).encode(), 200
            if url == attention.FIPS_LOOKUP_URL:
                return b"", 404
            fetched.append(url)
            return gdelt_zip([_row("SO", 1, 1)]), 200

    (tmp_path / "foreknown/snapshots/2026-08-12").mkdir(parents=True)
    (tmp_path / "foreknown/snapshots/2026-08-12/fts-plans-2026.json").write_text(
        json.dumps(PLANS), encoding="utf-8")
    registry = registry_with(episode("a", ["SOM"]))

    # backfill=3 alone would only reach 08-09..08-11 and never ask for
    # 08-08 again — the bug the discovery pass found.
    reaction.run_reaction(tmp_path, "2026-08-12", registry,
                          client=FakeClient(), backfill=3)

    assert attention.day_url("2026-08-08") in fetched
    assert (attention_dir / "2026-08-08.json").exists()
