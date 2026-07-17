from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from msb_v2.cognitive.decision_graph import DecisionGraph, DecisionNode, ReasonEdge
from msb_v2.cognitive.reason_graph import from_traces
from msb_v2.reasoning.integrity import EventStreamStore
from msb_v2.reasoning.scorer import score_from_events
from msb_v2.reasoning.store import ReasoningStore
from msb_v2.reasoning.types import ReasoningTrace


@dataclass
class ConfidenceEngine:
    store: ReasoningStore
    stream: EventStreamStore

    def assess(self, trace_id: str) -> Dict[str, Any]:
        trace = self.store.get_trace(trace_id)
        events = self.stream.events_for_trace(trace_id)
        assessment = score_from_events(
            [
                {
                    "event_id": event.event_id,
                    "sequence": event.sequence,
                    "kind": event.kind.value,
                    "source": event.source,
                    "payload": event.payload or {},
                    "trace_id": event.trace_id,
                    "decision_id": event.decision_id,
                }
                for event in events
            ]
        )
        return {
            "trace_id": trace_id,
            "title": trace.title,
            "status": trace.status.value if hasattr(trace.status, "value") else str(trace.status),
            "score": assessment.score,
            "confidence": assessment.confidence,
            "entropy": assessment.entropy,
            "concurrence": assessment.concurrence,
            "dissent": assessment.dissent,
        }

    def build_decision_graph(self, traces: Optional[List[ReasoningTrace]] = None) -> DecisionGraph:
        if traces is None:
            traces = self.store.list_traces()
        graph = DecisionGraph()
        for trace in traces:
            assessment = self.assess(trace.trace_id)
            graph.add(
                DecisionNode(
                    decision_id=trace.decision_id or trace.trace_id,
                    trace_id=trace.trace_id,
                    status=assessment["status"],
                    source=trace.title,
                    score=assessment["score"],
                    confidence=assessment["confidence"],
                    entropy=assessment["entropy"],
                )
            )
            for ref in self.store.refs_for(trace.decision_id or ""):
                if ref.decision_id and ref.decision_id != (trace.decision_id or ""):
                    graph.link(
                        ReasonEdge(
                            source_id=ref.decision_id,
                            target_id=trace.decision_id or trace.trace_id,
                            weight=assessment["confidence"],
                            kind="dependency",
                        )
                    )
        return graph

    def reason_graphs(self, trace_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        traces = [self.store.get_trace(tid) for tid in trace_ids] if trace_ids else self.store.list_traces()
        graphs = from_traces(traces)
        out: List[Dict[str, Any]] = []
        for graph in graphs:
            out.append(
                {
                    "trace_id": graph.trace_id,
                    "title": graph.title,
                    "score": graph.score,
                    "confidence": graph.confidence,
                    "entropy": graph.entropy,
                    "steps": graph.steps,
                    "conclusion": graph.conclusion,
                }
            )
        return out
