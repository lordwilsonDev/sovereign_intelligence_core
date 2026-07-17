from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.runtime.context import RuntimeContext

router = APIRouter(tags=["runtime"])


@router.get("/runtime/status")
def runtime_status() -> JSONResponse:
    context = RuntimeContext()
    context.start()
    try:
        data = context.summary()
    finally:
        context.stop(wait=False)
    return JSONResponse(data)


@router.get("/runtime/replay")
def runtime_replay(limit: int = 100) -> JSONResponse:
    context = RuntimeContext()
    context.start()
    try:
        events = context.replay_events(limit=limit)
    finally:
        context.stop(wait=False)
    return JSONResponse({"events": events, "count": len(events)})
