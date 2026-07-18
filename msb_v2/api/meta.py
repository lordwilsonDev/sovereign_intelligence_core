from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from cognitive_compiler.router_observer import RouterObserver
from msb_v2.transport.compression import compress_content

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


@router.post("/meta/route")
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


@router.post("/brain/meta-run")
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
        "temperature": result.get("temperature", {}),
        "scs_snapshot": result.get("scs_snapshot"),
    })
