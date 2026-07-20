from __future__ import annotations

import os
import time
from unittest import mock

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_control_chat_returns_status(client):
    os.environ["MSB_AUTH_LOCAL_BYPASS"] = "1"
    client.headers["Authorization"] = "Bearer test"
    client.post("/runtime/start", json={"profile_id": "p1", "display_name": "P1", "memory_partition": "p1/1"})
    with mock.patch("msb_v2.control.control_router._gateway") as gw:
        instance = gw
        instance.quarantine.return_value = {"reason": "mock"}
        instance.recent.return_value = []
        r = client.post("/chat", json={"message": "hello sovereign", "profile_id": "p1"})
    assert r.status_code == 200
    body = r.json()
    assert body.get("ok") is True
    assert body.get("accepted") is True
    assert "processed_count" in body


def test_control_runtime_lifecycle(client):
    os.environ["MSB_AUTH_LOCAL_BYPASS"] = "1"
    client.headers["Authorization"] = "Bearer test"
    start = client.post("/runtime/start", json={"profile_id": "ctrl1", "display_name": "Ctrl", "memory_partition": "ctrl/1"})
    assert start.status_code == 200
    assert start.json().get("ok") is True
    time.sleep(0.05)
    status = client.get("/runtime/status")
    assert status.status_code == 200
    assert len([p for p in status.json() if p.get("profile_id") == "ctrl1"]) == 1
    stop = client.post("/runtime/stop?profile_id=ctrl1")
    assert stop.status_code == 200
    assert stop.json().get("ok") is True
