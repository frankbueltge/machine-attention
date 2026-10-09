"""The Interval sources: fixtures only, no network."""

import json

import pytest

from practice.fetch import SourceUnavailable
from practice.interval import sources


class FakeClient:
    def __init__(self, routes):
        self.routes = routes
        self.calls = []

    def fetch(self, url, headers=None):
        self.calls.append(url)
        return self.routes.get(url, (b"", 404))


PKG = {"result": {"resources": [
    {"name": "other.csv", "download_url": "https://x/other.csv"},
    {"name": sources.IPC_RESOURCE, "download_url": "https://x/ipc.csv"}]}}


def test_resolve_ipc_url_picks_named_resource():
    assert sources.resolve_ipc_url(PKG) == "https://x/ipc.csv"


def test_resolve_ipc_url_missing_raises():
    with pytest.raises(SourceUnavailable):
        sources.resolve_ipc_url({"result": {"resources": []}})


def test_fts_url_keeps_years_verbatim():
    assert "year=2011,2012" in sources.fts_url("SOM", "2011,2012")
    assert "year=2011-2013" in sources.fts_url("SOM", "2011-2013")
    assert "filterBy=destinationGlobalClusterCode:FSC" in sources.fts_url(
        "SOM", "2020", filter_by="destinationGlobalClusterCode:FSC")


def _page(next_link):
    return json.dumps({"data": {"flows": []},
                       "meta": {"nextLink": next_link}}).encode(), 200


def test_fts_pages_follow_next_link_and_snapshot(tmp_path):
    u1 = sources.fts_url("SOM", "2011")
    u2 = u1 + "&page=2"
    client = FakeClient({u1: _page(u2), u2: _page(None)})
    out = sources.snapshot_fts(tmp_path, "2026-10-09", client, "SOM", "2011")
    assert out == {"country": "SOM", "pages": 2, "complete": True}
    manifest = json.loads((tmp_path / sources.BASE / "2026-10-09"
                           / "manifest.json").read_text())
    assert [e["url"] for e in manifest["entries"]] == [u1, u2]
    assert all(e["file"].startswith(sources.BASE) for e in manifest["entries"])


def test_fts_failure_is_kept_and_incomplete(tmp_path):
    u1 = sources.fts_url("SOM", "2011")
    client = FakeClient({u1: (b"", 500)})
    out = sources.snapshot_fts(tmp_path, "2026-10-09", client, "SOM", "2011")
    assert out["complete"] is False and out["pages"] == 1


def test_fts_loop_ends(tmp_path):
    u1 = sources.fts_url("SOM", "2011")
    client = FakeClient({u1: _page(u1)})
    assert len(sources.fts_pages(client, u1)) == 1


def test_ipc_snapshot_then_identical_skipped(tmp_path):
    client = FakeClient({sources.HDX_PACKAGE_URL: (json.dumps(PKG).encode(), 200),
                         "https://x/ipc.csv": (b"a,b\n1,2\n", 200)})
    first = sources.snapshot_ipc(tmp_path, "2026-10-09", client)
    assert first["preserved"] is True
    second = sources.snapshot_ipc(tmp_path, "2026-10-16", client)
    assert second["preserved"] is False
    assert not (tmp_path / sources.BASE / "2026-10-16").exists()


def test_ipc_http_error_raises(tmp_path):
    client = FakeClient({sources.HDX_PACKAGE_URL: (b"", 403)})
    with pytest.raises(SourceUnavailable):
        sources.snapshot_ipc(tmp_path, "2026-10-09", client)
