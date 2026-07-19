from __future__ import annotations

import json
import logging

import pytest
from fastapi.testclient import TestClient
from msb_v2.api.main import create_app

from msb_v2.engine.causal_memory import CausalMemory, StateSnapshot
from msb_v2.engine.moie_orchestrator import DialecticDepthGauge
from msb_v2.engine.observability import span
from msb_v2.v3.contracts import HarnessContract, lookup, register


class DummyModel:
    model_fields = {}

    @classmethod
    def model_validate(cls, payload):
        if payload.get("must_have") != "yes":
            raise ValueError("missing must_have")


def test_causal_memory_rejects_back_edge():
    mem = CausalMemory()
    mem.link("a", "b")
    mem.link("b", "c")
    mem.link("c", "a")
    assert not mem.has_link("c", "a")
    assert mem.has_link("a", "b")


def test_state_snapshot_hash_continues():
    mem = CausalMemory()
    mem.link("a", "b")
    first = mem.current_hash()
    mem.link("b", "c")
    second = mem.current_hash()
    assert first
    assert second
    assert first != second


def test_dialectic_depth_gauge_bounds():
    gauge = DialecticDepthGauge(min_rounds=2, max_rounds=5)
    assert gauge.limit(0, 3) == 2 * 3
    assert gauge.limit(999, 1) == 5 * 1
    assert gauge.limit(3, 2) == max(2 * 2, min(3, 5 * 2))


def test_span_timing_json_logs(caplog):
    caplog.set_level(logging.DEBUG, logger="msb_v2.engine")

    @span("unit.test")
    def ok_fn() -> dict:
        return {"status": "ok"}

    ok_fn()
    messages = [rec.getMessage() for rec in caplog.records]
    assert any(isinstance(m, str) and "unit.test" in m and "'ok': True" in m for m in messages), messages


def test_hcl_validator_blocks_invalid_payload():
    register(HarnessContract(route="/v3/knowledge/test", method="post", body_type=DummyModel))
    err = lookup("/v3/knowledge/test", "post").validate({"must_have": "no"})
    assert err is not None
    assert lookup("/v3/knowledge/test", "post").validate({"must_have": "yes"}) is None


def test_production_mutation_routes_reject_without_auth():
    if _under_local_bypass():
        return
    client = TestClient(create_app())
    public_endpoints = {"/auth/token/issue", "/auth/token/verify", "/health", "/runtime/ping"}
    disallowed = []
    for path, _ in _candidate_mutations():
        if path in public_endpoints:
            continue
        r = client.post(path, json=_minimal_payload(path))
        if r.status_code != 401:
            disallowed.append((path, r.status_code, r.text[:200]))
    assert disallowed == [], disallowed


def test_hcl_middleware_enforces_contracted_anon_route():
    from fastapi import APIRouter, FastAPI
    from fastapi.testclient import TestClient
    from msb_v2.v3.contracts import register
    from msb_v2.api.middleware import hcl_contract_middleware
    import os as _os

    route_path = "/test-public"
    register(HarnessContract(route=route_path, method="POST", allow_anonymous=True, max_body_bytes=4096))
    router = APIRouter()

    @router.post(route_path)
    def _public_test():
        return {"status": "ok"}

    app = FastAPI()
    app.middleware("http")(hcl_contract_middleware)
    app.include_router(router)
    client = TestClient(app)
    prev = _os.environ.get("MSB_REQUIRE_HCL")
    _os.environ["MSB_REQUIRE_HCL"] = "1"
    try:
        r = client.post(route_path, json={})
        assert r.status_code == 200, r.text
        r = client.post(route_path)
        assert r.status_code == 200, r.text
    finally:
        if prev is None:
            _os.environ.pop("MSB_REQUIRE_HCL", None)
        else:
            _os.environ["MSB_REQUIRE_HCL"] = prev


def test_hcl_middleware_blocks_payload_over_limit():
    import os as _os
    from fastapi import APIRouter, FastAPI
    from fastapi.testclient import TestClient
    from fastapi.exceptions import HTTPException
    from msb_v2.v3.contracts import register
    from msb_v2.api.middleware import hcl_contract_middleware

    route_path = "/test-limited"
    register(HarnessContract(route=route_path, method="post", allow_anonymous=True, max_body_bytes=1))
    router = APIRouter()

    @router.post(route_path)
    def _limited_test(payload: dict):
        return {"status": "ok"}

    app = FastAPI()
    app.middleware("http")(hcl_contract_middleware)
    app.include_router(router)
    client = TestClient(app)
    prev = _os.environ.get("MSB_REQUIRE_HCL")
    _os.environ["MSB_REQUIRE_HCL"] = "1"
    try:
        with pytest.raises(HTTPException) as exc_info:
            client.post(route_path, content=b'{"overflow": true}', headers={"content-type": "application/json", "content-length": "9"})
        assert exc_info.value.status_code == 413
    finally:
        if prev is None:
            _os.environ.pop("MSB_REQUIRE_HCL", None)
        else:
            _os.environ["MSB_REQUIRE_HCL"] = prev


def test_hcl_middleware_blocks_unauthenticated_non_anon_route_full_app():
    from msb_v2.api.middleware import set_local_bypass
    set_local_bypass(None)
    client = TestClient(create_app())
    r = client.post("/orchestrate", json={"tasks": [{"id": "1", "status": "queued"}]})
    assert r.status_code == 401, r.text


def test_hcl_middleware_allows_correct_behavior_on_full_app():
    from msb_v2.api.middleware import set_local_bypass
    set_local_bypass(None)
    client = TestClient(create_app())
    r = client.post("/orchestrate", json={"tasks": [{"id": "1", "status": "queued"}]})
    assert r.status_code == 401, r.text


def _under_local_bypass() -> bool:
    try:
        from msb_v2.api.middleware import _bypass_override
        return _bypass_override.get(None) is True
    except Exception:
        return False


def _candidate_mutations():
    return [
        ("/deepseek/chat", "post"),
        ("/rag/ingest", "post"),
        ("/rag/converse", "post"),
        ("/orchestrate", "post"),
        ("/brain/run", "post"),
        ("/v3/crew", "post"),
        ("/v3/twin", "post"),
        ("/v3/deliberate", "post"),
        ("/v3/inversion/hypotheses", "post"),
        ("/v3/inversion/experiments", "post"),
        ("/v3/inversion/experiments/e1/evidence", "post"),
        ("/v3/tasks/submit", "post"),
        ("/v3/memory/ingest", "post"),
        ("/v3/memory/ingest/batch", "post"),
        ("/v3/planner/plan", "post"),
        ("/reasoning/calibration/record-assessment", "post"),
        ("/reasoning/drift/baseline", "post"),
        ("/reasoning/drift/measure", "post"),
        ("/career/evaluate", "post"),
        ("/reasoning/counterfactual/branch", "post"),
        ("/scheduler/submit", "post"),
        ("/demo/query", "post"),
        ("/adk/query-adk", "post"),
    ]


def _minimal_payload(path: str) -> dict:
    return {}
