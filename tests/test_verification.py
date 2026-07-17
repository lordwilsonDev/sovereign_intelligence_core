from __future__ import annotations


from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.reasoning.integrity import EventStreamStore, ExecutionEvent, EventKind
from msb_v2.verification.integrity_verifier import IntegrityVerifier


def _make_stream() -> EventStreamStore:
    stream = EventStreamStore()
    stream.append(ExecutionEvent(event_id="e1", sequence=1, kind=EventKind.TOOL, source="unit", payload={"verdict": "accepted"}, decision_id="d1", previous_hash="abc"))
    stream.append(ExecutionEvent(event_id="e2", sequence=2, kind=EventKind.TOOL, source="unit", payload={"verdict": "accepted"}, decision_id="d1"))
    return stream


def test_integrity_verifier_marks_valid_trace_continuous() -> None:
    stream = _make_stream()
    verifier = IntegrityVerifier(stream=stream)
    trace_check = verifier.verify_trace("missing")
    assert trace_check["continuous"] is True
    assert trace_check["count"] == 0

    decision_check = verifier.verify_decision("d1")
    assert decision_check.valid is True
    assert decision_check.continuity["continuous"] is True


def test_integrity_verifier_detects_broken_hash() -> None:
    stream = EventStreamStore()
    stream.append(
        ExecutionEvent(event_id="e1", sequence=1, kind=EventKind.TOOL, source="unit", payload={}, decision_id="d2")
    )
    stream.append(
        ExecutionEvent(event_id="e2", sequence=2, kind=EventKind.TOOL, source="unit", payload={}, decision_id="d2", previous_hash=stream._events[0].integrity_hash)
    )
    e1 = stream._events[0]
    broken = ExecutionEvent(
        event_id=e1.event_id,
        sequence=e1.sequence,
        kind=e1.kind,
        source=e1.source,
        payload=e1.payload,
        trace_id=e1.trace_id,
        decision_id=e1.decision_id,
        ts=e1.ts,
        previous_hash=e1.previous_hash,
        integrity_hash="bogus",
    )
    stream._events[0] = broken
    check = IntegrityVerifier(stream=stream).verify_decision("d2")
    assert check.expected_hash == "bogus"
    assert check.actual_hash != "bogus"
    assert check.valid is False


def test_verification_api_endpoints_exist() -> None:
    client = TestClient(create_app())
    response = client.get("/verification/integrity/trace/missing")
    assert response.status_code == 200
    body = response.json()
    assert body["trace_id"] == "missing"

    response = client.get("/verification/integrity/decision/missing")
    assert response.status_code == 200
    body = response.json()
    assert "valid" in body

    response = client.post("/verification/integrity/batch", json={"decision_ids": ["a", "b"]})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
