from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_dashboard_returns_html() -> None:
    client = TestClient(create_app())
    response = client.get("/observability/dashboard")
    assert response.status_code == 200
    assert "MSB Observability" in response.text


def test_fallback_under_missing_observability_metric() -> None:
    client = TestClient(create_app())
    response = client.get("/observability/metrics")
    assert response.status_code == 200
    body = response.json()
    assert "reasoning" in body
    assert "memory" in body
    # fallback returns buckets at minimum
    assert isinstance(body, dict)
