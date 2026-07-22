from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


@dataclass(frozen=True)
class RiskAssessment:
    level: RiskLevel
    score: float
    reasons: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.value,
            "score": self.score,
            "reasons": list(self.reasons),
            "context": dict(self.context),
            "timestamp": self.timestamp,
        }


class RiskEvaluator:
    BLAST_RADIUS_THRESHOLD = 0.5
    FATIGUE_THRESHOLD = 0.6
    FRUSTRATION_THRESHOLD = 0.7
    SPECIFICITY_THRESHOLD = 0.4

    def _score_blast_radius(self, blast_analysis, score, reasons, context):
        if not blast_analysis:
            return score
        blast_score = float(blast_analysis.get("score", 0.0))
        context["blast_score"] = blast_score
        if blast_score > self.BLAST_RADIUS_THRESHOLD:
            reasons.append(f"Blast radius elevated: {blast_analysis.get('score')}")
            score += 0.4
        return score

    def _score_cognitive_state(self, cognitive_state, score, reasons, context):
        if not cognitive_state:
            return score
        fatigue = float(getattr(cognitive_state, 'fatigue', 0.0))
        frustration = float(getattr(cognitive_state, 'frustration', 0.0))
        context["fatigue"] = fatigue
        context["frustration"] = frustration
        if fatigue > self.FATIGUE_THRESHOLD:
            reasons.append(f"Operator fatigue: {fatigue:.0%}")
            score += 0.3
        if frustration > self.FRUSTRATION_THRESHOLD:
            reasons.append(f"Operator frustration: {frustration:.0%}")
            score += 0.2
        return score

    def _score_intent(self, intent, score, reasons):
        if hasattr(intent, 'is_destructive') and intent.is_destructive:
            reasons.append("Destructive action")
            score += 0.3
        if hasattr(intent, 'specificity') and intent.specificity < self.SPECIFICITY_THRESHOLD:
            reasons.append("Low specificity")
            score += 0.2
        return score

    def _derive_level(self, score):
        if score >= 0.8:
            return RiskLevel.critical
        elif score >= 0.6:
            return RiskLevel.high
        elif score >= 0.3:
            return RiskLevel.medium
        return RiskLevel.low

    def evaluate(self, intent: Any, cognitive_state: Any = None, blast_analysis: Dict[str, Any] = None, temporal_context: Any = None) -> RiskAssessment:
        score = 0.0
        reasons: List[str] = []
        context: Dict[str, Any] = {}

        score = self._score_blast_radius(blast_analysis, score, reasons, context)
        score = self._score_cognitive_state(cognitive_state, score, reasons, context)
        score = self._score_intent(intent, score, reasons)

        score = min(1.0, max(0.0, score))
        level = self._derive_level(score)

        return RiskAssessment(level=level, score=score, reasons=reasons, context=context)
