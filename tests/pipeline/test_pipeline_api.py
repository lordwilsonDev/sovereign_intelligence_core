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


SOVEREIGN_METRIC_NAMES = [
    "msb_audit_sovereign_fts",
    "msb_audit_sovereign_assumption_debt",
    "msb_audit_sovereign_score",
    "msb_pipeline_sas_average",
    "msb_pipeline_fts_average",
    "msb_pipeline_decisions_total",
    "msb_kb4_cycles_total",
    "msb_kb4_mutations_total",
    "msb_kb4_vetoes_total",
    "msb_provider_sovereignty_score",
    "msb_provider_vetoes_total",
    "msb_provider_coherence_avg",
    "msb_provider_trust_status",
    "msb_provider_ouroboros_events_total",
]


# NOTE: These test families are gated by live /metrics evidence captured in
# TestClient-backed tests through the app factory. Keep them grouped so missing
# gauges stay isolated to their subsystem.
_PIPELINE_METRICS = [
    "msb_pipeline_sas_average",
    "msb_pipeline_fts_average",
    "msb_pipeline_decisions_total",
]
_PROVIDER_METRICS = [
    "msb_provider_sovereignty_score",
    "msb_provider_vetoes_total",
    "msb_provider_trust_status",
]
_KB4_METRICS = [
    "msb_kb4_cycles_total",
    "msb_kb4_mutations_total",
    "msb_kb4_vetoes_total",
]


def _client() -> TestClient:
    return TestClient(create_app())


def test_pipeline_metrics_exposed() -> None:
    response = _client().get("/metrics")
    assert response.status_code == 200
    text = response.text
    for name in _PIPELINE_METRICS:
        assert name in text, f"missing_metric:{name}"


def test_provider_metrics_exposed() -> None:
    response = _client().get("/metrics")
    assert response.status_code == 200
    text = response.text
    for name in _PROVIDER_METRICS:
        assert name in text, f"missing_metric:{name}"


def test_pipeline_metrics_move_after_assess() -> None:
    client = _client()
    before = client.get("/metrics").text
    payload = {
        "artifact_id": "metrics-movement",
        "sas": 91.0,
        "rnr": 0.9,
        "fts": 0.12,
        "sas_a": 91.0,
    }
    response = client.post("/pipeline/assess", json=payload, headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    after = client.get("/metrics").text
    assert 'msb_pipeline_sas_average{stage="gate"} 91.0' in after
    assert 'msb_pipeline_fts_average{stage="gate"} 0.12' in after
    assert before != after


def test_kb4_metrics_exposed() -> None:
    response = _client().get("/metrics")
    assert response.status_code == 200
    text = response.text
    for name in _KB4_METRICS:
        assert name in text, f"missing_metric:{name}"
