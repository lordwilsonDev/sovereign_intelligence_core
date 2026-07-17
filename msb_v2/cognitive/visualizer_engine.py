from __future__ import annotations

from typing import Any, Dict, List

from msb_v2.cognitive.trace_visualizer import ConfidenceTimeline, TraceVisualization, TraceStepView
from msb_v2.cognitive.confidence import ConfidenceEngine
from msb_v2.reasoning.integrity import EventStreamStore, ExecutionEvent
from msb_v2.reasoning.store import ReasoningStore


class TraceVisualizerEngine:
    def __init__(self, store: ReasoningStore, stream: EventStreamStore) -> None:
        self.store = store
        self.stream = stream
        self.scorer = ConfidenceEngine(store=store, stream=stream)

    def visualize(self, trace_id: str) -> Dict[str, Any]:
        trace = self.store.get_trace(trace_id)
        assessment = self.scorer.assess(trace_id)
        
        steps = []
        for idx, step in enumerate(getattr(trace, "steps", [])):
            confidence = step.confidence if step.confidence else assessment["confidence"]
            verdict = _detect_verdict(step, assessment)
            risk = _classify_risk(confidence, assessment.get("entropy", 0.0))
            steps.append(TraceStepView(step_index=idx, claim=step.claim, confidence=confidence, verdict=verdict, risk=risk))
        
        critical_path = self._compute_critical_path(trace_id, steps)
        
        visualization = TraceVisualization(
            trace_id=trace_id,
            title=getattr(trace, "title", trace_id),
            status=assessment["status"],
            conclusion=trace.conclusion or "",
            score=assessment["score"],
            confidence=assessment["confidence"],
            entropy=assessment["entropy"],
            steps=steps,
            critical_path=critical_path,
        )
        return visualization.to_dict()

    def timeline(self, trace_id: str) -> Dict[str, Any]:
        events = [_event_to_dict(e) for e in self.stream.events_for_trace(trace_id)]
        milestones = _extract_milestone_events(events)
        return ConfidenceTimeline(trace_id=trace_id, events=events, milestones=milestones).to_dict()

    def _compute_critical_path(self, trace_id: str, steps: List[TraceStepView]) -> List[int]:
        if not steps:
            return []
        return [step.step_index for step in steps if step.confidence >= 0.8 and step.risk in ("low", "medium")]


def _event_to_dict(event: ExecutionEvent) -> Dict[str, Any]:
    return {
        "event_id": event.event_id,
        "sequence": event.sequence,
        "kind": event.kind.value,
        "source": event.source,
        "payload": event.payload or {},
        "trace_id": event.trace_id,
        "decision_id": event.decision_id,
        "ts": event.ts,
    }


def _detect_verdict(step: Any, assessment: Dict[str, Any]) -> str:
    if assessment.get("dissent", 0.0) > 0.5:
        return "contested"
    if assessment.get("confidence", 0.0) >= 0.8:
        return "accepted"
    return "pending"


def _classify_risk(confidence: float, entropy: float) -> str:
    if confidence >= 0.8 and entropy <= 0.3:
        return "low"
    if confidence >= 0.6 and entropy <= 0.6:
        return "medium"
    return "high"


def _extract_milestone_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    milestones: List[Dict[str, Any]] = []
    for event in events:
        kind = event.get("kind", "")
        payload = event.get("payload") or {}
        confidence_assessment = payload.get("confidence")
        if kind in ("confidence_assessment", "tool", "human"):
            milestone = dict(event)
            milestone["milestone_type"] = kind
            if confidence_assessment is not None:
                milestone["confidence"] = confidence_assessment
            milestones.append(milestone)
    return milestones
