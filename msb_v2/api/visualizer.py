from __future__ import annotations


from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.cognitive.visualizer_engine import TraceVisualizerEngine
from msb_v2.reasoning.integrity import EventStreamStore
from msb_v2.reasoning.store import ReasoningStore

router = APIRouter(tags=["visualizer"])

_store = ReasoningStore()
_stream = EventStreamStore()
_visualizer = TraceVisualizerEngine(store=_store, stream=_stream)


@router.get("/trace/{trace_id}")
def visualizer_trace(trace_id: str) -> JSONResponse:
    engine = TraceVisualizerEngine(store=ReasoningStore(), stream=EventStreamStore())
    try:
        data = engine.visualize(trace_id)
    except KeyError:
        data = {"trace_id": trace_id, "status": "not_found", "steps": [], "critical_path": []}
    return JSONResponse(data)


@router.get("/timeline/{trace_id}")
def visualizer_timeline(trace_id: str) -> JSONResponse:
    engine = TraceVisualizerEngine(store=ReasoningStore(), stream=EventStreamStore())
    data = engine.timeline(trace_id)
    return JSONResponse(data)
