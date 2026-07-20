from __future__ import annotations

from unittest import mock

import pytest

from msb_v2.api.web import create_app
from msb_v2.orca.router import router as orca_router
from msb_v2.v3.contracts import all_contracts


@pytest.fixture
def client():
    app = create_app()
    from fastapi.testclient import TestClient
    return TestClient(app)


def test_orca_status_returns_registry():
    app = create_app()
    assert any(route.path == "/orchestrate/orca/status" for route in orca_router.routes)


def test_orca_status(client):
    r = client.get("/orchestrate/orca/status")
    assert r.status_code == 200
    body = r.json()
    assert "orca_root" in body


def test_orca_worktree_create_missing_repo(client):
    r = client.post("/orchestrate/orca/worktree/create", json={"repo": "/missing/path", "agent": "a1"})
    assert r.status_code == 400


def test_orca_worktree_create_ok(client):
    import os
    repo = "/tmp"
    r = client.post("/orchestrate/orca/worktree/create", json={"repo": repo, "agent": "a1"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert body["worktree_id"] == "tmp"
    assert body["session_id"] == "tmp-a1"


def test_orca_worktree_status(client):
    status = client.get("/orchestrate/orca/worktree/tmp-a1")
    assert status.status_code == 200
    body = status.json()
    assert body["ok"] is True
    assert body["status"] == "ready"



if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
