import importlib.util
import json
import re
import shutil
from pathlib import Path

from practice.foreknown import attention, reaction, sources
from practice.foreknown.run import run

from .test_foreknown import GDACS_FIXTURE, FakeClient
from .test_reaction import FUNDING, PLANS, _row, gdelt_zip

REPO_ROOT = Path(__file__).parents[2]

FIPS_LOOKUP = b"ET\tEthiopia\nKE\tKenya\nJA\tJapan\nRM\tMarshall Islands\n"
CROSSWALK_RECORD = {"entries": {"ETH": {"fips": "ET"}, "KEN": {"fips": "KE"},
                                "JPN": {"fips": "JA"}, "MHL": {"fips": "RM"}}}


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _fixture_repo(tmp_path: Path) -> Path:
    """One night of the full chain: notary, resolver and reaction axis."""
    shutil.copytree(REPO_ROOT / "stage", tmp_path / "stage",
                    ignore=shutil.ignore_patterns("__pycache__"))
    crosswalk = tmp_path / "foreknown" / "reaction" / "iso3-fips.json"
    crosswalk.parent.mkdir(parents=True)
    crosswalk.write_text(json.dumps(CROSSWALK_RECORD), encoding="utf-8")
    responses = {
        sources.GDACS_URL: (json.dumps(GDACS_FIXTURE).encode(), 200),
        sources.NHC_URL: (json.dumps({"activeStorms": []}).encode(), 200),
        sources.FTS_PLANS_URL: (json.dumps(PLANS).encode(), 200),
        reaction.FTS_FUNDING_URL: (json.dumps(FUNDING).encode(), 200),
        attention.FIPS_LOOKUP_URL: (FIPS_LOOKUP, 200),
        attention.day_url("2026-08-06"): (gdelt_zip(
            [_row("KE", 2, 20), _row("ET", 1, 10), _row("JA", 1, 5)]), 200),
        attention.day_url("2026-08-07"): (gdelt_zip(
            [_row("KE", 4, 40), _row("ET", 1, 10), _row("JA", 1, 5)]), 200),
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
    # One reaction sentence on the featured warning, no dashboard: what the
    # world published, and whether any plan even lists these countries.
    assert "news mentions from these countries on 2026-08-07" in page
    assert "No UN humanitarian plan for 2026 lists these countries." in page
    assert page.count("featured-reaction") == 1

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


def test_verify_redoes_the_reaction_arithmetic_from_the_committed_bytes(tmp_path):
    """A reaction reading is a claim about preserved bytes; the verifier
    recomputes it rather than taking the record's word for it."""
    root = _fixture_repo(tmp_path)
    _load("stagegen_t3", root / "stage" / "generate.py").build(root)
    verify = _load("verify_t3", REPO_ROOT / "verify.py")
    assert verify.check(root) == []

    path = root / "foreknown/reaction/readings/2026-08-08.json"
    reading = json.loads(path.read_text())
    drought = reading["futures"]["gdacs-dr-1027450"]
    assert drought["money"]["plans"] == [1516]        # Somalia plan lists KEN
    assert drought["attention"]["articles"] == 50     # KE 40 + ET 10
    assert drought["attention"]["ratio_to_baseline"] == 1.67  # median 30

    drought["attention"]["articles"] = 5_000
    path.write_text(json.dumps(reading))
    assert any("recomputed from the committed day records" in p
               for p in verify.check(root))

    drought["attention"]["articles"] = 50
    drought["money"]["plan_funded_usd"] = 1
    path.write_text(json.dumps(reading))
    assert any("plan funding does not add up" in p for p in verify.check(root))

    # The crosswalk is the one hand-authored link: it is held against the
    # issuer's own code list, not against itself.
    drought["money"]["plan_funded_usd"] = 300
    path.write_text(json.dumps(reading))
    (root / "foreknown/reaction/iso3-fips.json").write_text(json.dumps(
        {"entries": {"ETH": {"fips": "ZZ"}}}), encoding="utf-8")
    assert any("not in the preserved GDELT code list" in p
               for p in verify.check(root))


def test_the_deeper_levels_build_from_the_records(tmp_path):
    """ENTER (dossier), INVESTIGATE (ledger), VERIFY (provenance) — every
    page a deterministic function of committed records, plain words first."""
    root = _fixture_repo(tmp_path)
    _load("stagegen_t4", root / "stage" / "generate.py").build(root)
    out = root / "public"

    dossier = (out / "future" / "gdacs-dr-1027450.html").read_text()
    assert "first seen" in dossier                       # the life, plainly
    assert "foreknown/snapshots/2026-08-08/gdacs.json" in dossier  # anchored
    assert "Somalia 2026" in dossier                     # the plan, by name
    assert "not money raised for this hazard" in dossier  # the limit rides along
    assert "news mentions from these countries" in dossier
    # the drought's window (to 2026-08-06) passed before first sight
    assert "artefact of when observation began" in dossier

    ledger = (out / "ledger.html").read_text()
    assert "Everything the machine has recorded so far" in ledger
    assert 'future/gdacs-tc-1001297.html' in ledger      # rows link down
    assert "No warning has closed yet" in ledger         # honest empty state
    assert "an empty night is honest" in ledger          # no proposals yet

    verify_html = (out / "verify.html").read_text()
    assert "Nothing here asks to be believed" in verify_html
    manifest = json.loads(
        (root / "foreknown/snapshots/2026-08-08/manifest.json").read_text())
    assert manifest["entries"][0]["sha256"] in verify_html
    assert "it is the finding" in verify_html            # referenced, not stored


def test_no_page_has_a_dead_end(tmp_path):
    """The exhibition rule as a test: every relative link on every generated
    page resolves to a generated file."""
    root = _fixture_repo(tmp_path)
    _load("stagegen_t5", root / "stage" / "generate.py").build(root)
    out = root / "public"
    pages = list(out.rglob("*.html"))
    assert len(pages) >= 5  # index, ledger, verify, two dossiers
    for page in pages:
        for link in re.findall(r'(?:href|src)="([^"]+)"', page.read_text()):
            if link.startswith(("http", "#", "mailto:")):
                continue
            assert (page.parent / link).exists(), \
                f"{page.relative_to(out)} -> {link}"


def test_the_ledger_shows_what_the_machine_itself_proposed(tmp_path):
    root = _fixture_repo(tmp_path)
    proposals = root / "foreknown" / "proposals"
    proposals.mkdir(parents=True)
    (proposals / "sensor-x.json").write_text(json.dumps({
        "name": "x-sensor", "definition": "Watches x against y.",
        "test_rule": "t", "falsification": "f", "status": "STANDING",
        "promotion": {"why_standing": "It measures nightly."}}),
        encoding="utf-8")
    (proposals / "obs-1.json").write_text(json.dumps({
        "kind": "difference_observation", "title": "An asymmetry",
        "statement": "The record shows an asymmetry.",
        "derived_from": ["foreknown/registry.json"]}), encoding="utf-8")
    _load("stagegen_t6", root / "stage" / "generate.py").build(root)

    ledger = (root / "public" / "ledger.html").read_text()
    assert "x-sensor" in ledger and "STANDING" in ledger
    assert "It measures nightly." in ledger              # the promotion story
    assert "An asymmetry" in ledger
    assert "derived from: foreknown/registry.json" in ledger
