from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_health_tls_reports_missing_by_default() -> None:
    client = TestClient(create_app())
    response = client.get("/health/tls")
    assert response.status_code == 200
    body = response.json()
    assert body["tls_enabled"] is False
    assert body["cert_path"] is None
    assert body["key_path"] is None
