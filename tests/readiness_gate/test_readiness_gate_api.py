"""Tests for readiness gate API and telemetry validation."""

from __future__ import annotations

from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_readiness_gate_status_returns_snapshot(client: TestClient) -> None:
    response = client.get("/readiness-gate/status")
    assert response.status_code == 200
    body = response.json()
    assert "status" in body
    assert "chaos_count" in body


def test_chaos_injection_updates_readiness(client: TestClient) -> None:
    response = client.post("/readiness-gate/chaos/inject", params={"scenario": "spike_cpu"})
    assert response.status_code == 200
    body = response.json()
    assert body["scenario"] == "spike_cpu"
    assert body["result"]["readiness"] in {"YELLOW", "RED"}
    assert body["result"]["telemetry"]["emitted"] is True
    assert len(body["result"]["affected"]) >= 1


def test_telemetry_emits_on_chaos(client: TestClient) -> None:
    response = client.post("/readiness-gate/chaos/inject", params={"scenario": "kill_harness"})
    assert response.status_code == 200
    body = response.json()
    assert body["result"]["telemetry"]["emitted"] is True


def test_failover_trigger_returns_status(client: TestClient) -> None:
    response = client.post("/readiness-gate/failover/trigger", params={"target": "db"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"success", "degraded"}
    assert "fallback" in body
