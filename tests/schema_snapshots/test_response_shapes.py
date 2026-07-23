"""API contract / response shape snapshot tests."""

from __future__ import annotations

import datetime
from typing import Any, Dict, List

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


class TestSystemReadinessShape:
    """Core status endpoints share a readiness contract."""

    ENDPOINTS = [
        "/soh/status",
        "/sshh/status",
        "/readiness-gate/status",
    ]

    @pytest.mark.parametrize("path", ENDPOINTS)
    def test_readiness_fields_present(self, client: TestClient, path: str) -> None:
        response = client.get(path)
        assert response.status_code == 200
        body = response.json()
        assert "system_readiness" in body or "status" in body
        status_value = body.get("system_readiness") or body.get("status")
        assert status_value in {"GREEN", "YELLOW", "RED"}
        assert "healthy_count" in body
        assert "degraded_count" in body
        assert "unhealthy_count" in body
        assert "critical_unhealthy" in body
        assert isinstance(body["critical_unhealthy"], list)

    def test_sshh_includes_sac_ready(self, client: TestClient) -> None:
        body = client.get("/sshh/status").json()
        assert "sac_ready" in body
        assert isinstance(body["sac_ready"], bool)

    def test_readiness_gate_includes_chaos_telemetry(self, client: TestClient) -> None:
        body = client.get("/readiness-gate/status").json()
        assert "last_chaos" in body
        assert "chaos_count" in body
        assert isinstance(body["chaos_count"], int)


class TestSACStatusShape:
    def test_fields_present(self, client: TestClient) -> None:
        body = client.get("/sac/status").json()
        assert "quarantine" in body
        assert "rnr" in body
        assert "eig" in body
        assert "cma" in body
        assert "psa" in body
        assert "sas" in body
        assert "interventions" in body
        assert isinstance(body["interventions"], list)

    def test_sas_score_numeric(self, client: TestClient) -> None:
        body = client.get("/sac/status").json()
        assert isinstance(body["sas"]["score"], (int, float))


class TestEchoStatusShape:
    def test_fields_present(self, client: TestClient) -> None:
        body = client.get("/echo/status").json()
        assert body["status"] == "ok"
        assert "total_commands" in body
        assert "echoes_triggered" in body
        assert "echo_rate" in body
        assert isinstance(body["echo_rate"], (int, float))


class TestCloudAgentStatusShape:
    def test_fields_present(self, client: TestClient) -> None:
        body = client.get("/cloud-agent/status").json()
        assert "active" in body
        assert "history_count" in body
        assert isinstance(body["active"], bool)
        assert isinstance(body["history_count"], int)


class TestVoiceprintStatusShape:
    def test_baseline_contains_required_keys(self, client: TestClient) -> None:
        body = client.get("/cloud-agent/voiceprint/status").json()
        assert "baseline" in body
        baseline = body["baseline"]
        required = {
            "fatigue_baseline",
            "frustration_baseline",
            "urgency_baseline",
            "speech_rate",
            "pitch_variance",
            "pause_frequency",
            "calibration_count",
            "last_calibrated",
        }
        assert required.issubset(baseline.keys())

    def test_calibration_count_nonnegative(self, client: TestClient) -> None:
        body = client.get("/cloud-agent/voiceprint/status").json()
        assert body["baseline"]["calibration_count"] >= 0


class TestFirstContactShape:
    def test_start_requires_post(self, client: TestClient) -> None:
        response = client.get("/first-contact/start")
        assert response.status_code == 405

    def test_start_creates_session(self, client: TestClient) -> None:
        response = client.post("/first-contact/start", json={})
        assert response.status_code == 200
        body = response.json()
        assert "session_id" in body
        assert "current_step" in body


class TestEvolutionMemoryShape:
    def test_latest_is_array(self, client: TestClient) -> None:
        body = client.get("/evolution/memory/latest").json()
        assert "memories" in body
        assert isinstance(body["memories"], list)

    def test_memory_entry_fields(self, client: TestClient) -> None:
        body = client.get("/evolution/memory/latest").json()
        if not body["memories"]:
            pytest.skip("no memories recorded yet")
        entry = body["memories"][0]
        required = {
            "proposal_id",
            "title",
            "affected_modules",
            "rationale",
            "risk",
            "status",
            "created_at",
            "approval_status",
            "fingerprint",
            "target",
        }
        assert required.issubset(entry.keys())
        assert entry["risk"] in {"low", "medium", "high"}
        assert entry["status"] in {"success", "failure", "pending"}
