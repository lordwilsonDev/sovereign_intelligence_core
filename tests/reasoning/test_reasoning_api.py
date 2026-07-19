from __future__ import annotations

import contextlib

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.main import app
from msb_v2.api.middleware import set_local_bypass as _set_local_bypass
from msb_v2.reasoning.store import ReasoningStore, SEED
from msb_v2.reasoning.types import JustificationKind, ReasoningStatus, ReasoningStep

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_reasoning_store():
    import msb_v2.api.reasoning as reasoning_mod
    reasoning_mod.store = ReasoningStore(SEED)


@contextlib.contextmanager
def _bypass():
    _set_local_bypass(True)
    try:
        yield
    finally:
        _set_local_bypass(None)


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
    with _bypass():
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
    with _bypass():
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
    with _bypass():
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
    with _bypass():
        payload = _payload()
        payload["steps"] = []
        assert client.post("/reasoning/traces", json=payload).status_code == 400


def test_duplicate_trace_rejected():
    with _bypass():
        tid = "rtrace-0099"
        payload = _payload(ReasoningStatus.DRAFT)
        payload["trace_id"] = tid
        assert client.post("/reasoning/traces", json=payload).status_code == 200
        assert client.post("/reasoning/traces", json=payload).status_code == 409


def test_list_traces_pagination() -> None:
    with _bypass():
        for idx in range(5):
            payload = _payload(ReasoningStatus.DRAFT)
            payload["trace_id"] = f"rtrace-p{idx}"
            assert client.post("/reasoning/traces", json=payload).status_code == 200
        page = client.get("/reasoning/traces?offset=2&limit=2").json()
        assert len(page) == 2
        ids = [t["trace_id"] for t in page]
        assert len(set(ids)) == 2


def test_list_traces_search() -> None:
    with _bypass():
        payload = _payload(ReasoningStatus.DRAFT)
        payload["trace_id"] = "rtrace-search-1"
        payload["title"] = "atomic fission revision"
        assert client.post("/reasoning/traces", json=payload).status_code == 200
        r = client.get("/reasoning/traces?q=fission")
        assert r.status_code == 200
        body = r.json()
        assert any(t["trace_id"] == "rtrace-search-1" for t in body)


def test_trace_mutations_require_bearer_token():
    payload = _payload()
    with _bypass():
        _set_local_bypass(None)
        r = client.post("/reasoning/traces", json=payload)
    assert r.status_code == 401


def test_trace_status_patch_requires_bearer_token():
    with _bypass():
        payload = _payload()
        payload["trace_id"] = "rtrace-auth-1"
        r = client.post("/reasoning/traces", json=payload)
        assert r.status_code == 200

    tid = "rtrace-auth-1"
    r = client.patch(f"/reasoning/traces/{tid}/status", json={"status": ReasoningStatus.COMPLETED.value})
    assert r.status_code == 401


def test_backfill_decision_requires_bearer_token():
    with _bypass():
        payload = _payload()
        payload["trace_id"] = "rtrace-auth-2"
        payload["decision_id"] = None
        r = client.post("/reasoning/traces", json=payload)
        assert r.status_code == 200
        tid = r.json()["trace_id"]

    r = client.post(f"/reasoning/traces/{tid}/decision", json="dec-9002")
    assert r.status_code == 401
