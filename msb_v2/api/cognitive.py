from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.cognitive.confidence import ConfidenceEngine
from msb_v2.cognitive.decision_graph import DecisionGraph
from msb_v2.reasoning.integrity import EventStreamStore
from msb_v2.reasoning.store import ReasoningStore

router = APIRouter(tags=["cognitive"])

_store = ReasoningStore()
_stream = EventStreamStore()
_engine = ConfidenceEngine(store=_store, stream=_stream)
_graph_cache_key = ""
_graph_cache: dict[str, Any] = {"graph": DecisionGraph().to_dict(), "graphs": []}


def _refresh_graph_cache() -> None:
    graph = _engine.build_decision_graph()
    graphs = _engine.reason_graphs()
    _graph_cache["graph"] = graph.to_dict()
    _graph_cache["graphs"] = graphs


@router.get("/assess/{trace_id}")
def cognitive_assess(trace_id: str) -> JSONResponse:
    return JSONResponse(_engine.assess(trace_id))


@router.get("/reason/{trace_id}")
def cognitive_reason(trace_id: str) -> JSONResponse:
    return JSONResponse(_engine.reason_graphs([trace_id])[0])


@router.get("/graph")
def cognitive_graph() -> JSONResponse:
    _refresh_graph_cache()
    return JSONResponse(_graph_cache["graph"])


@router.get("/reasons")
def cognitive_reasons() -> JSONResponse:
    _refresh_graph_cache()
    return JSONResponse({"count": len(_graph_cache["graphs"]), "graphs": _graph_cache["graphs"]})
