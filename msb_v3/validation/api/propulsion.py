from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel


class CandidateRequest(BaseModel):
    id: str
    problem: str
    assumption: str
    inverse: str
    novelty: float = 0.0
    explanatory_power: float = 0.0
    predictive_value: float = 0.0
    verification_cost: float = 1.0
    impact: float = 0.0
    cost: float = 1.0
    complexity: float = 1.0
    risk: float = 1.0
    timing: float = 1.0
    leverage: float = 1.0


router = APIRouter()


@router.post("/propulsion/evaluate")
def evaluate_candidate(payload: CandidateRequest) -> Dict[str, Any]:
    from msb_v3.validation.core.propulsion_engine import DiscoveryCandidate, propulsion_engine
    engine = propulsion_engine()
    candidate = DiscoveryCandidate(
        id=payload.id,
        problem=payload.problem,
        assumption=payload.assumption,
        inverse=payload.inverse,
        novelty=payload.novelty,
        explanatory_power=payload.explanatory_power,
        predictive_value=payload.predictive_value,
        verification_cost=payload.verification_cost,
        impact=payload.impact,
        cost=payload.cost,
        complexity=payload.complexity,
        risk=payload.risk,
        timing=payload.timing,
        leverage=payload.leverage,
    )
    result = engine.evaluate(candidate)
    serialized = {
        "id": result.id,
        "problem": result.problem,
        "assumption": result.assumption,
        "inverse": result.inverse,
        "score": float(result.score or 0.0),
        "novelty": float(result.novelty),
        "explanatory_power": float(result.explanatory_power),
        "predictive_value": float(result.predictive_value),
        "impact": float(result.impact),
        "cost": float(result.cost),
        "complexity": float(result.complexity),
        "risk": float(result.risk),
        "timing": float(result.timing),
        "leverage": float(result.leverage),
    }
    return {"scored": serialized, "ranked": engine.ranked()}
