from __future__ import annotations

import time

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.events import AuditEvent, EventType, Status
from msb_v2.audit.telemetry import AuditTelemetry


@pytest.fixture()
def client():
    set_local_bypass(True)
    client = TestClient(create_app())
    yield client
    set_local_bypass(None)


def test_metrics_endpoint_serves_prometheus_content(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "msb_audit_" in response.text


def test_audit_recent_route_exists(client):
    response = client.get("/audit/recent")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)


def test_audit_telemetry_maybe_resync_triggers_on_new_events(monkeypatch):
    engine = AuditEngine()
    telemetry = AuditTelemetry(audit=engine)
    calls = []

    monkeypatch.setattr(telemetry, "_resync_events", lambda: calls.append(True))
    engine.record(AuditEvent(workflow="wf", event_type=EventType.START, status=Status.SUCCEEDED))
    telemetry.maybe_resync()
    assert calls == [True]


def test_audit_telemetry_maybe_resync_skips_unchanged_count(monkeypatch):
    engine = AuditEngine()
    telemetry = AuditTelemetry(audit=engine)
    calls = []

    monkeypatch.setattr(telemetry, "_resync_events", lambda: calls.append(True))
    telemetry.maybe_resync()
    assert calls == []
