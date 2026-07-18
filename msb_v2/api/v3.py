from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.v3.constraints import ConstraintEngine
from msb_v2.v3.memory_router import MemoryRouter
from msb_v2.v3.registry import get_registry as _get_registry

router = APIRouter(tags=["v3"])


@router.get("/v3/capabilities")
def v3_capabilities() -> JSONResponse:
    registry = _get_registry()
    return JSONResponse({"capabilities": [c.__dict__ for c in registry.list()], "summary": registry.summary()})


@router.get("/v3/memory/routes")
def v3_memory_routes() -> JSONResponse:
    router = MemoryRouter()
    return JSONResponse(router.summary())


@router.post("/v3/capabilities/{capability_id}/validate")
def v3_validate(capability_id: str) -> JSONResponse:
    registry = _get_registry()
    node = registry.get(capability_id)
    if node is None:
        return JSONResponse({"error": "not_found", "capability_id": capability_id}, status_code=404)
    engine = ConstraintEngine()
    result = engine.check({
        "cost_estimate": node.cost_estimate,
        "autonomy_level": node.autonomy_level.value,
        "tool": None,
        "tags": [],
    })
    return JSONResponse({"capability_id": capability_id, "constraint_result": result})


@router.get("/v3/summary")
def v3_summary() -> JSONResponse:
    registry = _get_registry()
    memory = MemoryRouter()
    engine = ConstraintEngine()
    return JSONResponse({
        "capabilities": registry.summary(),
        "memory": memory.summary(),
        "constraints": engine.summary(),
    })
