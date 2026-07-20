from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass


def test_orchestrate_orca_worktree_intent_returns_session() -> None:
    client = TestClient(create_app())
    set_local_bypass(True)
    try:
        body = {
            "tasks": [],
            "intent": "orca_worktree",
            "metadata": {"repo": "/Users/lordwilson/msb-v2", "agent": "default"},
        }
        r = client.post("/orchestrate", json=body)
    finally:
        set_local_bypass(None)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert data and data[0]["status"] == "orchestrated"
    assert data[0]["intent"] == "orca_worktree"
    assert "session_id" in data[0]["worktree"]
