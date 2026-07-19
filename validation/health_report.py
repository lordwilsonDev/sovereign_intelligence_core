from __future__ import annotations

from typing import Any, Dict


class HealthReport:
    @staticmethod
    def build(validator: Dict[str, Any]) -> Dict[str, Any]:
        passed = validator.get("passed", [])
        failed = validator.get("failed", [])
        score = validator.get("score", 0.0)
        grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "F"
        sections = {
            "health": [p for p in passed if "/health" in p],
            "memory": [p for p in passed if "/memory" in p],
            "reasoning": [p for p in passed if "/reasoning" in p or "/cognitive" in p],
            "agents": [p for p in passed if "/agent" in p or "/desktop" in p],
            "evolution": [p for p in passed if "/evolution" in p],
            "verification": [p for p in passed if "/verification" in p],
        }
        return {
            "msb_integrity_score": score,
            "grade": grade,
            "sections": sections,
            "passed": passed,
            "failed": failed,
        }
