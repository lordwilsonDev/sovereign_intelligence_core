from __future__ import annotations

import copy
from typing import Any

from msb_v2.reasoning.integrity import EventKind, ExecutionEvent
from msb_v2.reasoning.scorer import ConfidenceAssessment, score_from_events

_BRANCH_MARKER = "_branch"

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


def _dict_to_execution_event(data: dict[str, Any]) -> ExecutionEvent:
    kind = data.get("kind", "execution")
    return ExecutionEvent(
        event_id=data.get("event_id", ""),
        sequence=int(data.get("sequence", 0)),
        kind=EventKind(kind),
        source=data.get("source", ""),
        payload=data.get("payload") or {},
        trace_id=data.get("trace_id"),
        decision_id=data.get("decision_id"),
        ts=data.get("ts", ""),
    )

_adk_event = None
_branch_path = None


def _get_adk_event_class() -> type | None:
    global _adk_event
    if _adk_event is None:
        try:
            from google.adk.events.event import Event as _Event
            _adk_event = _Event
        except Exception:
            _adk_event = None
    return _adk_event


def _get_branch_path_class() -> type | None:
    global _branch_path
    if _branch_path is None:
        try:
            from google.adk.events._node_path_builder import _NodePathBuilder as _BranchPath
            _branch_path = _BranchPath
        except Exception:
            _branch_path = None
    return _branch_path


def to_adk_event(event: ExecutionEvent) -> dict[str, Any]:
    cls = _get_adk_event_class()
    if cls is None:
        raise ImportError("google.adk.events.event.Event is not available")
    data = _event_to_dict(event)
    return cls.model_validate(data).model_dump(mode="json", by_alias=True)


def from_adk_event(data: dict[str, Any]) -> ExecutionEvent:
    data_n = dict(data)
    kind = data_n.pop("kind", "execution")
    data_n["kind"] = kind
    return _dict_to_execution_event(data_n)


def _apply_branch(branched, branch_step, flip_verdict, new_kind):
    chosen_index = None
    if branch_step is not None:
        chosen_index = next((i for i, e in enumerate(branched) if e.get("sequence") == branch_step), None)
        if chosen_index is None:
            raise ValueError("branch step not found")
        event = branched[chosen_index]
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
            branched[chosen_index] = event
    return branched, chosen_index


def _as_adk_optional(event_dict):
    event_cls = _get_adk_event_class()
    if event_cls is None:
        return event_dict
    try:
        return event_cls.model_validate(event_dict).model_dump(mode="json", by_alias=True)
    except Exception:
        return event_dict


def _assemble_branch_trace_result(trace_id, original_dicts, original_score, branched, branch_step, chosen_index, cf_score, chosen_dict):
    return {
        "trace_id": trace_id,
        "adk_available": _get_adk_event_class() is not None,
        "original": {
            "trace": [_as_adk_optional(e) for e in original_dicts],
            "score": original_score.score,
            "confidence": original_score.confidence,
            "concurrence": original_score.concurrence,
            "dissent": original_score.dissent,
            "entropy": original_score.entropy,
        },
        "counterfactual": {
            "trace": [_as_adk_optional(e) for e in branched],
            "score": cf_score.score,
            "confidence": cf_score.confidence,
            "concurrence": cf_score.concurrence,
            "dissent": cf_score.dissent,
            "entropy": cf_score.entropy,
            "branch_step": branch_step,
            "branch_index": chosen_index,
            "branched_event": _as_adk_optional(chosen_dict) if chosen_dict is not None else None,
        },
        "delta": {
            "score": round(cf_score.score - original_score.score, 6),
            "confidence": round(cf_score.confidence - original_score.confidence, 6),
            "entropy": round(cf_score.entropy - original_score.entropy, 6),
        },
    }


def branch_trace_adk(
    stream: Any,
    trace_id: str,
    branch_step: int | None = None,
    flip_verdict: bool = True,
    new_kind: str | None = None,
) -> dict[str, Any]:
    original = stream.events_for_trace(trace_id)
    if not original:
        raise ValueError("trace not found")

    original_dicts = [_event_to_dict(e) for e in original]
    original_score = _score_from_trace(original)

    branched = copy.deepcopy(original_dicts)
    branched, chosen_index = _apply_branch(branched, branch_step, flip_verdict, new_kind)

    cf_score = score_from_events(branched)
    chosen_dict = branched[chosen_index] if chosen_index is not None else None

    return _assemble_branch_trace_result(
        trace_id, original_dicts, original_score, branched, branch_step, chosen_index, cf_score, chosen_dict
    )


_add_adk_prefix_marker = False


def _add_adk_prefix(stream: Any, trace_id: str, event: ExecutionEvent) -> str | None:
    global _add_adk_prefix_marker
    return trace_id + ("#ADK" if _add_adk_prefix_marker else "")


def _score_from_trace(events: list[ExecutionEvent]) -> ConfidenceAssessment:
    dicts = [_event_to_dict(e) for e in events]
    return score_from_events(dicts)
