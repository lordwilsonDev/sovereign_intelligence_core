from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["meta"])


@router.post("/meta/route")
def meta_route_endpoint(payload: dict) -> JSONResponse:
    from cognitive_compiler.harness_dispatcher_v1 import HarnessDispatcher

    query = str(payload.get("query", ""))
    context = payload.get("context", {}) or {}
    dispatcher = HarnessDispatcher()
    result = dispatcher.dispatch(query, context=context)
    return JSONResponse(result)


@router.get("/meta/health")
def meta_health() -> JSONResponse:
    return JSONResponse({"status": "ok", "module": "meta"})
