"""The Interval driver rule `drivers-grfc-v1`: constructed workbooks in a
temporary tree, no network; the preserved GRFC file read once as a fixed
regression; and `verify.py`'s independent re-derivation."""

import importlib.util
import io
import json
import zipfile
from pathlib import Path

import pytest

from practice.interval import drivers

REPO = Path(__file__).resolve().parents[2]
GRFC = "interval/probes/2026-10-22/hdx/grfc_afi_database_2016-2025_september_update.xlsx"
HEAD = list(drivers.COLUMNS)


def verifier():
    spec = importlib.util.spec_from_file_location("verify_ivd", REPO / "verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def xlsx(rows, inline=False):
    """A minimal workbook: header + rows, shared strings, years as numbers."""
    strings: list[str] = []

    def cell(ref, value):
        if isinstance(value, int):
            return f'<c r="{ref}"><v>{value}</v></c>'
        if inline:
            return f'<c r="{ref}" t="inlineStr"><is><t>{value}</t></is></c>'
        if value not in strings:
            strings.append(value)
        return f'<c r="{ref}" t="s"><v>{strings.index(value)}</v></c>'

    body = ""
    for i, row in enumerate([HEAD] + rows, start=1):
        body += f'<row r="{i}">' + "".join(
            cell(f"{'ABCDEF'[j]}{i}", v) for j, v in enumerate(row)
            if v is not None) + "</row>"
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("xl/workbook.xml", f'<workbook {ns} xmlns:r="http://schemas.'
                   'openxmlformats.org/officeDocument/2006/relationships"><sheets>'
                   '<sheet name="s" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
                   '2006/relationships"><Relationship Id="rId1" Type="x" '
                   'Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr("xl/sharedStrings.xml", f"<sst {ns}>" + "".join(
            f"<si><t>{s}</t></si>" for s in strings) + "</sst>")
        z.writestr("xl/worksheets/sheet1.xml",
                   f"<worksheet {ns}><sheetData>{body}</sheetData></worksheet>")
    return buf.getvalue()


ROWS = [
    ["AAA", "2023", 2022, "Weather extremes", "N/A", "N/A"],
    ["AAA", "2024", 2023, "Economic shocks", "Weather extremes", "None"],
    ["AAA", "2025", 2024, "Conflict/insecurity", "Economic shocks", "Weather extremes"],
    ["AAA", "2025 MYU", 2025, "Weather extremes", "Conflict/Insecurity", None],
    ["BBB", "2024", 2023, "None", "None", "None"],
    ["BBB", "2025", 2024, "N/A", "N/A", "N/A"],
    ["CCC", "2024", 2023, "Economic shocks", "N/A", "N/A"],
    ["CCC", "2025 MYU", 2023, "Weather extremes", "Crop pests", "N/A"],
    ["DDD", "2024", 2023, "Pests and diseases", "N/A", "N/A"],
]


@pytest.mark.parametrize("inline", [False, True])
def test_rows_are_read_by_header(inline):
    rows = drivers.read_rows(xlsx(ROWS, inline=inline))
    assert len(rows) == len(ROWS)
    assert rows[0]["ISO Code 3"] == "AAA"
    assert rows[0]["Year of reference"] == "2022"
    assert rows[3]["Tertiary driver"] == ""


def test_the_primary_driver_is_the_label_and_secondaries_stay_verbatim():
    rows = drivers.read_rows(xlsx(ROWS))
    a = drivers.assign(rows, "AAA", "2024-08")
    assert a == {"driver": "conflict", "primary": "Conflict/insecurity",
                 "secondary": ["Economic shocks", "Weather extremes"],
                 "grfc_edition": "2025", "year_of_reference": 2024}
    assert drivers.assign(rows, "AAA", "2022-03")["driver"] == "weather"
    assert drivers.assign(rows, "AAA", "2023-01")["secondary"] == ["Weather extremes"]


def test_the_later_edition_wins_and_casing_is_kept():
    rows = drivers.read_rows(xlsx(ROWS))
    a = drivers.assign(rows, "AAA", "2025-06")
    assert a["grfc_edition"] == "2025 MYU"
    assert a["secondary"] == ["Conflict/Insecurity"]
    c = drivers.assign(rows, "CCC", "2023-11")
    assert (c["driver"], c["grfc_edition"], c["secondary"]) == (
        "weather", "2025 MYU", ["Crop pests"])


