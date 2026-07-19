from __future__ import annotations

import json

import pytest
from auth.jwt import issue_token
from fastapi.testclient import TestClient

from msb_v2.api.agent import router as agent_router
from msb_v2.api.desktop import router as desktop_router
from msb_v2.api.main import create_app
from msb_v2.api.recovery import router as recovery_router
from msb_v2.api.runtime import router as runtime_router
from msb_v2.api.security import router as security_router


def _app() -> object:
    app = create_app()
    app.include_router(agent_router, prefix="")
    app.include_router(runtime_router, prefix="")
    app.include_router(recovery_router, prefix="")
    app.include_router(security_router, prefix="")
    app.include_router(desktop_router, prefix="")
    return app


def test_valid_bearer_allows() -> None:
    token = issue_token("u1", roles=["ops"], scopes=["system:read"])
    client = TestClient(_app())
    response = client.post(
        "/agent/run",
        content=json.dumps({"run_id": "r1", "tasks": []}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_environment_bypass_allows_no_token(monkeypatch: "pytest.MonkeyPatch") -> None:
    monkeypatch.setenv("MSB_AUTH_LOCAL_BYPASS", "1")
    client = TestClient(_app())
    response = client.post(
        "/agent/run",
        content=json.dumps({"run_id": "r1", "tasks": []}).encode(),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
