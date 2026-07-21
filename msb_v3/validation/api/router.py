from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel


class RunValidationRequest(BaseModel):
    system: str
    domain: str
    claim: str


class ValidationResultResponse(BaseModel):
    subject: str
    confidence: float
    evidence_score: float
    falsification_risk: float
    assumption_count: int
    unresolved_questions: list[str]
    recommendations: list[str]
    evolution_required: bool


router = APIRouter()


@router.post("/run")
def run_validation(payload: RunValidationRequest) -> ValidationResultResponse:
    from msb_v3.validation.core.scoring import scoring_engine
    result = scoring_engine().score(
        subject=f"{payload.system}:{payload.claim}",
        confidence=0.8,
        evidence=0.9,
        assumptions=3,
        falsification_risk=0.4,
    )
    return ValidationResultResponse(
        subject=result.subject,
        confidence=result.confidence,
        evidence_score=result.evidence_score,
        falsification_risk=result.falsification_risk,
        assumption_count=result.assumption_count,
        unresolved_questions=result.unresolved_questions,
        recommendations=result.recommendations,
        evolution_required=result.evolution_required,
    )
