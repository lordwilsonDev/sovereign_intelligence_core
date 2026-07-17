from __future__ import annotations

from copy import deepcopy
from typing import Any

from msb_v2.reasoning.integrity import ExecutionEvent, EventKind, EventStreamStore
from msb_v2.reasoning.scorer import ConfidenceAssessment, score_from_events


class CounterfactualError(Exception):
    pass


def branch_trace(
    stream: EventStreamStore,
    trace_id: str,
    branch_step: int | None = None,
    flip_verdict: bool = True,
    new_kind: str | None = None,
) -> dict[str, Any]:
    original = stream.events_for_trace(trace_id)
    if not original:
        raise CounterfactualError("trace not found")

    original_dicts = [_event_to_dict(e) for e in original]
    original_score = _score_from_trace(original)

    branched = deepcopy(original_dicts)
    if branch_step is not None:
        idx = next((i for i, e in enumerate(branched) if e.get("sequence") == branch_step), None)
        if idx is None:
            raise CounterfactualError("branch step not found")
        event = branched[idx]
        payload = event.get("payload") or {}
        if flip_verdict and "verdict" in payload:
            payload = dict(payload)
            payload["verdict"] = "rejected" if payload.get("verdict") == "accepted" else "accepted"
            event["payload"] = payload
        if new_kind is not None:
            event = dict(event)
            try:
                event["kind"] = EventKind(new_kind).value
            except ValueError:
                event["kind"] = new_kind
            branched[idx] = event

    cf_assessment = score_from_events(branched)
    return {
        "trace_id": trace_id,
        "original": {
            "trace": original_dicts,
            "score": original_score.score,
            "confidence": original_score.confidence,
            "concurrence": original_score.concurrence,
            "dissent": original_score.dissent,
            "entropy": original_score.entropy,
        },
        "counterfactual": {
            "trace": branched,
            "score": cf_assessment.score,
            "confidence": cf_assessment.confidence,
            "concurrence": cf_assessment.concurrence,
            "dissent": cf_assessment.dissent,
            "entropy": cf_assessment.entropy,
        },
        "delta": {
            "score": round(cf_assessment.score - original_score.score, 6),
            "confidence": round(cf_assessment.confidence - original_score.confidence, 6),
            "entropy": round(cf_assessment.entropy - original_score.entropy, 6),
        },
    }


def _event_to_dict(event: ExecutionEvent) -> dict[str, Any]:
    return {
        "event_id": event.event_id,
        "sequence": event.sequence,
        "kind": event.kind.value,
        "source": event.source,
        "payload": event.payload,
        "trace_id": event.trace_id,
        "decision_id": event.decision_id,
        "ts": event.ts,
    }


def _latest_assessment(events: list[ExecutionEvent]) -> ConfidenceAssessment:
    for event in reversed(events):
        if event.kind == EventKind.CONFIDENCE_ASSESSMENT:
            data = event.payload or {}
            return ConfidenceAssessment(
                trace_id=data.get("trace_id"),
                statement_id=data.get("statement_id"),
                score=float(data.get("score", 0.0)),
                confidence=float(data.get("confidence", 0.0)),
                concurrence=float(data.get("concurrence", 0.0)),
                dissent=float(data.get("dissent", 0.0)),
                entropy=float(data.get("entropy", 0.0)),
                ground_truth_accepted=data.get("ground_truth_accepted"),
                notes=data.get("notes", ""),
                ts=data.get("ts", ""),
            )
    return ConfidenceAssessment(
        trace_id=None,
        statement_id=None,
        score=0.0,
        confidence=0.0,
        concurrence=0.0,
        dissent=0.0,
        entropy=0.0,
        ground_truth_accepted=None,
        notes="",
    )


def _score_from_trace(events: list[ExecutionEvent]) -> ConfidenceAssessment:
    dicts = [_event_to_dict(e) for e in events]
    return score_from_events(dicts)
