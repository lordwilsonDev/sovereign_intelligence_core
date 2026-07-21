"""Pipeline assess API endpoint tests."""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_pipeline_assess_endpoint() -> None:
    client = TestClient(create_app())
    payload = {
        "artifact_id": "img:latest",
        "sas": 95.0,
        "rnr": 0.95,
        "fts": 0.1,
        "sas_a": 95.0,
    }
    response = client.post("/pipeline/assess", json=payload, headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "PASS"
    assert data["artifact_id"] == "img:latest"
    assert "audit_receipt" in data


def test_pipeline_assess_rejects_degraded() -> None:
    client = TestClient(create_app())
    payload = {
        "artifact_id": "bad:latest",
        "sas": 60.0,
        "rnr": 0.6,
        "fts": 0.2,
        "sas_a": 60.0,
    }
    response = client.post("/pipeline/assess", json=payload, headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "REJECT"
    assert data["reason"] is not None


def test_pipeline_metrics_exposed() -> None:
    client = TestClient(create_app())
    response = client.get("/metrics")
    assert response.status_code == 200
    text = response.text
    for name in ["msb_pipeline_sas_average", "msb_pipeline_fts_average", "msb_pipeline_decisions_total"]:
        assert name in text, f"missing_metric:{name}"
