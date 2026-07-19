from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.v3.contracts import HarnessContract, register as _register_contract
from msb_v2.reasoning.calibration import CalibrationStore

from msb_v2.v3.contracts import HarnessContract
router = APIRouter(tags=["calibration"])
_calibration_store = CalibrationStore()
_register_contract(HarnessContract(route="/reasoning/calibration/record", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/reasoning/calibration/record-assessment", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/reasoning/calibration/summary", method="get", allow_anonymous=True))
_register_contract(HarnessContract(route="/reasoning/calibration/records", method="get", allow_anonymous=True))


@router.post("/calibration/record", dependencies=[Depends(require_bearer_token)])
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


@router.post("/calibration/record-assessment", dependencies=[Depends(require_bearer_token)])
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
# HCL contract registration
_register_contract(HarnessContract(route="/reasoning/calibration/calibration/record", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/reasoning/calibration/calibration/record-assessment", method="post", allow_anonymous=False))
