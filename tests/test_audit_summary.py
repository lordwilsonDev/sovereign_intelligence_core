from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.auto_healing import AutoHealingPolicyEngine
from msb_v2.audit.business_metrics import BusinessMetrics
from msb_v2.audit.events import AuditEvent, EventType, Status
from msb_v2.audit.storage import AuditStore


@pytest.fixture()
def client():
    set_local_bypass(True)
    client = TestClient(create_app())
    yield client
    set_local_bypass(None)


def test_audit_recent_returns_events(client):
    response = client.get("/audit/recent")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)


def test_audit_summary_route_exists(client):
    response = client.get("/audit/summary")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "summary" in body
    assert "business_impact" in body


def test_audit_summary_accepts_limit(client):
    response = client.get("/audit/summary?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_audit_policies_route_exists(client):
    response = client.get("/audit/policies")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "actions" in body
    assert "count" in body


def test_audit_policies_returns_schema(client):
    response = client.get("/audit/policies")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "actions" in body
    assert "count" in body
    assert isinstance(body["actions"], list)
    assert isinstance(body["count"], int)


def test_business_metrics_snapshot_structure(tmp_path):
    store = AuditStore(root=str(tmp_path))
    engine = AuditEngine(store=store)
    engine.record(AuditEvent(workflow="w1", event_type=EventType.START, status=Status.SUCCEEDED, duration_ms=10, agent="agent-a"))
    engine.record(AuditEvent(workflow="w1", event_type=EventType.WORKFLOW_COMPLETE, status=Status.SUCCEEDED, duration_ms=100, agent="agent-a"))
    engine.record(AuditEvent(workflow="w2", event_type=EventType.WORKFLOW_FAILED, status=Status.FAILED, duration_ms=50, agent="agent-b"))

    snapshot = BusinessMetrics(audit=engine).snapshot()
    assert snapshot["summary"]["total_workflows"] == 2
    assert snapshot["summary"]["success_rate"] == 0.5
    assert snapshot["business_impact"]["hours_saved"] >= 0
    assert isinstance(snapshot["recommendations"], list)
    immutable = snapshot["immutable_record"]
    assert isinstance(immutable, dict)
    assert "root_hash" in immutable
    assert "total_blocks" in immutable
    assert isinstance(immutable["root_hash"], str)
    assert isinstance(immutable["total_blocks"], int)
    assert immutable["total_blocks"] == 3


def test_auto_healing_emits_self_correction_event(tmp_path):
    store = AuditStore(root=str(tmp_path))
    engine = AuditEngine(store=store)
    for _ in range(20):
        engine.record(AuditEvent(workflow="w", event_type=EventType.TOOL_CALLED, status=Status.SUCCEEDED))
    for _ in range(20):
        engine.record(AuditEvent(workflow="w", event_type=EventType.TIMEOUT, status=Status.FAILED))
    AutoHealingPolicyEngine(audit=engine).evaluate()
    events = engine.events()
    self_corrections = [event for event in events if event.get("event_type") == EventType.SELF_CORRECTION.value]
    assert len(self_corrections) == 1
    assert self_corrections[0]["metadata"]["policy"] == "tool_timeout_rate"