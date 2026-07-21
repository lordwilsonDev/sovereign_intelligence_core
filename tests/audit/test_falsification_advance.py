"""Falsification loop API regression tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


client = TestClient(create_app())


def test_policies_falsification_advance_endpoint_returns_schema() -> None:
    response = client.post("/audit/policies/falsification/advance", json={"policy": "tool_timeout_rate"})
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "advanced" in body
    assert "actions" in body
    assert "count" in body
    assert isinstance(body["actions"], list)
    assert isinstance(body["advanced"], int)
    assert body["count"] >= 0


def test_policies_falsification_advance_without_policy() -> None:
    response = client.post("/audit/policies/falsification/advance", json={})
    assert response.status_code == 200
    body = response.json()
    assert body["advanced"] == 0
    assert body["actions"] == []
    assert body["records_updated"] >= 0
    assert body["latest"] in ([], [[]])
