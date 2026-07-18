from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_v3_memory_ingest_and_search() -> None:
    payload = {"source": "smoke", "content": "alpha beta gamma", "memory_type": "fact", "importance": 1.0}
    response = client.post("/v3/memory/ingest", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["ingested"] is True
    memory_id = body["memory_id"]

    search = client.get("/v3/memory/search", params={"q": "alpha", "limit": 10})
    assert search.status_code == 200
    results = search.json()
    assert results["count"] >= 1
    assert any(entry["memory_id"] == memory_id for entry in results["entries"])


def test_v3_memory_ingest_batch_and_recent() -> None:
    batch = [
        {"source": "batch", "content": "omega one", "memory_type": "fact", "importance": 1.0},
        {"source": "batch", "content": "omega two", "memory_type": "fact", "importance": 1.0},
    ]
    response = client.post("/v3/memory/ingest/batch", json=batch)
    assert response.status_code == 200
    assert response.json()["ingested"] == 2

    recent = client.get("/v3/memory/recent", params={"limit": 10})
    assert recent.status_code == 200
    body = recent.json()
    assert body["count"] >= 2
