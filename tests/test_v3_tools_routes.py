from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_v3_tools_list_returns_registry() -> None:
    response = client.get("/v3/tools")
    assert response.status_code == 200
    body = response.json()
    assert "tools" in body
    assert isinstance(body["tools"], list)
    assert len(body.get("tools", [])) >= 2


def test_v3_tools_schema_non_empty() -> None:
    response = client.get("/v3/tools/schema")
    assert response.status_code == 200
    body = response.json()
    assert "tools" in body
    assert isinstance(body["tools"], list)
    assert len(body["tools"]) >= 2
    assert any(item.get("function", {}).get("name") == "web_search" for item in body["tools"])
