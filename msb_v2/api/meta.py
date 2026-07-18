from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter(tags=["meta"])


class RoutePayload(BaseModel):
    query: str
    context: dict | None = None


@router.post("/meta/route")
def meta_route_endpoint(payload: RoutePayload) -> JSONResponse:
    from cognitive_compiler.harness_dispatcher_v1 import HarnessDispatcher
    from cognitive_compiler.router_observer import RouterObserver

    dispatcher = HarnessDispatcher()
    result = dispatcher.dispatch(payload.query, context=payload.context or {})
    RouterObserver().record(result, payload.query)
    return JSONResponse(result)


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
    from cognitive_compiler.router_observer import RouterObserver

    dispatcher = HarnessDispatcher()
    context = {
        "intent": payload.intent,
        "trace_id": payload.trace_id,
        "preferred_harness": payload.intent if payload.intent != "default" else None,
    }
    result = dispatcher.dispatch(payload.query, context=context)
    RouterObserver().record(result, payload.query)
    return JSONResponse({
        "intent": payload.intent,
        "meta_routing": result.get("routing", {}),
        "primary_output": result.get("primary_output"),
        "temperature": result.get("temperature", {}),
        "scs_snapshot": result.get("scs_snapshot"),
    })
