from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from msb_v2.api.middleware import require_bearer_token

from msb_v2.v3.constraints import ConstraintEngine
from msb_v2.v3.memory_router import MemoryRouter
from msb_v2.v3.registry import get_registry as _get_registry
from msb_v2.v3.memory_pipeline import EventToMemoryPipeline, MemoryEnhancedPlanner, MemoryEntry, InMemoryStore
from msb_v2.knowledge.graph import KnowledgeGraph, LearningEngine

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter(tags=["v3"])

_shared_store = InMemoryStore()
_pipeline = EventToMemoryPipeline(store=_shared_store)
_graph = KnowledgeGraph()
_learning = LearningEngine(graph=_graph)
_planner = MemoryEnhancedPlanner(pipeline=_pipeline, learning_engine=_learning)


def _get_store() -> InMemoryStore:
    return _shared_store


def _get_pipeline() -> EventToMemoryPipeline:
    return _pipeline


def _get_planner() -> MemoryEnhancedPlanner:
    return _planner


@router.get("/v3/health")
def v3_health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@router.get("/v3/capabilities")
def v3_capabilities() -> JSONResponse:
    registry = _get_registry()
    return JSONResponse({"capabilities": [c.__dict__ for c in registry.list()], "summary": registry.summary()})


@router.get("/v3/memory/routes")
def v3_memory_routes() -> JSONResponse:
    router_mem = MemoryRouter()
    return JSONResponse(router_mem.summary())


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


@router.post("/v3/memory/ingest")
def ingest_memory(payload: dict, auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    pipeline = _get_pipeline()
    entry = pipeline.ingest(
        source=str(payload.get("source", "unknown")),
        content=str(payload.get("content", "")),
        memory_type=str(payload.get("memory_type", "episodic")),
        importance=float(payload.get("importance", 0.5)),
    )
    return JSONResponse({"ingested": True, "memory_id": entry.memory_id})


@router.post("/v3/memory/ingest/batch")
def ingest_batch(payload: list[dict], auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    pipeline = _get_pipeline()
    entries = pipeline.ingest_batch(payload or [])
    return JSONResponse({"ingested": len(entries), "memory_ids": [e.memory_id for e in entries]})


@router.get("/v3/memory/recent")
def recent_memories(limit: int = 20) -> dict:
    pipeline = _get_pipeline()
    entries = pipeline.recent(limit=limit)
    return {"entries": [e.__dict__ for e in entries], "count": len(entries)}


@router.get("/v3/memory/search")
def search_memories(q: str, limit: int = 20) -> dict:
    pipeline = _get_pipeline()
    entries = pipeline.recall(q, limit=limit)
    return {"query": q, "entries": [e.__dict__ for e in entries], "count": len(entries)}


@router.get("/v3/contracts")
def v3_contracts_list() -> JSONResponse:
    try:
        from msb_v2.v3.contracts import all_contracts as _all_contracts
        return JSONResponse({"count": len(_all_contracts()), "contracts": [c.__dict__ for c in _all_contracts()]})
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)


@router.post("/v3/planner/plan")
def plan_task(payload: dict, auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    planner = _get_planner()
    task = payload.get("task", "")
    context = payload.get("context")
    context_text = "" if context is None else (context if isinstance(context, str) else str(context))
    result = planner.plan(task=task, context=context_text or None)
    return JSONResponse(result)
# HCL contract registration
_register_contract(HarnessContract(route="/v3/capabilities/{capability_id}/validate", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/v3/memory/ingest", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/v3/memory/ingest/batch", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/v3/planner/plan", method="post", allow_anonymous=False))
