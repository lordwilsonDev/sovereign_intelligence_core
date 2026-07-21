from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass
from msb_v2.audit.sovereign.metrics import compute_audit_sovereignty_score

pytestmark = pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledCoroutineWarning")


@pytest.fixture(autouse=True)
def _disable_auth_for_test(monkeypatch, tmp_path):
    monkeypatch.setenv("MSB_LOCAL_AUTH_OVERRIDE", "1")
    set_local_bypass(True)
    monkeypatch.setenv("MSB_AUDIT_ROOT", str(tmp_path))
    yield


def test_ass_metric_formula():
    assert compute_audit_sovereignty_score(merkle_ok=True, fts=0.0, assumption_debt=0, veto_active=True) == 100.0
    assert compute_audit_sovereignty_score(merkle_ok=False, fts=0.0, assumption_debt=0, veto_active=True) == 60.0
    assert compute_audit_sovereignty_score(merkle_ok=True, fts=0.8, assumption_debt=5, veto_active=False) == 50.0
    assert compute_audit_sovereignty_score(merkle_ok=False, fts=0.9, assumption_debt=10, veto_active=False) == 10.0
    assert compute_audit_sovereignty_score(merkle_ok=True, fts=1.0, assumption_debt=0, veto_active=True) == 80.0


def test_audit_verify_endpoint():
    app = create_app()
    with TestClient(app) as client:
        response = client.get("/audit/verify")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["verified"], bool)
        assert "log" in data


def test_audit_sovereignty_endpoint():
    app = create_app()
    with TestClient(app) as client:
        response = client.get("/audit/sovereignty")
        assert response.status_code == 200
        data = response.json()
        assert data["audit_sovereignty_score"] >= 0
        assert "blocked_actions" in data
        assert "merkle_ok" in data
        assert "fts" in data
        assert "assumption_debt" in data
        assert "falsified_count" in data
        assert isinstance(data["fts"], (int, float))
        assert isinstance(data["assumption_debt"], int)
