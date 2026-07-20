from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.events import AuditEvent, EventType, Status


@pytest.fixture()
def app():
    set_local_bypass(True)
    client = TestClient(create_app())
    yield client
    set_local_bypass(None)


def test_audit_recent_route_exists(app):
    response = app.get("/audit/recent")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_audit_recent_accepts_limit_param(app):
    response = app.get("/audit/recent?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
