from __future__ import annotations

from pathlib import Path

import pytest
from msb_v2.audit.auto_healing import AutoHealingPolicyEngine
from msb_v2.audit.events import AuditEvent, EventType, Status


def _make_timeout_events(n: int, *, event_type: str = EventType.TIMEOUT.value) -> list[AuditEvent]:
    events = []
    for _ in range(n):
        events.append(AuditEvent(workflow="demo", event_type=event_type, status=Status.SUCCEEDED))
        events.append(AuditEvent(workflow="demo", event_type=EventType.TOOL_CALLED.value, status=Status.SUCCEEDED))
    return events


class FakeEngine:
    def __init__(self, events):
        self._events = events

    def events(self):
        return [e.to_dict() for e in self._events]

    def record(self, event):
        self._events.append(event)

    def record_policy_falsification(self, *, policy, detected_rate, sample_count, blocked, checksum):
        return {
            "policy": policy,
            "detected_rate": detected_rate,
            "sample_count": sample_count,
            "blocked": blocked,
            "checksum": checksum,
            "improvement": 0.0,
            "outcome": "pending",
        }


def test_auto_healing_veto_blocks_high_risk_action():
    engine = AutoHealingPolicyEngine()
    events = []
    for _ in range(30):
        events.append(AuditEvent(workflow="demo", event_type=EventType.TOOL_CALLED.value, status=Status.SUCCEEDED))
        events.append(AuditEvent(workflow="demo", event_type=EventType.TIMEOUT.value, status=Status.SUCCEEDED))
    fake = FakeEngine(events)
    engine._audit = fake
    actions = engine.evaluate()
    assert len(actions) == 1


def test_auto_healing_no_actions_when_below_threshold():
    engine = AutoHealingPolicyEngine()
    events = [
        AuditEvent(workflow="demo", event_type=EventType.TOOL_CALLED.value, status=Status.SUCCEEDED),
        AuditEvent(workflow="demo", event_type=EventType.TOOL_COMPLETED.value, status=Status.SUCCEEDED),
    ]
    fake = FakeEngine(events)
    engine._audit = fake
    actions = engine.evaluate()
    assert actions == []
