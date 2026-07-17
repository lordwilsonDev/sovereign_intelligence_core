from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import app
from msb_v2.reasoning.store import ReasoningStore, SEED
from msb_v2.reasoning.types import JustificationKind, ReasoningStatus, ReasoningStep

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_reasoning_store():
    import msb_v2.api.reasoning as reasoning_mod
    reasoning_mod.store = ReasoningStore(SEED)


def _step(claim, confidence=1.0):
    return ReasoningStep(
        step_index=0,
        claim=claim,
        evidence_refs=(),
        assumptions=(),
        confidence=confidence,
        metadata={"kind": JustificationKind.STRATEGIC},
    ).__dict__


def _payload(status=ReasoningStatus.COMPLETED):
    return {
        "trace_id": "rtrace-0001",
        "title": "why route?",
        "status": status.value,
        "steps": [_step("memory is durable"), _step("speed is secondary")],
        "decision_id": "dec-1001",
        "memory_ids": ["mem-11", "mem-12"],
        "conclusion": "use durable memory",
        "metadata": {"actor": "planner"},
    }


def test_create_read_list_filter():
    body = _payload()
    r = client.post("/reasoning/traces", json=body)
    assert r.status_code == 200
    assert r.json()["trace_id"] == "rtrace-0001"

    r = client.get("/reasoning/traces")
    assert r.status_code == 200
    assert any((i["trace_id"] == "rtrace-0001") for i in r.json())

    r = client.get("/reasoning/traces/rtrace-0001")
    assert r.status_code == 200
    assert r.json()["decision_id"] == "dec-1001"

    r = client.get("/reasoning/traces?status=completed")
    assert r.status_code == 200
    assert any((i["trace_id"] == "rtrace-0001") for i in r.json())


def test_status_transition():
    r = client.post("/reasoning/traces", json=_payload(ReasoningStatus.ACTIVE))
    assert r.status_code == 200
    tid = r.json()["trace_id"]

    r = client.patch(f"/reasoning/traces/{tid}/status", json={"status": ReasoningStatus.COMPLETED.value})
    assert r.status_code == 200
    assert r.json()["status"] == ReasoningStatus.COMPLETED.value
    before = r.json()["updated_at"]

    r = client.patch(f"/reasoning/traces/{tid}/status", json={"status": ReasoningStatus.ABANDONED.value})
    assert r.json()["updated_at"] != before


def test_backfill_decision_cross_ref():
    body = _payload()
    body["trace_id"] = "rtrace-0002"
    body["decision_id"] = None
    r = client.post("/reasoning/traces", json=body)
    assert r.status_code == 200
    tid = r.json()["trace_id"]

    r = client.post(f"/reasoning/traces/{tid}/decision", json="dec-9001")
    assert r.status_code == 200
    assert r.json()["decision_id"] == "dec-9001"

    r = client.get("/reasoning/refs/dec-9001")
    assert r.status_code == 200
    refs = r.json()
    assert refs
    assert refs[0]["trace_id"] == tid


def test_missing_ids():
    r = client.get("/reasoning/traces/missing-id")
    assert r.status_code == 404

    r = client.get("/reasoning/refs/missing")
    assert r.status_code == 200
    assert r.json() == []


def test_empty_steps_rejected():
    payload = _payload()
    payload["steps"] = []
    assert client.post("/reasoning/traces", json=payload).status_code == 400


def test_duplicate_trace_rejected():
    tid = "rtrace-0099"
    payload = _payload(ReasoningStatus.DRAFT)
    payload["trace_id"] = tid
    assert client.post("/reasoning/traces", json=payload).status_code == 200
    assert client.post("/reasoning/traces", json=payload).status_code == 409
