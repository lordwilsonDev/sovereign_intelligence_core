from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional, Tuple


class EvalResult:
    def __init__(self, name: str, passed: bool, tier: str, score: float = 0.0, details: Optional[Dict[str, Any]] = None) -> None:
        self.name = name
        self.passed = passed
        self.tier = tier
        self.score = score
        self.details = details or {}


class EvalRunner:
    def __init__(self, fixtures_dir: str = "evals/fixtures") -> None:
        self.fixtures_dir = fixtures_dir
        self.results: List[EvalResult] = []

    def run_deterministic(self, name: str, actual: Any, expected: Any, tolerance: float = 0.0) -> EvalResult:
        if tolerance:
            diff = abs(float(actual) - float(expected))
            passed = diff <= tolerance
            result = EvalResult(name, passed, "tier1_deterministic", score=1.0 if passed else 0.0, details={"diff": diff})
        else:
            passed = actual == expected
            result = EvalResult(name, passed, "tier1_deterministic", score=1.0 if passed else 0.0, details={"actual": actual, "expected": expected})
        self.results.append(result)
        return result

    def run_semantic(self, name: str, output: str, expected_intent: str, judge: Optional[Any] = None) -> EvalResult:
        if judge is None:
            result = EvalResult(name, False, "tier2_semantic", score=0.0, details={"skipped": True, "reason": "no_judge"})
            self.results.append(result)
            return result
        try:
            verdict = judge(output, expected_intent)
            passed = verdict.lower() == "yes"
            result = EvalResult(name, passed, "tier2_semantic", score=1.0 if passed else 0.0, details={"output": output, "expected_intent": expected_intent})
        except Exception as exc:
            result = EvalResult(name, False, "tier2_semantic", score=0.0, details={"error": str(exc)})
        self.results.append(result)
        return result

    def summary(self) -> Dict[str, Any]:
        tier1 = [r for r in self.results if r.tier == "tier1_deterministic"]
        tier2 = [r for r in self.results if r.tier == "tier2_semantic"]
        return {
            "total": len(self.results),
            "tier1_pass": sum(1 for r in tier1 if r.passed),
            "tier2_pass": sum(1 for r in tier2 if r.passed),
            "tier1_total": len(tier1),
            "tier2_total": len(tier2),
        }
