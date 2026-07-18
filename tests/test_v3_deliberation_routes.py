from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_deliberation_returns_rounds_and_recommendation():
    r = client.post("/v3/deliberate", json={"query": "reduce latency", "max_rounds": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["query"] == "reduce latency"
    assert "rounds" in body
    assert "recommended" in body


def test_deliberation_clamps_max_rounds():
    r = client.post("/v3/deliberate", json={"query": "any", "max_rounds": 10})
    assert r.status_code == 200
    body = r.json()
    assert len(body["rounds"]) <= 3
