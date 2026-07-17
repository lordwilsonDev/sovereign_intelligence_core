from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2 import knowledge as knowledge_module


def test_security_posture_returns_svk() -> None:
    client = TestClient(create_app())
    response = client.get("/cognitive/security/posture", headers={"accept": "application/json"})
    assert response.status_code == 200
    body = response.json()
    assert "spec" in body
    assert "verifier" in body
    assert "knowledge" in body


def test_security_posture_knowledge_counts_markdown() -> None:
    snapshot = knowledge_module.snapshot()
    assert snapshot.entries > 0
    assert snapshot.links >= 0


def test_security_posture_knowledge_counts_positive_in_api() -> None:
    client = TestClient(create_app())
    response = client.get("/cognitive/security/posture", headers={"accept": "application/json"})
    assert response.status_code == 200
    body = response.json()
    knowledge = body["knowledge"]
    assert knowledge["markdown_entries"] > 0
    assert knowledge["markdown_links"] >= 0