def test_no_row_none_na_or_unknown_primary_is_unassigned():
    rows = drivers.read_rows(xlsx(ROWS))
    assert drivers.assign(rows, "AAA", "2026-01")["driver"] == "unassigned"
    assert drivers.assign(rows, "AAA", "2026-01")["grfc_edition"] is None
    assert drivers.assign(rows, "BBB", "2023-05")["driver"] == "unassigned"
    assert drivers.assign(rows, "BBB", "2024-05")["driver"] == "unassigned"
    d = drivers.assign(rows, "DDD", "2023-05")
    assert (d["driver"], d["primary"]) == ("unassigned", "Pests and diseases")


def test_the_rule_never_says_drought_or_mixed():
    assert set(drivers.PRIMARY.values()) == {"conflict", "economic", "weather"}


def test_an_unknown_edition_is_refused():
    rows = drivers.read_rows(xlsx([["EEE", "2025 X", 2024, "Economic shocks",
                                    "N/A", "N/A"]]))
    with pytest.raises(ValueError):
        drivers.assign(rows, "EEE", "2024-01")


def test_the_preserved_grfc_file_gives_seven_of_eight():
    """Regression on the committed probe (audit 2026-10-22). Not an entry:
    interval/drivers.json is untouched until the maintainer's window question
    is settled (REQUESTS.md, 2026-10-22)."""
    got = {(e["country"], e["t0"]): (e["driver"], e["grfc_edition"])
           for e in drivers.derive(REPO, GRFC)}
    assert got == {
        ("AFG", "2021-10"): ("conflict", "2022"),
        ("AFG", "2025-10"): ("economic", "2025 MYU"),
        ("DJI", "2023-04"): ("economic", "2024"),
        ("SDN", "2023-06"): ("conflict", "2024"),
        ("SOM", "2022-03"): ("weather", "2023"),
        ("SOM", "2024-08"): ("weather", "2025"),
        ("SOM", "2026-01"): ("unassigned", None),
        ("YEM", "2025-06"): ("economic", "2025 MYU"),
    }


def test_verify_rederives_the_rule_independently():
    v = verifier()
    rows = v._iv_grfc_rows((REPO / GRFC).read_bytes())
    for e in drivers.derive(REPO, GRFC):
        assert v._iv_grfc_assign(rows, e["country"], e["t0"]) == {
            k: e[k] for k in ("driver", "primary", "secondary", "grfc_edition",
                              "year_of_reference")}


def check(root):
    problems = []
    verifier().check_interval_drivers(root, problems)
    return problems


def good(tmp_path):
    src = tmp_path / "interval/probes/x/grfc.xlsx"
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_bytes(xlsx(ROWS))
    return [drivers.entry(tmp_path, "interval/probes/x/grfc.xlsx", "AAA", "2024-08"),
            drivers.entry(tmp_path, "interval/probes/x/grfc.xlsx", "AAA", "2026-01")]


def test_verify_accepts_entries_the_rule_wrote(tmp_path):
    entries = good(tmp_path)
    (tmp_path / "interval/drivers.json").write_text(json.dumps({"drivers": entries}))
    assert entries[1]["source"] is None and entries[1]["grfc_file"]
    assert check(tmp_path) == []


@pytest.mark.parametrize("field,value,needle", [
    ("driver", "drought", "differs from drivers-grfc-v1"),
    ("secondary", ["Economic shocks"], "differs from drivers-grfc-v1"),
    ("grfc_edition", "2024", "differs from drivers-grfc-v1"),
    ("source_sha256", "0" * 64, "changed without its hash"),
    ("rule", "drivers-grfc-v0", "unknown rule"),
    ("grfc_file", "interval/probes/x/missing.xlsx", "not committed"),
    ("source", "https://example.invalid/", "source is not the GRFC file"),
])
def test_verify_refuses_a_hand_edit(tmp_path, field, value, needle):
    entries = good(tmp_path)
    entries[0][field] = value
    (tmp_path / "interval/drivers.json").write_text(json.dumps({"drivers": entries}))
    assert any(needle in p for p in check(tmp_path))


def test_entries_without_a_rule_are_left_to_the_register_check(tmp_path):
    (tmp_path / "interval").mkdir()
    (tmp_path / "interval/drivers.json").write_text(json.dumps({"drivers": [
        {"country": "AAA", "t0": "2024-08", "driver": "unassigned", "source": None}]}))
    assert check(tmp_path) == []
