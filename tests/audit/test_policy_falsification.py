from __future__ import annotations

from pathlib import Path

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


def _seed_events(engine: AuditEngine):
    for _ in range(30):
        engine.record(AuditEvent(workflow="demo", event_type=EventType.TOOL_CALLED.value, status=Status.SUCCEEDED))
        engine.record(AuditEvent(workflow="demo", event_type=EventType.TIMEOUT.value, status=Status.SUCCEEDED))


def test_audit_policies_falsification_route_returns_schema(client):
    response = client.get("/audit/policies/falsification")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "records" in body
    assert "count" in body
    assert "falsified_count" in body

def test_policy_falsification_classifies_outcome(tmp_path: Path):
    store = AuditStore(root=str(tmp_path))
    engine = AuditEngine(store=store)

    first = engine.record_policy_falsification(
        policy="tool_timeout_rate",
        detected_rate=0.50,
        sample_count=50,
        blocked=True,
        checksum="abc123",
    )
    assert first["outcome"] == "pending"

    second = engine.record_policy_falsification(
        policy="tool_timeout_rate",
        detected_rate=0.20,
        sample_count=40,
        blocked=False,
        checksum="def456",
    )
    assert second["outcome"] == "pending"
    assert second["improvement"] == 0.30

    third = engine.record_policy_falsification(
        policy="tool_timeout_rate",
        detected_rate=0.80,
        sample_count=60,
        blocked=False,
        checksum="ghi789",
    )
    assert third["outcome"] == "falsified"
    assert third["improvement"] == -0.60
