from __future__ import annotations

import os

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_live_smoke_brain_run() -> None:
    r = client.post("/brain/run", json={"query": "smoke", "intent": "default"})
    assert r.status_code == 200
    payload = r.json()
    assert payload["status"] == "ok"
    assert "task_id" in payload
    assert "metrics" in payload


def test_live_smoke_runtime_snapshots() -> None:
    r = client.post("/runtime/snapshots", json={"tag": "smoke-test", "source": os.path.abspath("docs")})
    assert r.status_code == 200
    assert r.json()["tag"] == "smoke-test"

    r = client.get("/runtime/snapshots?tag=smoke-test")
    assert r.status_code == 200
    body = r.json()
    assert body["tag"] == "smoke-test"
    assert len(body["snapshots"]) >= 1


def test_live_smoke_evolution_scan() -> None:
    r = client.post("/evolution/scan")
    assert r.status_code == 200
    body = r.json()
    assert "hotspots" in body


def test_live_smoke_integrations_content() -> None:
    r = client.get("/integrations/content/articles")
    assert r.status_code == 200
    body = r.json()
    assert "articles" in body

    r = client.post("/integrations/content/refresh", json={"urls": []})
    assert r.status_code == 200
    assert r.json()["added"] == []
