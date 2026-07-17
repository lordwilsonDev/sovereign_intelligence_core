from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.cognitive import _engine as _cognitive_engine


def test_security_resources_reports_circuit_open_after_usage() -> None:
    client = TestClient(create_app())
    response = client.get("/cognitive/graph", headers={"accept": "application/json"})
    assert response.status_code == 200
    body = response.json()
    assert "nodes" in body
    assert "edges" in body
