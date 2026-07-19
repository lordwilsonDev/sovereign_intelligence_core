from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_knowledge_nodes_and_edges():
    client.post("/v3/knowledge/_reset")
    r = client.post("/v3/knowledge/nodes", json={"node_id": "a", "label": "Alpha", "weight": 0.8})
    assert r.status_code == 200
    client.post("/v3/knowledge/nodes", json={"node_id": "b", "label": "Beta", "weight": 0.4})
    client.post("/v3/knowledge/edges", json={"source": "a", "target": "b", "relation": "next", "weight": 0.9})

    r = client.get("/v3/knowledge/neighbors/a")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 1
    assert body["neighbors"][0]["target"] == "b"

    r = client.get("/v3/knowledge/shortest-path", params={"start": "a", "end": "b"})
    assert r.status_code == 200
    body = r.json()
    assert body["found"] is True
    assert body["path"] == ["a", "b"]


def test_knowledge_learning_update_and_recommend():
    client.post("/v3/knowledge/_reset")
    client.post("/v3/knowledge/nodes", json={"node_id": "x", "label": "X"})
    r = client.post("/v3/knowledge/update-outcome", json={"node_id": "x", "outcome": "success"})
    assert r.status_code == 200
    body = r.json()
    assert "heuristic" in body

    r = client.get("/v3/knowledge/recommend/x")
    assert r.status_code == 200
    body = r.json()
    assert "next" in body
