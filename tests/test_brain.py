from __future__ import annotations

import pytest

from starlette.testclient import TestClient

from msb_v2.api.main import create_app


@pytest.fixture()
def client():  # noqa: ANN001
    return TestClient(create_app())


def test_brain_fallback_noop(client):  # noqa: ANN001
    response = client.post("/brain/run", json={"query": "ping", "intent": "default"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["kind"] == "fallback"
    assert "query" in payload["payload"]
    assert payload["payload"]["resolved"] == "noop"
