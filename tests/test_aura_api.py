from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_aura_run_returns_ok_and_state() -> None:
    response = client.post("/aura/run", json={"goal": "Say hello"})
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "ok"
    assert "result" in body


def test_aura_run_with_empty_goal() -> None:
    response = client.post("/aura/run", json={"goal": ""})
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "ok"
