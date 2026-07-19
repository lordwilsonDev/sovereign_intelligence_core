from __future__ import annotations

import time
from fastapi.testclient import TestClient
from msb_v2.api.web import create_app


def test_control_chat_returns_status():
    client = TestClient(create_app())
    client.headers["Authorization"] = "Bearer test"
    r = client.post("/chat", json={"message": "hello sovereign", "profile_id": "p1"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["accepted"] is True
    assert "processed_count" in body


def test_control_runtime_lifecycle():
    client = TestClient(create_app())
    client.headers["Authorization"] = "Bearer test"
    start = client.post("/runtime/start", json={"profile_id": "ctrl1", "display_name": "Ctrl", "memory_partition": "ctrl/1"})
    assert start.status_code == 200
    assert start.json()["ok"] is True
    time.sleep(0.05)
    status = client.get("/runtime/status")
    assert status.status_code == 200
    assert len([p for p in status.json() if p["profile_id"] == "ctrl1"]) == 1
    stop = client.post("/runtime/stop?profile_id=ctrl1")
    assert stop.status_code == 200
    assert stop.json()["ok"] is True
