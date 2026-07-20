from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.auto_healing import AutoHealingPolicyEngine
from msb_v2.audit.events import AuditEvent, EventType, Status
from msb_v2.audit.schemas import apply_event_hashes, chain_hash
from msb_v2.audit.storage import AuditStore


@pytest.fixture()
def client():
    set_local_bypass(True)
    client = TestClient(create_app())
    yield client
    set_local_bypass(None)


def test_chain_hash_deterministic_sorted():
    event = {"event_type": "START", "workflow": "w", "status": "succeeded", "timestamp": "2026-07-20T18:00:00+00:00"}
    first = chain_hash("0" * 40, event)
    second = chain_hash("0" * 40, event)
    assert first == second
    assert len(first) == 40


def test_chain_hash_changes_with_event():
    event = {"event_type": "START", "workflow": "w", "status": "succeeded", "timestamp": "2026-07-20T18:00:00+00:00"}
    root = "0" * 40
    first = chain_hash(root, event)
    changed = dict(event, status="failed")
    second = chain_hash(root, changed)
    assert first != second


def test_apply_event_hashes_shape_and_chain():
    events = [
        {"event_type": "START", "workflow": "w", "status": "succeeded", "timestamp": "2026-07-20T18:00:00+00:00"},
        {"event_type": "WORKFLOW_COMPLETE", "workflow": "w", "status": "succeeded", "timestamp": "2026-07-20T18:01:00+00:00"},
    ]
    hashed = apply_event_hashes(events)
    assert len(hashed) == 2
    for event in hashed:
        assert "event_hash" in event
        assert "chain_hash" in event
        assert len(event["event_hash"]) == 40
        assert len(event["chain_hash"]) == 40
    assert hashed[1]["chain_hash"] != hashed[0]["chain_hash"]


def test_business_metrics_immutable_record_has_chain_root(tmp_path):
    store = AuditStore(root=str(tmp_path))
    engine = AuditEngine(store=store)
    engine.record(AuditEvent(workflow="w1", event_type=EventType.START, status=Status.SUCCEEDED))
    engine.record(AuditEvent(workflow="w1", event_type=EventType.WORKFLOW_COMPLETE, status=Status.SUCCEEDED))
    from msb_v2.audit.business_metrics import BusinessMetrics
    snapshot = BusinessMetrics(audit=engine).snapshot()
    immutable = snapshot["immutable_record"]
    assert immutable["total_blocks"] == 2
    assert isinstance(immutable["root_hash"], str)
    assert immutable["root_hash"] != "0" * 40


def test_audit_summary_sections_present(client):
    response = client.get("/audit/summary")
    assert response.status_code == 200
    body = response.json()
    assert "workflow_integrity" in body
    assert "decision_record" in body
    assert "error_recovery" in body
    assert "business_impact" in body
    assert "immutable_record" in body
