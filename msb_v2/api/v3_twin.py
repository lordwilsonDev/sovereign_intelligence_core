from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.v3.digital_twin import DigitalTwinHook

router = APIRouter(tags=["v3-twin"])

_hooks = DigitalTwinHook()


@router.post("/v3/twin")
def create_twin(payload: dict) -> JSONResponse:
    name = payload.get("name", "")
    state = payload.get("state", {})
    fork_of = payload.get("fork_of")
    twin = _hooks.create(name=name, state=state, fork_of=fork_of)
    return JSONResponse({"twin_id": twin.twin_id})


@router.post("/v3/twin/{twin_id}/snapshot")
def snapshot_twin(twin_id: str) -> JSONResponse:
    snap = _hooks.snapshot(twin_id)
    if snap is None:
        return JSONResponse({"error": "twin_not_found", "twin_id": twin_id}, status_code=404)
    return JSONResponse({"snapshot_id": snap.twin_id})


@router.post("/v3/twin/{twin_id}/evolve")
def evolve_twin(twin_id: str, payload: dict) -> JSONResponse:
    evolved = _hooks.evolve(twin_id, payload.get("delta", {}))
    if evolved is None:
        return JSONResponse({"error": "twin_not_found", "twin_id": twin_id}, status_code=404)
    return JSONResponse({"twin_id": evolved.twin_id})


@router.get("/v3/twin/{twin_id}")
def get_twin(twin_id: str) -> JSONResponse:
    twin = _hooks.get(twin_id)
    if twin is None:
        return JSONResponse({"error": "twin_not_found", "twin_id": twin_id}, status_code=404)
    return JSONResponse(twin.__dict__)


@router.get("/v3/twin/summary")
def twin_summary() -> JSONResponse:
    return JSONResponse(_hooks.summary())
