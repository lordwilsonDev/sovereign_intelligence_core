from __future__ import annotations

import json

import pytest

from msb_v2.audit.audit_engine import AuditEngine, AuditStore
from msb_v2.audit.events import AuditEvent, EventType, Status
from msb_v2.audit.replay import ReplayEngine


@pytest.fixture()
def store(tmp_path):
    engine = AuditEngine(store=AuditStore(root=str(tmp_path / "audit")))
    engine.clear()
    return engine


def test_replay_filter_by_workflow(store):
    store.record(AuditEvent(workflow="alpha", event_type=EventType.START, status=Status.SUCCEEDED))
    store.record(AuditEvent(workflow="beta", event_type=EventType.TOOL_CALLED, status=Status.SUCCEEDED))
    replay = ReplayEngine(store=store._store)
    alpha = replay.filter(workflow="alpha")
    assert len(alpha) == 1
    assert alpha[0]["workflow"] == "alpha"


def test_replay_validate_loaded(store):
    store.record(AuditEvent(workflow="alpha", event_type=EventType.START, status=Status.SUCCEEDED))
    replay = ReplayEngine(store=store._store)
    events = replay.load_events()
    loaded = replay.validate_loaded(events)
    assert len(loaded) == 1
    assert loaded[0].workflow == "alpha"


def test_replay_rejects_invalid_events(store):
    store._store.append({"event_type": "START", "workflow": "malformed", "duration_ms": "not-a-number"})
    replay = ReplayEngine(store=store._store)
    with pytest.raises(ValueError, match="Replay validation failed"):
        replay.validate_loaded(replay.load_events())
