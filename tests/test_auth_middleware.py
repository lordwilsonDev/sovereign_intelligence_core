from __future__ import annotations

import json

from auth.jwt import issue_token
from fastapi.testclient import TestClient

from msb_v2.api.agent import router as agent_router
from msb_v2.api.main import create_app
from msb_v2.api.middleware import require_bearer_token


def _app():
    app = create_app()
    app.include_router(agent_router, prefix="")
    return app


def test_protected_route_blocks_missing_bearer(monkeypatch: "pytest.MonkeyPatch") -> None:
    monkeypatch.delenv("MSB_AUTH_LOCAL_BYPASS", raising=False)
    client = TestClient(_app())
    payload = json.dumps({"run_id": "r1", "tasks": []}).encode()
    response = client.post("/agent/run", content=payload, headers={"Content-Type": "application/json"})
    assert response.status_code == 401
    body = response.json()
    assert body["detail"] == "Missing bearer token"


def test_protected_route_blocks_invalid_bearer(monkeypatch: "pytest.MonkeyPatch") -> None:
    monkeypatch.delenv("MSB_AUTH_LOCAL_BYPASS", raising=False)
    client = TestClient(_app())
    payload = json.dumps({"run_id": "r1", "tasks": []}).encode()
    response = client.post("/agent/run", content=payload, headers={"Content-Type": "application/json", "Authorization": "Bearer bad"})
    assert response.status_code == 401
    body = response.json()
    assert body["detail"] == "malformed_token"


def test_protected_route_allows_valid_bearer(monkeypatch: "pytest.MonkeyPatch") -> None:
    monkeypatch.delenv("MSB_AUTH_LOCAL_BYPASS", raising=False)
    client = TestClient(_app())
    token = issue_token("user-1", roles=["ops"], scopes=["system:read"])
    payload = json.dumps({"run_id": "r1", "tasks": []}).encode()
    response = client.post("/agent/run", content=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_environment_bypass_allows_unauthenticated(monkeypatch: "pytest.MonkeyPatch") -> None:
    monkeypatch.setenv("MSB_AUTH_LOCAL_BYPASS", "1")
    client = TestClient(_app())
    payload = json.dumps({"run_id": "r1", "tasks": []}).encode()
    response = client.post("/agent/run", content=payload, headers={"Content-Type": "application/json"})
    assert response.status_code == 200
