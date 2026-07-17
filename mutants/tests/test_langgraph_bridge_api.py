from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


@pytest.fixture
def client():
    return TestClient(create_app())


def test_langgraph_tool_calls_fallback(client):
    payload = {"tool_calls": [{"name": "echo", "args": {"message": "langgraph-bridge"}}]}
    response = client.post("/aura/langgraph/tools", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["backend"] == "fallback"
    assert body["results"] == [{"tool": "echo", "output": {"status": "ok", "message": "langgraph-bridge", "confidence": 1.0}}]
