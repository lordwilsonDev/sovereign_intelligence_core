from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.cognitive.visualizer_engine import TraceVisualizerEngine
from msb_v2.reasoning.integrity import EventStreamStore, ExecutionEvent, EventKind
from msb_v2.reasoning.store import ReasoningStore
from msb_v2.reasoning.types import ReasoningStatus, ReasoningTrace


def test_trace_visualizer_returns_visualization() -> None:
    trace = ReasoningTrace(trace_id="tv-1", title="Trace Visualization", status=ReasoningStatus.ACTIVE, steps=())
    store = ReasoningStore([trace])
    stream = EventStreamStore()
    stream.append(ExecutionEvent(event_id="e1", sequence=1, kind=EventKind.TOOL, source="unit", payload={"verdict": "accepted"}, trace_id="tv-1"))
    
    engine = TraceVisualizerEngine(store=store, stream=stream)
    data = engine.visualize("tv-1")
    
    assert data["trace_id"] == "tv-1"
    assert "steps" in data
    assert "critical_path" in data
    assert data["status"] == "active"


def test_trace_visualizer_timeline_returns_events() -> None:
    trace = ReasoningTrace(trace_id="tv-2", title="Timeline Trace", status=ReasoningStatus.COMPLETED, steps=())
    store = ReasoningStore([trace])
    stream = EventStreamStore()
    stream.append(ExecutionEvent(event_id="e1", sequence=1, kind=EventKind.TOOL, source="unit", payload={"verdict": "accepted"}, trace_id="tv-2"))
    stream.append(ExecutionEvent(event_id="e2", sequence=2, kind=EventKind.CONFIDENCE_ASSESSMENT, source="scorer", payload={"confidence": 0.9, "score": 0.8, "entropy": 0.1}, trace_id="tv-2"))
    
    engine = TraceVisualizerEngine(store=store, stream=stream)
    data = engine.timeline("tv-2")
    
    assert data["trace_id"] == "tv-2"
    assert len(data["events"]) == 2
    assert len(data["milestones"]) == 2


def test_visualizer_api_endpoints_exist() -> None:
    client = TestClient(create_app())
    for path in ["/visualizer/trace/tv-1", "/visualizer/timeline/tv-1"]:
        response = client.get(path)
        assert response.status_code == 200, path


def test_visualizer_api_timeline_endpoint() -> None:
    client = TestClient(create_app())
    
    response = client.get("/visualizer/timeline/tv-1")
    assert response.status_code == 200
    body = response.json()
    assert "events" in body
