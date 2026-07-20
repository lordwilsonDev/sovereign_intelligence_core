from __future__ import annotations

import json
from pathlib import Path

from msb_v2.audit.audit_engine import AuditEngine, AuditStore
from msb_v2.audit.events import AuditEvent, EventType, Status
from msb_v2.audit.hooks import build_audit_hook
from msb_v2.audit.replay import ReplayEngine
from msb_v2.engine.orchestrator import Task, orchestrate


def test_orchestrate_audit_hook_writes_events(tmp_path):
    store = AuditStore(root=str(tmp_path / "audit"))
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
