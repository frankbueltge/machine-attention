"""The Interval weekly reading: a constructed tree and a fake client, no
network; verify.py recomputes every decision the reading made."""

import json

from practice.interval import register, sources, weekly
from practice.preserve import read_json

from .test_interval_register import flow, tree, verifier


class FakeClient:
    def __init__(self, routes):
        self.routes = routes
        self.calls = []
        self.requests = 0
        self.http_429 = 0

    def fetch(self, url, headers=None):
        self.calls.append(url)
        self.requests += 1
        return self.routes.get(url, (b"", 404))


def fts_routes(url, flows, per_page=5):
    """Pages with distinct nextLinks, as FTS serves them."""
    chunks = [flows[i:i + per_page] for i in range(0, len(flows), per_page)]
    links = [url] + [f"{url}&page={i}" for i in range(2, len(chunks) + 1)]
    return {link: (json.dumps({"data": {"flows": chunk}, "meta": {
        "nextLink": links[i + 1] if i + 1 < len(links) else None}}).encode(),
        200) for i, (link, chunk) in enumerate(zip(links, chunks))}


def routes_for(root, flows):
    ipc = (root / register.newest_ipc(root)).read_bytes()
    pkg = {"result": {"resources": [{"name": sources.IPC_RESOURCE,
                                     "download_url": "https://x/ipc.csv"}]}}
    routes = {sources.HDX_PACKAGE_URL: (json.dumps(pkg).encode(), 200),
              "https://x/ipc.csv": (ipc, 200)}
    for tag in register.SETS:
        routes.update(fts_routes(sources.fts_url(
            "XXX", "2021,2022,2023", filter_by=register.SETS[tag]), flows))
    return routes


def committed_flows():
    flows = [flow(f"b{i}", f"2021-{i:02d}", 10) for i in range(3, 13)]
    return flows + [flow("b13", "2022-01", 10), flow("b14", "2022-02", 10),
                    flow("r1", "2022-05", 30)]


def test_frozen_needs_a_basis_past_the_grace():
    assert not weekly.frozen(None, "2023-02")
    assert not weekly.frozen("2023-05-31", "2023-02")
    assert weekly.frozen("2023-06-01", "2023-02")


def test_closed_episode_is_frozen_incomplete_one_fetched(tmp_path):
    root = tree(tmp_path, total_incomplete=True)
    client = FakeClient(routes_for(root, committed_flows()))
    reading = weekly.run(root, "2026-10-13", client)
    by_set = {q["set"]: q for q in reading["queries"]}
    # fsc: complete basis from 2026-10, far past window end 2023-02 + 3.
    assert by_set["fsc"]["decision"] == "frozen"
    assert by_set["fsc"]["basis_day"] == "2026-10-01"
    # total: its committed set ends with a nextLink, so there is no basis.
    assert by_set["total"]["decision"] == "fetch"
    assert by_set["total"]["basis_day"] is None
    assert by_set["total"]["outcome"] == "preserved"
    assert reading["ipc"]["status"] == "unchanged"
    assert not any("filterBy" in c for c in client.calls)
    reg = read_json(root / register.REGISTER)
    assert reg["episodes"][0]["money"]["total"]["as_of"] == "2026-10"
    problems = []
    verifier().check_interval_readings(root, problems)
    assert problems == []


def test_identical_pages_are_not_preserved_twice(tmp_path, monkeypatch):
    root = tree(tmp_path)
    monkeypatch.setattr(weekly, "GRACE_MONTHS", 1000)
    client = FakeClient(routes_for(root, committed_flows()))
    reading = weekly.run(root, "2026-10-13", client)
    fsc = next(q for q in reading["queries"] if q["set"] == "fsc")
    assert fsc["decision"] == "fetch"
    # The committed fixture pages carry nextLink "next", the fake serves
    # real links: different bytes, so preserved. Run again on those bytes.
    assert fsc["outcome"] == "preserved"
    again = weekly.run(root, "2026-10-20", client)
    fsc2 = next(q for q in again["queries"] if q["set"] == "fsc")
    assert fsc2["outcome"] == "unchanged"
    assert fsc2["basis_day"] == "2026-10-13"
    manifest = read_json(root / sources.BASE / "2026-10-20" / "manifest.json",
                         {"entries": []})
    assert not any("/fsc-" in e["file"] for e in manifest["entries"])


def test_verify_catches_a_forged_decision(tmp_path):
    root = tree(tmp_path)
    weekly.run(root, "2026-10-13", FakeClient(routes_for(root, committed_flows())))
    path = root / weekly.READINGS / "2026-10-13.json"
    doc = json.loads(path.read_text())
    doc["queries"][0]["decision"] = "fetch"
    path.write_text(json.dumps(doc))
    problems = []
    verifier().check_interval_readings(root, problems)
    assert any("decision differs" in p for p in problems)
