from __future__ import annotations

import time

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.auto_healing import AutoHealingPolicyEngine
from msb_v2.audit.events import AuditEvent, EventType, Status
from msb_v2.audit.storage import AuditStore


@pytest.fixture()
def client():
    set_local_bypass(True)
    client = TestClient(create_app())
    yield client
    set_local_bypass(None)


def _engine(tmp_path):
    store = AuditStore(root=str(tmp_path))
    return AuditEngine(store=store)


def test_auto_healing_noop_below_threshold(tmp_path):
    engine = _engine(tmp_path)
    engine.record(AuditEvent(workflow="w", event_type=EventType.TOOL_CALLED, status=Status.SUCCEEDED))
    engine.record(AuditEvent(workflow="w", event_type=EventType.TOOL_COMPLETED, status=Status.SUCCEEDED))
    actions = AutoHealingPolicyEngine(audit=engine).evaluate()
    assert actions == []


def test_auto_healing_detects_timeout_violation(tmp_path):
    engine = _engine(tmp_path)
    for _ in range(20):
        engine.record(AuditEvent(workflow="w", event_type=EventType.TOOL_CALLED, status=Status.SUCCEEDED))
    for _ in range(20):
        engine.record(AuditEvent(workflow="w", event_type=EventType.TIMEOUT, status=Status.FAILED))
    actions = AutoHealingPolicyEngine(audit=engine).evaluate()
    assert len(actions) == 1
    assert actions[0]["policy"] == "tool_timeout_rate"
    assert actions[0]["detected_rate"] == pytest.approx(20 / 40)


def test_auto_healing_detects_retry_violation(tmp_path):
    engine = _engine(tmp_path)
    for _ in range(20):
        engine.record(AuditEvent(workflow="w", event_type=EventType.TOOL_CALLED, status=Status.SUCCEEDED))
    for _ in range(20):
        engine.record(AuditEvent(workflow="w", event_type=EventType.RETRY, status=Status.RUNNING))
    actions = AutoHealingPolicyEngine(audit=engine).evaluate()
    assert len(actions) == 1
    assert actions[0]["policy"] == "retry_rate"


def test_auto_healing_detects_cache_miss_violation(tmp_path):
    engine = _engine(tmp_path)
    for _ in range(40):
        engine.record(AuditEvent(workflow="w", event_type=EventType.CACHE_MISS, status=Status.SUCCEEDED))
    for _ in range(60):
        engine.record(AuditEvent(workflow="w", event_type=EventType.CACHE_HIT, status=Status.SUCCEEDED))
    actions = AutoHealingPolicyEngine(audit=engine).evaluate()
    assert len(actions) == 1
    assert actions[0]["policy"] == "cache_miss_rate"
    assert actions[0]["detected_rate"] == pytest.approx(40 / 100)


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
