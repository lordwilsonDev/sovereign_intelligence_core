from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.reasoning.integrity import EventStreamStore
from msb_v2.verification.capability_registry import CapabilityRegistry
from msb_v2.verification.evidence import EvidenceEngine
from msb_v2.verification.integrity_verifier import IntegrityVerifier
from msb_v2.verification.extension import VerificationFeedbackExtension
from msb_v2.runtime.context import RuntimeContext

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter(tags=["verification"])

_stream = EventStreamStore()
_verifier = IntegrityVerifier(stream=_stream)
_registry = CapabilityRegistry()
_extension = VerificationFeedbackExtension()


class BatchVerifyRequest(BaseModel):
    decision_ids: list[str] = []


class EvaluateBody(BaseModel):
    query: str
    answer: str
    trace: Dict[str, Any] = {"confidence": 0.8, "steps": [], "tool_calls": [], "provenance": []}


class CorrectionBody(BaseModel):
    original_query: str
    original_answer: str
    corrected_answer: str
    user_id: str | None = None
    context: Dict[str, Any] = {}
    verification_report_hash: str | None = None


@router.get("/verification/integrity/trace/{trace_id}")
def verification_trace(trace_id: str) -> JSONResponse:
    return JSONResponse(_verifier.verify_trace(trace_id))


@router.get("/verification/integrity/hardware")
def verification_hardware_attestation() -> JSONResponse:
    from pathlib import Path
    from msb_v2.verification.hardware_attestation import HardwareAttestation
    try:
        binary_path = Path(__file__).resolve().parents[2] / "msb_v2" / "api" / "verification.py"
        attestation = HardwareAttestation(binary_path=binary_path).verify()
    except Exception as exc:
        attestation = {"verdict": "ERROR", "error": str(exc)}
    return JSONResponse(attestation)


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


@router.post("/verification/integrity/batch", dependencies=[Depends(require_bearer_token)])
def verification_batch(payload: BatchVerifyRequest) -> JSONResponse:
    return JSONResponse(_verifier.batch_verify(payload.decision_ids))


@router.get("/verification/benchmarks")
def verification_benchmarks() -> Dict[str, Any]:
    return {"benchmarks": list(_registry._benchmarks.keys()), "scores": _registry.get_scores()}


@router.post("/verification/benchmark/{name}/run", dependencies=[Depends(require_bearer_token)])
def verification_run_benchmark(name: str) -> Dict[str, Any]:
    try:
        score = _registry.run_benchmark(name)
    except ValueError as exc:
        return {"benchmark": name, "error": str(exc)}
    return {"benchmark": name, "score": score, "history": _registry.get_history(name)}


@router.post("/verification/evaluate", dependencies=[Depends(require_bearer_token)])
def verification_evaluate(payload: EvaluateBody) -> Dict[str, Any]:
    engine = EvidenceEngine(registry=_registry, memory_client=_extension)
    report = engine.evaluate(query=payload.query, answer=payload.answer, trace=payload.trace)
    return {
        "hash": report.compute_hash(),
        "confidence": report.confidence,
        "consistency": report.consistency,
        "novelty": report.novelty,
        "verification_score": report.verification_score,
        "falsification_score": report.falsification_score,
        "uncertainty": report.uncertainty,
        "trace_depth": report.trace_depth,
        "memory_support": report.memory_support,
        "tool_support": report.tool_support,
        "provenance": report.provenance,
    }


@router.post("/feedback/correction", dependencies=[Depends(require_bearer_token)])
def feedback_correction(payload: CorrectionBody) -> Dict[str, Any]:
    context = _extension
    context.event_bus.publish("user_correction", payload.model_dump())
    return {"status": "recorded"}


@router.get("/feedback/summary")
def feedback_summary() -> Dict[str, Any]:
    return _extension.summary()
# HCL contract registration
_register_contract(HarnessContract(route="/verification/integrity/batch", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/verification/benchmark/{name}/run", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/verification/evaluate", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/feedback/correction", method="post", allow_anonymous=False))
