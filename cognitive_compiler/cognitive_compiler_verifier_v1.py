from __future__ import annotations

import importlib.util
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class VerificationReport:
    ok: bool
    stage: str
    risk: float
    issues: list[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)


class CognitiveCompilerVerifier:
    def __init__(self, *, risk_threshold: float = 0.7) -> None:
        self.risk_threshold = float(risk_threshold)
        self._available = self._probe_axiom_evaluator()

    def verify(self, result: Dict[str, Any], context: Dict[str, Any]) -> Optional[VerificationReport]:
        if not self._available:
            return None
        primary_output = ((result or {}).get("primary_output") or {})
        if not primary_output:
            return None
        risk = self._estimate_risk(primary_output, context)
        issues: list[str] = []
        if risk >= self.risk_threshold:
            issues.append(f"high_risk:{risk:.2f}")
        evidence = {
            "ax_defect_count": sum(1 for k in primary_output.keys() if k.startswith("error")),
        }
        return VerificationReport(ok=risk < self.risk_threshold, stage="axiom", risk=round(risk, 2), issues=issues, evidence=evidence)

    def _probe_axiom_evaluator(self) -> bool:
        try:
            spec = importlib.util.find_spec("cognitive_compiler.axiom_evaluator_v1")
            return spec is not None
        except Exception:
            return False

    def _estimate_risk(self, payload: Dict[str, Any], context: Dict[str, Any]) -> float:
        try:
            if "error" in payload or payload.get("ok") is False:
                return 0.9
            conf = float(((context or {}).get("confidence") or 0.0))
            base = max(0.0, min(1.0, 1.0 - conf))
            return min(1.0, base + 0.05)
        except Exception:
            return 0.8
