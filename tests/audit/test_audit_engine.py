from __future__ import annotations

import json

import pytest

from msb_v2.audit.audit_engine import AuditEngine, AuditStore
from msb_v2.audit.events import AuditEvent, EventType, Status
from msb_v2.audit.metrics import MetricsEngine
from msb_v2.audit.schemas import build_input_hash, build_output_hash, stable_workflow
from msb_v2.audit.validator import AuditValidator


@pytest.fixture()
def store(tmp_path):
    engine = AuditEngine(store=AuditStore(root=str(tmp_path / "audit")))
    engine.clear()
    return engine


def test_audit_event_roundtrip(store):
    event = AuditEvent(workflow="demo", event_type=EventType.START, status=Status.RUNNING)
    stored = store.record(event)
    assert stored.trace_id == event.trace_id
    events = store.events()
    assert len(events) == 1
    loaded = AuditEvent.from_dict(events[0])
    assert loaded.workflow == "demo"
    assert loaded.event_type == EventType.START
    assert loaded.status == Status.RUNNING
    assert loaded.timestamp


def test_validator_rejects_invalid_event_type():
    validator = AuditValidator()
    bad = AuditEvent(event_type="INVALID")
    assert validator.is_valid(bad) is False
    with pytest.raises(ValueError):
        validator.validate(bad)


def test_metrics_summary_counts_by_workflow(store):
    for idx in range(5):
        store.record(AuditEvent(workflow="alpha", event_type=EventType.TOOL_CALLED, status=Status.SUCCEEDED))
        if idx < 2:
            store.record(AuditEvent(workflow="beta", event_type=EventType.WORKFLOW_FAILED, status=Status.FAILED))
    metrics = MetricsEngine(audit=store)
    summary = metrics.snapshot()
    alpha = summary["workflows"]["alpha"]
    assert alpha["total"] == 5
    assert alpha["succeeded"] == 5
    assert alpha["success_rate"] == 1.0
    beta = summary["workflows"]["beta"]
    assert beta["failed"] == 2
    assert beta["success_rate"] == 0.0


def test_schemas_stable_workflow_and_hashes():
    assert stable_workflow("Demo Workflow") == "demo-workflow"
    assert build_input_hash("demo", {"q": "trace"}) == build_input_hash("demo", {"q": "trace"})
    assert build_input_hash("demo", {"q": "trace"}) != build_input_hash("demo", {"q": "other"})
    assert build_output_hash(1) != build_output_hash(2)


def test_audit_store_clear(store):
    store.record(AuditEvent(workflow="x", event_type=EventType.START, status=Status.SUCCEEDED))
    assert store.events()
    store.clear()
    assert store.events() == []
