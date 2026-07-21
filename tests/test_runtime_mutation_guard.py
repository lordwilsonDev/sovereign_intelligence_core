from __future__ import annotations

import pytest

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


client = TestClient(create_app())


def test_mutation_request_requires_intent_and_actor() -> None:
    response = client.post("/runtime/mutation/request", json={})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "error"


def test_unsigned_blocking_mutation_is_blocked() -> None:
    payload = {
        "intent": "delete core module",
        "actor": "tester",
        "failure_rate": 0.8,
    }
    response = client.post("/runtime/mutation/request", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "blocked"
    rule_ids = [r["rule_id"] for r in body["policy_results"] if r["triggered"]]
    assert "re-allow-unsigned-mutation" in rule_ids


def test_signed_non_blocking_mutation_is_approved() -> None:
    payload = {
        "intent": "rotate telemetry config",
        "actor": "operator",
        "signature": "signed",
        "failure_rate": 0.05,
    }
    response = client.post("/runtime/mutation/request", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "approved"
    assert body["signed"] is True
