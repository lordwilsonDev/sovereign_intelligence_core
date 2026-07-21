"""Pipeline config endpoint tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app

client = TestClient(create_app())


def test_pipeline_get_config_returns_threshold() -> None:
    response = client.get("/pipeline/config")
    assert response.status_code == 200
    body = response.json()
    assert "threshold" in body
    assert "source" in body
    assert isinstance(body["threshold"], (int, float))


def test_pipeline_update_config_accepts_valid_threshold() -> None:
    response = client.patch("/pipeline/config", json={"threshold": 75.0})
    assert response.status_code == 200
    body = response.json()
    assert body["updated"] is True
    assert body["threshold"] == 75.0
    assert body["source"] == "env:MSB_PIPELINE_SAS_THRESHOLD"


def test_pipeline_update_config_rejects_out_of_range() -> None:
    response = client.patch("/pipeline/config", json={"threshold": 150.0})
    assert response.status_code == 200
    body = response.json()
    assert body["updated"] is False
    assert "reason" in body


def test_pipeline_assess_uses_updated_threshold(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MSB_PIPELINE_SAS_THRESHOLD", "90.0")
    response = client.post(
        "/pipeline/assess",
        json={"artifact_id": "schema-artifact", "sas": 91.0, "fts": 0.1, "rnr": 2.0, "sas_a": 91.0},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["verdict"] == "PASS"
    assert body["reason"] is None
