"""The Interval register: constructed snapshots in a temporary tree, no
network; and the committed register against its rebuild."""

import importlib.util
import json
from pathlib import Path

import pytest

from practice.interval import register
from practice.preserve import Snapshot

REPO = Path(__file__).resolve().parents[2]
HEADER = ("Date of analysis,Country,Total country population,Validity period,"
          "From,To,Phase,Number,Percentage\n")
MON = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def verifier():
    spec = importlib.util.spec_from_file_location("verify_iv", REPO / "verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ipc_rows(country, month, share, pop=1000):
    """One analysis: current and first projection, phase 4 = share x pop."""
    y, m = month.split("-")
    label = f"{MON[int(m) - 1]} {y}"
    out = ""
    for period in ("current", "first projection"):
        p4 = int(share * pop) if period == "first projection" else 0
        out += f"{label},{country},{pop},{period},x,x,all,{pop},1.0\n"
        for phase in ("3+", "1", "2", "3"):
            out += f"{label},{country},{pop},{period},x,x,{phase},0,0\n"
        out += f"{label},{country},{pop},{period},x,x,4,{p4},0\n"
        out += f"{label},{country},{pop},{period},x,x,5,0,0\n"
    return out


def flow(fid, month, amount):
    return {"id": fid, "versionId": 1, "amountUSD": amount, "status": "paid",
            "boundary": "incoming", "flowType": "Standard",
            "date": f"{month}-15T00:00:00Z",
            "firstReportedDate": f"{month}-15T00:00:00Z"}


def pages_bytes(flows, per_page=5, last_has_next=False):
    chunks = [flows[i:i + per_page] for i in range(0, len(flows), per_page)]
    out = []
    for i, chunk in enumerate(chunks):
        nxt = "next" if i < len(chunks) - 1 or last_has_next else None
        out.append(json.dumps({"data": {"flows": chunk},
                               "meta": {"nextLink": nxt}}).encode())
    return out


def tree(tmp_path, *, total_incomplete=False):
    """XXX onset 2022-03 at 5 % and 10 % (quiet since 2021-03); YYY above
    10 % from its first analysis (left-censored)."""
    csv = HEADER
    for month in ("2021-03", "2021-06", "2021-09"):
        csv += ipc_rows("XXX", month, 0.01)
    csv += ipc_rows("XXX", "2022-03", 0.12)
    csv += ipc_rows("YYY", "2021-03", 0.30)
    snap = Snapshot(tmp_path, "2026-10-01", base=register.SNAPSHOTS)
    snap.preserve(register.IPC_FILE, csv.encode(), "u", 200)
    flows = [flow(f"b{i}", f"2021-{i:02d}", 10) for i in range(3, 13)]
    flows += [flow("b13", "2022-01", 10), flow("b14", "2022-02", 10),
              flow("r1", "2022-05", 30)]
    for i, data in enumerate(pages_bytes(flows), 1):
        snap.preserve(f"fts/XXX/fsc-2021_2022_2023-p{i:03d}.json", data, "u", 200)
    for i, data in enumerate(pages_bytes(flows, last_has_next=True), 1):
        snap.preserve(f"fts/XXX/total-2021_2022_2023-p{i:03d}.json", data,
                      "u", 200)
    snap.write_manifest()
    return tmp_path


def test_episode_grid_and_left_censoring(tmp_path):
    reg = register.build(tree(tmp_path))
    assert reg["left_censored"] == {"0.05": ["YYY"], "0.10": ["YYY"],
                                    "0.25": ["YYY"]}
    [ep] = reg["episodes"]
    assert (ep["country"], ep["t0"]) == ("XXX", "2022-03")
    assert ep["onset_at_theta"] == ["0.05", "0.10"]
    assert ep["w"] == 0.12 and ep["blocks"] == 1
    assert ep["window"] == ["2021-03", "2023-02"]
    assert ep["driver"] == {"driver": "unassigned", "source": None}
    fsc = ep["money"]["fsc"]
    assert fsc["status"] == "read" and fsc["as_of"] == "2026-10"
    assert fsc["flows"] == 13 and len(fsc["cells"]) == 4
    k2 = next(c for c in fsc["cells"] if c["k"] == 2 and c["axis"] == "date")
    k3 = next(c for c in fsc["cells"] if c["k"] == 3 and c["axis"] == "date")
    assert (k2["t1"], k2["gap_months"], k2["status"]) == ("2022-05", 2, "closed")
    assert (k3["t1"], k3["gap_months"], k3["status"]) == ("2022-05", 2, "closed")


def test_incomplete_page_set_is_not_preserved_never_estimated(tmp_path):
    reg = register.build(tree(tmp_path))
    total = reg["episodes"][0]["money"]["total"]
    assert total == {"status": "not_preserved",
                     "boundary_years": "2021,2022,2023"}


def test_driver_needs_a_source(tmp_path):
    root = tree(tmp_path)
    (root / "interval").mkdir(exist_ok=True)
    (root / register.DRIVERS).write_text(json.dumps({"drivers": [
        {"country": "XXX", "t0": "2022-03", "driver": "drought",
         "source": None}]}))
    with pytest.raises(ValueError, match="needs a source"):
        register.build(root)
    (root / register.DRIVERS).write_text(json.dumps({"drivers": [
        {"country": "XXX", "t0": "2022-03", "driver": "drought",
         "source": "interval/snapshots/x"}]}))
    ep = register.build(root)["episodes"][0]
    assert ep["driver"] == {"driver": "drought", "source": "interval/snapshots/x"}


def test_verify_recomputes_the_register_independently(tmp_path):
    root = tree(tmp_path)
    register.write(root)
    v = verifier()
    problems = []
    v.check_interval(root, problems)
    assert problems == []
    doc = json.loads((root / register.REGISTER).read_text())
    doc["episodes"][0]["money"]["fsc"]["cells"][0]["gap_months"] = 0
    (root / register.REGISTER).write_text(json.dumps(doc))
    problems = []
    v.check_interval(root, problems)
    assert problems == ["interval/register.json: episode XXX 2022-03 differs "
                        "from its recomputation"]


def test_committed_register_is_its_own_rebuild():
    path = REPO / register.REGISTER
    if not path.exists():
        pytest.skip("no committed register")
    assert json.loads(path.read_text()) == register.build(REPO)
