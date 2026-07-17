from __future__ import annotations


from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from msb_v2.verification.integrity_verifier import IntegrityVerifier
from msb_v2.reasoning.integrity import EventStreamStore

router = APIRouter(tags=["verification"])

_stream = EventStreamStore()
_verifier = IntegrityVerifier(stream=_stream)


class BatchVerifyRequest(BaseModel):
    decision_ids: list[str] = []


@router.get("/verification/integrity/trace/{trace_id}")
def verification_trace(trace_id: str) -> JSONResponse:
    return JSONResponse(_verifier.verify_trace(trace_id))


@router.get("/verification/integrity/decision/{decision_id}")
def verification_decision(decision_id: str) -> JSONResponse:
    check = _verifier.verify_decision(decision_id)
    return JSONResponse(
        {
            "decision_id": check.decision_id,
            "valid": check.valid,
            "broken_at": check.broken_at,
            "expected_hash": check.expected_hash,
            "actual_hash": check.actual_hash,
            "continuity": check.continuity,
        }
    )


@router.post("/verification/integrity/batch")
def verification_batch(payload: BatchVerifyRequest) -> JSONResponse:
    return JSONResponse(_verifier.batch_verify(payload.decision_ids))
