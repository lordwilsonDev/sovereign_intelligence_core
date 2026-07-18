from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_v3_inversion_routes() -> None:
    assert client.get("/v3/inversion/hypotheses").status_code == 200
    assert client.get("/v3/inversion/experiments").status_code == 200


def test_v3_deliberate_route() -> None:
    response = client.post("/v3/deliberate", json={"prompt": "ping"})
    assert response.status_code == 200


def test_v3_knowledge_nodes_route() -> None:
    response = client.post("/v3/knowledge/nodes", json={"label": "node1"})
    assert response.status_code == 200


def test_v3_twin_route() -> None:
    response = client.post("/v3/twin", json={"name": "twin1"})
    assert response.status_code == 200
