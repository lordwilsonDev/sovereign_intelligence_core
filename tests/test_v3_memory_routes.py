from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_v3_memory_ingest_and_search() -> None:
    payload = {
        "source": "smoke",
        "content": "alpha beta smoke",
        "memory_type": "fact",
        "importance": 1.0,
    }
    response = client.post("/v3/memory/ingest", json=payload)
    assert response.status_code == 200, response.json()
    body = response.json()
    assert body.get("ingested") is True
    memory_id = body.get("memory_id")
    assert memory_id

    search = client.get("/v3/memory/search", params={"q": "alpha", "limit": 10})
    assert search.status_code == 200
    results = search.json()
    assert results.get("count", 0) >= 1
    assert any(entry.get("memory_id") == memory_id for entry in results.get("entries", []))


def test_v3_memory_ingest_batch_and_recent() -> None:
    batch = [
        {"source": "batch", "content": "omega one", "memory_type": "fact", "importance": 1.0},
        {"source": "batch", "content": "omega two", "memory_type": "fact", "importance": 1.0},
    ]
    response = client.post("/v3/memory/ingest/batch", json=batch)
    assert response.status_code == 200
    body = response.json()
    assert body.get("ingested") == 2
    assert len(body.get("memory_ids", [])) == 2

    recent = client.get("/v3/memory/recent", params={"limit": 10})
    assert recent.status_code == 200
    body = recent.json()
    assert body.get("count", 0) >= 2
