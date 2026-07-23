"""Tests for SAC attestation endpoint and ReadinessGate integration."""

from __future__ import annotations

from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from msb_v2.api.web import create_app
from msb_v2.core.sac_gate import ReadinessGate


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_sac_attest_verify_endpoint(client: TestClient) -> None:
    response = client.post("/sac/attest", json={})
    assert response.status_code == 200
    body = response.json()
    assert "verdict" in body


def test_sac_attest_trust_endpoint(client: TestClient) -> None:
    with patch("msb_v2.verification.hardware_attestation.subprocess.run") as mock_run:
        mock_run.return_value = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        response = client.post("/sac/attest", json={"action": "trust"})
        assert response.status_code == 200
        body = response.json()
        assert body["verdict"] == "TRUST_ESTABLISHED"


def test_readiness_gate_attestation_verdict() -> None:
    gate = ReadinessGate()
    with patch("msb_v2.verification.hardware_attestation.subprocess.run") as mock_run:
        mock_run.return_value = type("R", (), {"returncode": 0, "stdout": "deadbeef\n"})()
        verdict = gate.attestation_verdict()
        assert verdict["verdict"] in {"OK", "TAMPERED", "TRUST_NOT_ESTABLISHED"}


def test_readiness_gate_blocks_on_tamper() -> None:
    gate = ReadinessGate()
    with patch("msb_v2.verification.hardware_attestation.subprocess.run") as mock_run:
        mock_run.return_value = type("R", (), {"returncode": 0, "stdout": "abc123\n"})()
        assert gate.is_ready() is False


def test_readiness_gate_ready_when_ok() -> None:
    gate = ReadinessGate()
    original_verdict = gate.attestation_verdict
    try:
        gate.attestation_verdict = lambda: {"verdict": "OK"}
        assert gate.is_ready() is True
    finally:
        gate.attestation_verdict = original_verdict
