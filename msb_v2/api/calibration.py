from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.reasoning.calibration import CalibrationStore

router = APIRouter(tags=["reasoning"])
_calibration_store = CalibrationStore()


@router.post("/calibration/record")
def record_calibration(body: Dict[str, Any]) -> Dict[str, Any]:
    statement_id = str(body.get("statement_id") or "")
    confidence = float(body.get("confidence") or 0.0)
    actual = bool(body.get("actual"))
    trace_id = body.get("trace_id")
    decision_id = body.get("decision_id")
    record = _calibration_store.record(
        statement_id=statement_id,
        confidence=confidence,
        actual=actual,
        trace_id=trace_id,
        decision_id=decision_id,
    )
    return record.payload()


@router.post("/calibration/record-assessment")
def record_assessment(assessment: Dict[str, Any]) -> Dict[str, Any]:
    confidence = float(assessment.get("confidence") or assessment.get("score") or 0.0)
    actual = bool(assessment.get("actual", False))
    return record_calibration({
        "statement_id": str(assessment.get("statement_id") or assessment.get("trace_id") or ""),
        "confidence": confidence,
        "actual": actual,
        "trace_id": assessment.get("trace_id"),
        "decision_id": assessment.get("decision_id"),
    })


@router.get("/calibration/summary")
def calibration_summary(window: int = 100) -> Dict[str, Any]:
    return _calibration_store.summary(window=window)


@router.get("/calibration/records")
def calibration_records(window: int = 100) -> Dict[str, Any]:
    return {"records": _calibration_store.list_records(window=window)}
