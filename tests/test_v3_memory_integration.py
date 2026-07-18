from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_v3_memory_ingest_and_recall():
    r = client.post("/v3/memory/ingest", json={
        "memory_id": "it-1",
        "source": "integration-test",
        "content": "inference latency dropped after cache warmup",
        "memory_type": "procedural",
        "importance": 0.9,
        "created_at": "2026-07-18T00:00:00Z",
    })
    assert r.status_code == 200
    assert r.json()["ingested"] is True

    r = client.get("/v3/memory/search", params={"q": "cache", "limit": 5})
    assert r.status_code == 200
    body = r.json()
    assert body["query"] == "cache"
    assert body["count"] >= 1
    sources = [e["source"] for e in body["entries"]]
    assert "integration-test" in sources


def test_v3_planner_plan_recalls_memory():
    client.post("/v3/memory/ingest", json={
        "memory_id": "it-2",
        "source": "planner-seed",
        "content": "prefer batching small writes",
        "memory_type": "procedural",
        "importance": 0.7,
        "created_at": "2026-07-18T00:00:00Z",
    })
    r = client.post("/v3/planner/plan", json={"task": "optimize writes"})
    assert r.status_code == 200
    body = r.json()
    assert "recalled_count" in body
    assert "plan" in body


def test_v3_memory_recent_endpoint():
    r = client.get("/v3/memory/recent", params={"limit": 10})
    assert r.status_code == 200
    body = r.json()
    assert "entries" in body
    assert "count" in body


def test_v3_planner_with_graph_next_step():
    client.post("/v3/memory/ingest", json={
        "memory_id": "it-3",
        "source": "alpha",
        "content": "observed alpha behavior",
        "memory_type": "episodic",
        "importance": 0.8,
        "created_at": "2026-07-18T00:00:00Z",
    })
    r = client.post("/v3/planner/plan", json={"task": "explore alpha"})
    assert r.status_code == 200
    body = r.json()
    assert "next_step" in body
