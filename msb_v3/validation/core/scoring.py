from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ValidationResult:
    subject: str
    confidence: float
    evidence_score: float
    falsification_risk: float
    assumption_count: int
    unresolved_questions: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    evolution_required: bool = False


class ValidationScoringEngine:
    def __init__(self) -> None:
        self._history: List[ValidationResult] = []

    def score(self, subject: str, *, confidence: float, evidence: float, assumptions: int, falsification_risk: float) -> ValidationResult:
        if assumptions <= 0:
            assumption_debt = 0.0
        else:
            assumption_debt = 1.0 / float(assumptions)
        predictive_accuracy = max(0.0, min(1.0, evidence))
        falsification_resistance = max(0.0, min(1.0, 1.0 - falsification_risk))
        ras = (predictive_accuracy * falsification_resistance) / (assumption_debt if assumption_debt > 0 else 1e-6)
        ras = max(0.0, min(1.0, ras))
        result = ValidationResult(
            subject=subject,
            confidence=float(max(0.0, min(1.0, confidence))),
            evidence_score=predictive_accuracy,
            falsification_risk=float(max(0.0, min(1.0, falsification_risk))),
            assumption_count=int(assumptions),
            evolution_required=ras < 0.5,
        )
        self._history.append(result)
        return result

    def history(self) -> List[Dict[str, Any]]:
        return [self._serialize(r) for r in self._history]

    @staticmethod
    def _serialize(result: ValidationResult) -> Dict[str, Any]:
        return {
            "subject": result.subject,
            "confidence": result.confidence,
            "evidence_score": result.evidence_score,
            "falsification_risk": result.falsification_risk,
            "assumption_count": result.assumption_count,
            "unresolved_questions": result.unresolved_questions,
            "recommendations": result.recommendations,
            "evolution_required": result.evolution_required,
        }


_engine = ValidationScoringEngine()


def scoring_engine() -> ValidationScoringEngine:
    return _engine
