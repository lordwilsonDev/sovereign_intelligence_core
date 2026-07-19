from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.reasoning.counterfactual import CounterfactualError, _event_to_dict, branch_trace
from msb_v2.api.reasoning_integrity import _stream

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter()


class CounterfactualRequest(BaseModel):
    trace_id: str
    branch_step: int | None = None
    flip_verdict: bool = True
    new_kind: str | None = None


@router.post("/branch")
def counterfactual_branch(payload: CounterfactualRequest) -> dict[str, Any]:
    try:
        return branch_trace(
            _stream,
            payload.trace_id,
            branch_step=payload.branch_step,
            flip_verdict=payload.flip_verdict,
            new_kind=payload.new_kind,
        )
    except CounterfactualError as exc:
        raise CounterfactualError(str(exc))


@router.get("/scan")
def scan() -> dict[str, Any]:
    all_events = _stream.global_stream(limit=10000)
    by_trace: dict[str, list[Any]] = {}
    for event in all_events:
        key = event.trace_id or event.decision_id
        if not key:
            continue
        by_trace.setdefault(key, []).append(_event_to_dict(event))

    signals = []
    for trace_id, events in by_trace.items():
        assessments = [e for e in events if e.get("kind") == "confidence_assessment"]
        drift = [e for e in events if e.get("kind") == "drift"]
        errors = [e for e in events if e.get("kind") == "error"]
        latest = assessments[-1] if assessments else None
        score = float(latest.get("payload", {}).get("score", 0.0)) if latest else 0.0
        confidence = float(latest.get("payload", {}).get("confidence", 0.0)) if latest else 0.0
        entropy = float(latest.get("payload", {}).get("entropy", 0.0)) if latest else 0.0
        grounded = bool(latest.get("payload", {}).get("ground_truth_accepted")) if latest else False
        signals.append({
            "trace_id": trace_id,
            "score": round(score, 4),
            "confidence": round(confidence, 4),
            "entropy": round(entropy, 4),
            "ground_truth_accepted": grounded,
            "drift_count": len(drift),
            "error_count": len(errors),
            "assessment_count": len(assessments),
        })

    signals.sort(key=lambda x: x.get("score", 0.0))
    strong = [s for s in signals if s.get("confidence", 0.0) >= 0.8 and s.get("score", 0.0) <= 0.6]
    weak = [s for s in signals if s.get("score", 0.0) < 0.6 and s.get("confidence", 0.0) < 0.6]
    return {
        "count": len(signals),
        "average": {
            "score": round(sum(s["score"] for s in signals)/len(signals), 4) if signals else 0.0,
            "confidence": round(sum(s["confidence"] for s in signals)/len(signals), 4) if signals else 0.0,
            "entropy": round(sum(s["entropy"] for s in signals)/len(signals), 4) if signals else 0.0,
        },
        "strong_signals": len(strong),
        "weak_signals": len(weak),
        "signals": signals,
    }
# HCL contract registration
_register_contract(HarnessContract(route="/reasoning/counterfactual/branch", method="post", allow_anonymous=False))
