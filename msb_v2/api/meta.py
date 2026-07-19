from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from cognitive_compiler.router_observer import RouterObserver
from msb_v2.api.middleware import require_bearer_token
from msb_v2.transport.compression import compress_content

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter(tags=["meta"])

_COMPRESS_THRESHOLD = 2000


def _maybe_compress(value):
    try:
        raw = str(value).encode("utf-8")
    except Exception:
        return value
    if len(raw) <= _COMPRESS_THRESHOLD:
        return value
    compressed = compress_content("transport", raw)
    if compressed is None or len(compressed) >= len(raw):
        return value
    return compressed.decode("utf-8", errors="replace")

_observer = RouterObserver(log_path="runtime/meta_routing_observations.jsonl")


class RoutePayload(BaseModel):
    query: str
    context: dict | None = None


@router.post("/meta/route", dependencies=[Depends(require_bearer_token)])
def meta_route_endpoint(payload: RoutePayload) -> JSONResponse:
    from cognitive_compiler.harness_dispatcher_v1 import HarnessDispatcher

    dispatcher = HarnessDispatcher()
    result = dispatcher.dispatch(payload.query, context=payload.context or {})
    _observer.record(result, payload.query)
    compressed = _maybe_compress(result)
    return JSONResponse(compressed)


@router.get("/meta/health")
def meta_health() -> JSONResponse:
    return JSONResponse({"status": "ok", "module": "meta"})


class BrainMetaPayload(BaseModel):
    query: str
    intent: str = "default"
    trace_id: str | None = None


@router.post("/brain/meta-run", dependencies=[Depends(require_bearer_token)])
def brain_meta_run(payload: BrainMetaPayload) -> JSONResponse:
    from cognitive_compiler.harness_dispatcher_v1 import HarnessDispatcher

    dispatcher = HarnessDispatcher()
    context = {
        "intent": payload.intent,
        "trace_id": payload.trace_id,
        "preferred_harness": payload.intent if payload.intent != "default" else None,
    }
    result = dispatcher.dispatch(payload.query, context=context)
    _observer.record(result, payload.query)
    return JSONResponse({
        "intent": payload.intent,
        "meta_routing": result.get("routing", {}),
        "primary_output": result.get("primary_output"),
        "secondary_output": result.get("secondary_output"),
        "temperature": result.get("temperature", {}),
        "scs_snapshot": result.get("scs_snapshot"),
        "artifact_summary": result.get("artifact_summary"),
        "telemetry": result.get("telemetry"),
        "elapsed_s": result.get("elapsed_s"),
    })
# HCL contract registration
_register_contract(HarnessContract(route="/meta/route", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/brain/meta-run", method="post", allow_anonymous=False))
