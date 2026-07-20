from __future__ import annotations

import json
from typing import Any, Dict, Optional

import pytest
from auth.jwt import issue_token
from fastapi import FastAPI
from fastapi.testclient import TestClient

from msb_v2.api.agent import router as agent_router
from msb_v2.api.desktop import router as desktop_router
from msb_v2.api.main import create_app
from msb_v2.api.middleware import _bypass_context, set_local_bypass
from msb_v2.api.recovery import router as recovery_router
from msb_v2.api.runtime import router as runtime_router
from msb_v2.api.security import router as security_router


def _build_app() -> FastAPI:
    app = create_app()
    for r in (agent_router, runtime_router, recovery_router, security_router, desktop_router):
        app.include_router(r, prefix="")
    return app


def _raw(token: Optional[str]) -> Any:
    client = TestClient(_build_app())
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return client.post(
        "/agent/run",
        content=json.dumps({"run_id": "r1", "tasks": []}).encode(),
        headers=headers,
    )


def test_valid_bearer_allows() -> None:
    token = issue_token("u1", roles=["ops"], scopes=["system:read"])
    assert _raw(token).status_code == 200


def test_missing_bearer_blocks() -> None:
    set_local_bypass(False)
    try:
        assert _raw(None).status_code == 401
    finally:
        set_local_bypass(None)


def test_bad_bearer_blocks() -> None:
    set_local_bypass(False)
    try:
        assert _raw("bad").status_code == 401
    finally:
        set_local_bypass(None)


def _route_requires_token(path: str, method: str = "post", json_body: Optional[Dict[str, Any]] = None) -> bool:
    set_local_bypass(False)
    try:
        client = TestClient(_build_app())
        response = (client.get(path) if method == "get" else client.post(path, json=json_body or {}))
    finally:
        set_local_bypass(None)
    return response.status_code == 401


def test_runtime_rollback_requires_token() -> None:
    assert _route_requires_token("/runtime/snapshots/rollback", "post", {"tag": "x", "dest": "/tmp/x"})


def test_recovery_requires_token() -> None:
    assert _route_requires_token("/recovery/rollback/r1", "get")


def test_security_requires_token() -> None:
    assert _route_requires_token("/security/rotate", "post")


def test_desktop_requires_token() -> None:
    assert _route_requires_token("/desktop/stop", "post")


def test_token_issue_validation():
    set_local_bypass(False)
    client = TestClient(_build_app())
    # canonical owner is msb_v2.api.policy; require subject/action/resource in body
    assert client.post("/auth/token/issue", json={}).status_code == 422
    assert client.post("/auth/token/issue", json={"subject": "ab", "action": "read", "resource": "x"}).status_code == 200
    assert client.post("/auth/token/issue", json={"subject": "ok", "action": "read", "resource": "x", "roles": ["admin"]}).status_code == 200
    issue = client.post("/auth/token/issue", json={"subject": "ok", "action": "read", "resource": "x", "roles": ["admin"], "scopes": ["read"]}).json()
    assert issue["subject"] == "ok"
    assert issue["token"]


def test_model_route_requires_token() -> None:
    assert _route_requires_token("/model/route", "post", {"task": "x"})


def test_reasoning_traces_require_token() -> None:
    assert _route_requires_token(
        "/reasoning/traces",
        "post",
        {
            "trace_id": "rt-1",
            "title": "t",
            "status": "completed",
            "steps": [{"step_index": 0, "claim": "c", "evidence_refs": [], "assumptions": [], "confidence": 1.0, "metadata": {"kind": "strategic"}}],
            "decision_id": "d1",
            "memory_ids": [],
            "conclusion": "",
            "metadata": {},
        },
    )
