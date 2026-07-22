from __future__ import annotations

from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_voiceprint_baseline_returns_defaults(client: TestClient) -> None:
    response = client.get("/cloud-agent/voiceprint/baseline")
    assert response.status_code == 200
    body = response.json()
    for key in ["fatigue_baseline", "frustration_baseline", "urgency_baseline", "speech_rate", "pitch_variance", "pause_frequency"]:
        assert key in body


def test_voiceprint_calibrate_updates_baseline(client: TestClient) -> None:
    response = client.post(
        "/cloud-agent/voiceprint/calibrate",
        json={
            "samples": [
                {"fatigue_baseline": 0.3, "frustration_baseline": 0.2, "urgency_baseline": 0.15, "speech_rate": 0.9, "pitch_variance": 1.1, "pause_frequency": 0.2}
            ]
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "calibrated"
    assert body["baseline"]["fatigue_baseline"] == pytest.approx(0.3)
    assert body["baseline"]["frustration_baseline"] == pytest.approx(0.2)


def test_voiceprint_reset_restores_defaults(client: TestClient) -> None:
    client.post(
        "/cloud-agent/voiceprint/calibrate",
        json={
            "samples": [
                {"fatigue_baseline": 0.5, "frustration_baseline": 0.5, "urgency_baseline": 0.5, "speech_rate": 2.0, "pitch_variance": 2.0, "pause_frequency": 0.5}
            ]
        },
    )
    response = client.post("/cloud-agent/voiceprint/reset")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "reset"
    assert body["baseline"]["fatigue_baseline"] == pytest.approx(0.2)
    assert body["baseline"]["frustration_baseline"] == pytest.approx(0.1)


def test_voiceprint_calibrate_rejects_non_list_payload(client: TestClient) -> None:
    response = client.post("/cloud-agent/voiceprint/calibrate", json={"samples": "not-a-list"})
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "calibrated"
    assert body["baseline"]["fatigue_baseline"] == pytest.approx(0.2)
