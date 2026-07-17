from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException
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


@router.post("/runtime/snapshots")
def runtime_create_snapshot(tag: str = Body(...), source: str = Body(...)) -> JSONResponse:
    context = RuntimeContext()
    context.start()
    try:
        tag_out = context.create_snapshot(tag=tag, source=source)
    finally:
        context.stop(wait=False)
    return JSONResponse({"tag": tag_out})


@router.get("/runtime/snapshots")
def runtime_list_snapshots(tag: str) -> JSONResponse:
    context = RuntimeContext()
    context.start()
    try:
        items = context.snapshots.list_snapshots(tag)
    finally:
        context.stop(wait=False)
    return JSONResponse({"tag": tag, "snapshots": items})


@router.post("/runtime/snapshots/rollback")
def runtime_rollback_snapshot(tag: str = Body(...), dest: str = Body(...)) -> JSONResponse:
    context = RuntimeContext()
    context.start()
    try:
        context.rollback_snapshot(tag=tag, dest=dest)
    finally:
        context.stop(wait=False)
    return JSONResponse({"tag": tag, "dest": dest})
