from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_v3_tools_list() -> None:
    r = client.get("/v3/tools")
    assert r.status_code == 200
    body = r.json()
    assert "tools" in body
    assert "web_search" in body["tools"]


def test_v3_tools_schema() -> None:
    r = client.get("/v3/tools/schema")
    assert r.status_code == 200
    body = r.json()
    assert "tools" in body
    assert len(body["tools"]) >= 1
    assert body["tools"][0]["type"] == "function"


def test_v3_tools_detail() -> None:
    r = client.get("/v3/tools/web_search")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "web_search"
    assert "query" in body["parameters"]
