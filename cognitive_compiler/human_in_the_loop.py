from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class AssumptionTrace:
    id: str
    description: str
    risk: str
    testability: str
    tested: bool
    validated: Optional[bool] = None


@dataclass
class HumanHandoffReport:
    summary: str
    confidence: float
    assumptions: List[AssumptionTrace] = field(default_factory=list)
    predictions: List[dict] = field(default_factory=list)
    escalation_reason: str = ""
    recommendation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "confidence": self.confidence,
            "assumptions": [a.__dict__ for a in self.assumptions],
            "predictions": self.predictions,
            "escalation_reason": self.escalation_reason,
            "recommendation": self.recommendation,
        }


class HumanInTheLoop:
    def __init__(self, escalation_thresholds: Optional[Dict[str, Any]] = None):
        self.thresholds = escalation_thresholds or {
            "min_confidence_for_auto": 0.9,
            "max_assumption_debt_auto": 2,
            "require_human_domains": ["healthcare", "legal", "safety_critical"],
        }

    def should_escalate(self, harness_output: Dict[str, Any], domain: str = "") -> Tuple[bool, str]:
        reasons: List[str] = []
        if domain in self.thresholds["require_human_domains"]:
            reasons.append(f"Domain '{domain}' requires human oversight")
        confidence = float(harness_output.get("updated_confidence") or harness_output.get("confidence") or 0.0)
        if confidence < self.thresholds["min_confidence_for_auto"]:
            reasons.append(f"Confidence {confidence:.2f} below threshold")
        assumption_debt = int(harness_output.get("assumption_debt") or harness_output.get("high_risk_untested") or 0)
        if assumption_debt > self.thresholds["max_assumption_debt_auto"]:
            reasons.append("High assumption debt")
        predictions_tested = int(harness_output.get("predictions_tested") or 0)
        if predictions_tested == 0:
            reasons.append("No predictions empirically tested")
        return bool(reasons), "; ".join(reasons)

    def generate_handoff(self, harness_output: Dict[str, Any], reason: str) -> HumanHandoffReport:
        assumptions_raw = harness_output.get("assumptions") or []
        if not assumptions_raw and harness_output.get("assumption_debt"):
            assumptions_raw = [{"id": "A-UNKNOWN", "description": "Untested assumptions detected", "risk": "HIGH", "testability": "later", "tested": False}]
        assumptions = [AssumptionTrace(**a) if isinstance(a, dict) else AssumptionTrace(id=str(a), description=str(a), risk="HIGH", testability="later", tested=False) for a in assumptions_raw]
        return HumanHandoffReport(
            summary=str(harness_output.get("summary") or harness_output.get("conclusion") or "Output flagged for human review."),
            confidence=float(harness_output.get("updated_confidence") or harness_output.get("confidence") or 0.0),
            assumptions=assumptions,
            predictions=harness_output.get("predictions") or [],
            escalation_reason=reason,
            recommendation="Review the above assumptions and predictions before proceeding.",
        )
