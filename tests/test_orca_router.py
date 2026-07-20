from __future__ import annotations

import os
import subprocess
import tempfile

from pathlib import Path

import pytest

from msb_v2.api.web import create_app
from msb_v2.v3.contracts import all_contracts


@pytest.fixture
def git_repo():
    path = tempfile.mkdtemp(prefix="msb-orca-git-")
    subprocess.run(["git", "init", path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "-C", path, "config", "user.email", "msb@example.invalid"], check=True)
    subprocess.run(["git", "-C", path, "config", "user.name", "MSB Orca Adapter"], check=True)
    (Path(path) / "README.md").write_text("# repo\n")
    subprocess.run(["git", "-C", path, "add", "README.md"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(
        ["git", "-C", path, "commit", "-m", "seed"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        yield path
    finally:
        for branch in ["master", "main"]:
            subprocess.run(["git", "-C", path, "branch", "-D", branch], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            os.remove(os.path.join(path, ".git", "index"))
        except FileNotFoundError:
            pass
        try:
            os.rmdir(path)
        except OSError:
            pass


@pytest.fixture
def client():
    app = create_app()
    from fastapi.testclient import TestClient
    return TestClient(app)


def test_orca_status_returns_registry():
    app = create_app()
    from msb_v2.orca.router import router as orca_router
    assert any(route.path == "/orchestrate/orca/status" for route in orca_router.routes)


def test_orca_status(client):
    r = client.get("/orchestrate/orca/status")
    assert r.status_code == 200
    body = r.json()
    assert body["adapter"] == "git-worktree-python"
    assert "mode" in body


def test_orca_worktree_create_missing_repo(client):
    r = client.post("/orchestrate/orca/worktree/create", json={"repo": "/missing/path", "agent": "a1"})
    assert r.status_code == 400


def test_orca_worktree_create_ok(client, git_repo):
    r = client.post("/orchestrate/orca/worktree/create", json={"repo": git_repo, "agent": "a1"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True
    assert body["worktree_id"] == Path(body["worktree_root"]).name
    assert body["session_id"].startswith(f"{Path(git_repo).name}-a1-")
    assert body["agent"] == "a1"
    assert body["branch"].startswith("msb/a1/")


def test_orca_worktree_status(client, git_repo):
    create = client.post("/orchestrate/orca/worktree/create", json={"repo": git_repo, "agent": "a1"}).json()
    session_id = create["session_id"]
    r = client.get(f"/orchestrate/orca/worktree/{session_id}", params={"repo": git_repo})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True
    assert body["status"] == "ready"
    assert body["branch"] is not None


def test_browser_snapshot_without_bin_returns_placeholder(client):
    r = client.get("/orchestrate/orca/browser/snapshot")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is False
    assert "ORCA_BIN" in body["html"]


def test_browser_snapshot_with_bin_normalizes_json(client, monkeypatch):
    monkeypatch.setenv("ORCA_BIN", "/usr/local/bin/fake-orca")
    import msb_v2.orca.router as _orca_module
    _orca_module._ORCA_BIN = "/usr/local/bin/fake-orca"
    payload = {"ok": True, "html": "<html><title>Hi</title><p>q</p></html>", "url": "example.com", "title": "<b>"}
    monkeypatch.setattr(_orca_module, "_cli_json", lambda *_: payload)

    r = client.get("/orchestrate/orca/browser/snapshot")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["ok"] is True
    assert body["html"] == "<html><title>Hi</title><p>q</p></html>"
    assert body["url"] == "https://example.com"
    assert body["title"] == "<b>"


def test_orca_status_maps_to_bool(client):
    r = client.get("/orchestrate/orca/status")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["git_available"] in {"true", "false"}
    assert "orca_root" in body


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
