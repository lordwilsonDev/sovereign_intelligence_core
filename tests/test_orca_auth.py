"""Explicit auth enforcement for Orca routes."""
from __future__ import annotations

import os
from typing import Any, Generator

import pytest

from msb_v2.api.middleware import set_local_bypass
from msb_v2.api.web import create_app
from starlette.testclient import TestClient


@pytest.fixture()
def app_no_bypass() -> Generator[Any, None, None]:
    set_local_bypass(None)
    application = create_app()
    yield application
    set_local_bypass(None)


@pytest.fixture()
def client_no_bypass(app_no_bypass) -> Generator[TestClient, None, None]:
    yield TestClient(app_no_bypass)


@pytest.fixture()
def app_with_bypass() -> Generator[Any, None, None]:
    set_local_bypass(True)
    application = create_app()
    yield application
    set_local_bypass(None)


@pytest.fixture()
def client_with_bypass(app_with_bypass) -> Generator[TestClient, None, None]:
    yield TestClient(app_with_bypass)


def test_orca_status_without_auth_returns_200(client_no_bypass: TestClient):
    r = client_no_bypass.get("/orchestrate/orca/status")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["adapter"] == "git-worktree-python"
    assert "mode" in body


def test_orca_worktree_create_without_auth_returns_401(client_no_bypass: TestClient):
    r = client_no_bypass.post("/orchestrate/orca/worktree/create", json={"repo": "/tmp", "agent": "a1"})
    assert r.status_code == 401, r.text


def test_orca_snapshot_with_bin_but_no_auth_returns_401(client_no_bypass: TestClient, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("ORCA_BIN", "/usr/local/bin/fake-orca")
    r = client_no_bypass.get("/orchestrate/orca/browser/snapshot")
    assert r.status_code == 401, r.text


def test_orca_status_with_local_bypass_allowed(client_with_bypass: TestClient):
    r = client_with_bypass.get("/orchestrate/orca/status")
    assert r.status_code == 200, r.text


def test_orca_worktree_create_with_local_bypass_allowed(client_with_bypass: TestClient, tmp_path):
    repo = str(tmp_path)
    os.system(f"git init {repo} >/dev/null 2>&1")
    os.system(f"git -C {repo} config user.email test@test.com")
    os.system(f"git -C {repo} config user.name Test")
    open(os.path.join(repo, "f"), "w").write("x")
    os.system(f"git -C {repo} add f")
    os.system(f"git -C {repo} commit -m init >/dev/null 2>&1")
    r = client_with_bypass.post("/orchestrate/orca/worktree/create", json={"repo": repo, "agent": "a1"})
    assert r.status_code == 200, r.text
