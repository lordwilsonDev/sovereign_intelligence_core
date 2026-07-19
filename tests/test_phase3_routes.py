from __future__ import annotations

import contextlib
from typing import Generator

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_scheduler_submit_status_queue() -> None:
    client = TestClient(create_app())
    r = client.post("/scheduler/submit", json={"goal": "schedule-health", "priority": 2})
    assert r.status_code == 200
    task_id = r.json()["task_id"]
    status = client.get(f"/scheduler/status/{task_id}")
    assert status.status_code == 200
    assert status.json()["status"] in {"queued", "running", "completed"}


def test_knowledge_graph_endpoints() -> None:
    client = TestClient(create_app())
    node = client.post("/knowledge/nodes", json={"id": "n1", "labels": ["Person"], "properties": {"name": "A"}})
    assert node.status_code == 200
    assert node.json()["id"] == "n1"
    edge = client.post("/knowledge/edges", json={"source": "n1", "target": "n2", "relation": "DECIDED"})
    assert edge.status_code == 200
    assert edge.json()["relation"] == "DECIDED"


def test_security_rotate_and_secret_store_are_scaffolded() -> None:
    client = TestClient(create_app())
    with _bearer(client):
        rotate = client.post("/security/rotate", json={})
        assert rotate.status_code == 200
        assert rotate.json()["rotated"] is True
        assert rotate.json()["rotation_count"] == 1
        secret = client.post("/security/secret/store", json={"secret": "1234567890123456"})
        assert secret.status_code == 200
        assert secret.json()["stored"] is True
        assert secret.json()["metadata"]["length"] >= 16


def test_public_auth_token_issue_returns_token() -> None:
    client = TestClient(create_app())
    response = client.post("/auth/token/issue", json={"subject": "user-1", "roles": ["admin"], "scopes": ["system:read", "token:issue"]})
    assert response.status_code == 200
    body = response.json()
    assert body.get("token")
    assert body.get("subject") == "user-1"


@contextlib.contextmanager
def _bearer(client: TestClient) -> Generator[None, None, None]:
    token = _issue_test_token(client)
    client.headers["Authorization"] = f"Bearer {token}"
    try:
        yield
    finally:
        client.headers.pop("Authorization", None)


def _issue_test_token(client: TestClient) -> str:
    res = client.post("/auth/token/issue", json={"subject": "test-bypass", "roles": ["admin"], "scopes": ["*"]})
    assert res.status_code == 200, res.text
    return res.json()["token"]
