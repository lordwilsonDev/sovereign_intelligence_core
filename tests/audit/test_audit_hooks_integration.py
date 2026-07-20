from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.events import AuditEvent, EventType, Status
from msb_v2.audit.hooks import build_audit_hook
from msb_v2.audit.replay import ReplayEngine
from msb_v2.audit.storage import AuditStore
from msb_v2.audit.telemetry import AuditTelemetry
from msb_v2.engine.orchestrator import Task, orchestrate


@pytest.fixture()
def app():
    set_local_bypass(True)
    client = TestClient(create_app())
    yield client
    set_local_bypass(None)


def test_audit_recent_returns_events(app):
    response = app.get("/audit/recent")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_audit_recent_accepts_limit_param(app):
    response = app.get("/audit/recent?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_telemetry_maybe_resync_avoids_unchanged_count(monkeypatch):
    engine = AuditEngine()
    engine.record(AuditEvent(workflow="wf", event_type=EventType.START, status=Status.SUCCEEDED))
    telemetry = AuditTelemetry(audit=engine)
    calls = []

    def fake_resync() -> None:
        calls.append(True)

    monkeypatch.setattr(telemetry, "_resync_events", fake_resync)
    telemetry.maybe_resync()
    assert calls == []
    telemetry.maybe_resync(force=True)
    assert calls == [True]


def test_telemetry_maybe_resync_triggers_on_new_events(monkeypatch):
    engine = AuditEngine()
    engine.record(AuditEvent(workflow="wf", event_type=EventType.START, status=Status.SUCCEEDED))
    telemetry = AuditTelemetry(audit=engine)
    calls = []

    def fake_resync() -> None:
        calls.append(True)

    monkeypatch.setattr(telemetry, "_resync_events", fake_resync)
    engine.record(AuditEvent(workflow="wf", event_type=EventType.TOOL_CALLED, status=Status.RUNNING))
    telemetry.maybe_resync()
    assert calls == [True]


def test_orchestrate_audit_hook_writes_events(tmp_path):
    store_path = tmp_path / "audit"
    store_path.mkdir(parents=True, exist_ok=True)
    store = AuditStore(root=str(store_path))
    engine = AuditEngine(store=store)
    engine.clear()
    hook = build_audit_hook(engine, workflow="orchestrate", agent="test")
    tasks = [
        Task(id="a", action=lambda: "done-a"),
        Task(id="b", dependencies=["a"], action=lambda: "done-b"),
    ]
    results = orchestrate(tasks, hook=hook)
    assert [task.status for task in results] == ["succeeded", "succeeded"]
    events = engine.events()
    assert len(events) == 4
    replay = ReplayEngine(store=store)
    filtered = replay.filter(workflow="orchestrate-dispatch")
    assert len(filtered) == 2
    validated = replay.validate_loaded(events)
    assert all(isinstance(event, AuditEvent) for event in validated)
