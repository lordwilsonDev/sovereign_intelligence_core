from __future__ import annotations

from msb_v2.cognitive.decision_graph import DecisionGraph, DecisionNode, ReasonEdge
from msb_v2.cognitive.confidence import ConfidenceEngine
from msb_v2.reasoning.integrity import EventStreamStore, ExecutionEvent, EventKind
from msb_v2.cognitive.reason_graph import from_trace


def test_decision_graph_nodes_and_links() -> None:
    graph = DecisionGraph()
    graph.add(DecisionNode(decision_id="d1", trace_id="t1", status="active", score=0.9))
    graph.add(DecisionNode(decision_id="d2", trace_id="t2", status="active", score=0.4))
    graph.link(ReasonEdge(source_id="d1", target_id="d2", weight=0.9, kind="supports"))

    nodes = list(graph.to_dict()["nodes"])
    assert {n["decision_id"] for n in nodes} == {"d1", "d2"}
    edges = graph.to_dict()["edges"]
    assert edges[0]["source"] == "d1"
    assert edges[0]["target"] == "d2"
    assert len(graph.successors("d1")) == 1
    assert len(graph.predecessors("d2")) == 1


def test_reason_graph_from_trace() -> None:
    graph = from_trace(
        type(
            "Trace",
            (),
            {
                "trace_id": "trace-1",
                "title": "alpha",
                "steps": (type("Step", (), {"step_index": 0, "claim": "c", "evidence_refs": (), "assumptions": (), "confidence": 0.8})(),),
                "conclusion": "alpha",
                "metadata": {"score": 0.7, "confidence": 0.8, "entropy": 0.2},
            },
        )()
    )
    assert graph.title == "alpha"
    assert graph.steps[0]["claim"] == "c"
    assert graph.confidence == 0.8


def test_confidence_engine_assess_and_graph() -> None:
    store = type(
        "R",
        (),
        {
            "get_trace": lambda self, tid: type(
                "Trace",
                (),
                {
                    "trace_id": tid,
                    "title": "alpha",
                    "steps": (),
                    "status": "active",
                    "conclusion": "ok",
                    "decision_id": "d1",
                    "metadata": {},
                },
            )(),
            "list_traces": lambda self: [
                type(
                    "Trace",
                    (),
                    {
                        "trace_id": "t1",
                        "decision_id": "d1",
                        "title": "alpha",
                        "steps": (),
                        "status": "active",
                        "conclusion": "ok",
                        "metadata": {},
                    },
                )()
            ],
            "refs_for": lambda self, _id: [],
        },
    )()
    stream = EventStreamStore()
    stream.append(ExecutionEvent(event_id="e1", sequence=1, kind=EventKind.TOOL, source="unit", payload={"verdict": "accepted"}, trace_id="t1"))

    engine = ConfidenceEngine(store=store, stream=stream)
    out = engine.assess("t1")
    assert out["trace_id"] == "t1"
    assert out["score"] == 0.65

    graph = engine.build_decision_graph()
    nodes = list(graph.to_dict()["nodes"])
    assert len(nodes) == 1

    reason_graphs = engine.reason_graphs(["t1"])
    assert reason_graphs[0]["title"] == "alpha"


def test_confidence_engine_empty_trace_uses_zeroed_metrics() -> None:
    store = type("R", (), {"get_trace": lambda self, tid: type("Trace", (), {"trace_id": tid, "title": "empty", "status": "draft", "steps": (), "conclusion": "", "metadata": {}})(), "refs_for": lambda self, _id: []})()
    stream = EventStreamStore()
    engine = ConfidenceEngine(store=store, stream=stream)
    out = engine.assess("none")
    assert out["score"] == 0.5  # tool_calls=1 -> 0.5 + 0.15
    assert out["confidence"] == 0.6
