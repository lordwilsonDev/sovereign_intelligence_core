"""CI webhook flow tests for sovereign pipeline assess."""

from __future__ import annotations

from typing import Any

import pytest

from msb_v2.api.web import create_app
from fastapi.testclient import TestClient


def _auth() -> dict[str, str]:
    return {"Authorization": "Bearer test"}


def test_ci_webhook_blocks_degraded_artifact() -> None:
    client = TestClient(create_app())
    payload = {
        "artifact_id": "ci-build-123",
        "sas": 55.0,
        "rnr": 0.55,
        "fts": 0.3,
        "sas_a": 55.0,
    }
    response = client.post("/pipeline/assess", json=payload, headers=_auth())
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "REJECT"
    assert data["audit_receipt"] is not None


def test_ci_webhook_approves_healthy_artifact() -> None:
    client = TestClient(create_app())
    payload = {
        "artifact_id": "ci-build-124",
        "sas": 96.0,
        "rnr": 0.96,
        "fts": 0.08,
        "sas_a": 96.0,
    }
    response = client.post("/pipeline/assess", json=payload, headers=_auth())
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "PASS"
    assert data["audit_receipt"] is not None


def test_ci_webhook_blocks_high_fts_artifact() -> None:
    client = TestClient(create_app())
    payload = {
        "artifact_id": "ci-build-125",
        "sas": 90.0,
        "rnr": 0.9,
        "fts": 0.7,
        "sas_a": 90.0,
    }
    response = client.post("/pipeline/assess", json=payload, headers=_auth())
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "REJECT"
