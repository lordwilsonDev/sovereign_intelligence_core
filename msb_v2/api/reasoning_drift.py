from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from msb_v2.reasoning.scorer import score_from_events
from msb_v2.api.reasoning_integrity import _stream

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter()


@router.post("/baseline")
def set_baseline(trace_id: str) -> Dict[str, Any]:
    events = _stream.events_for_trace(trace_id)
    dicts = [
        {
            "event_id": e.event_id,
            "sequence": e.sequence,
            "kind": e.kind.value,
            "source": e.source,
            "payload": e.payload,
            "trace_id": e.trace_id,
            "decision_id": e.decision_id,
            "ts": e.ts,
        }
        for e in events
    ]
    assessment = score_from_events(dicts)
    baseline = _stream.set_baseline(trace_id, assessment.payload())
    return baseline


@router.post("/measure")
def measure_drift(trace_id: str) -> Dict[str, Any]:
    assessment = _stream.get_baseline(trace_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="baseline not set")
    current_events = _stream.events_for_trace(trace_id)
    dicts = [
        {
            "event_id": e.event_id,
            "sequence": e.sequence,
            "kind": e.kind.value,
            "source": e.source,
            "payload": e.payload,
            "trace_id": e.trace_id,
            "decision_id": e.decision_id,
            "ts": e.ts,
        }
        for e in current_events
    ]
    scored = score_from_events(dicts)
    result = _stream.measure_drift(trace_id, scored.payload())
    return result


@router.get("/all")
def list_drift() -> Dict[str, Any]:
    rows: Dict[str, Dict[str, Any]] = {}
    for e in _stream.global_stream(limit=9999):
        key = e.trace_id or e.decision_id
        if not key:
            continue
        row = rows.setdefault(
            key,
            {
                "trace_id": key,
                "has_baseline": False,
                "baseline": _stream.get_baseline(key).get("baseline"),
                "drift_count": 0,
                "latest_drift": None,
            },
        )
        if e.kind == "drift":
            row["drift_count"] += 1
            row["latest_drift"] = e.payload
        if _stream.get_baseline(key):
            row["has_baseline"] = True
    return {"baseline_count": sum(1 for r in rows.values() if r["has_baseline"]), "traces": sorted(rows.values(), key=lambda x: x.get("trace_id", ""))}
# HCL contract registration
_register_contract(HarnessContract(route="/reasoning/drift/baseline", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/reasoning/drift/measure", method="post", allow_anonymous=False))
