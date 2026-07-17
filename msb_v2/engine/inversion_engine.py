from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence


@dataclass
class InversionResult:
    original: str
    inversion: str
    consequences: list[str] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    score: float = 0.0
    scored_output: dict[str, Any] = field(default_factory=dict)
    impact: float = 0.5
    confidence: float = 0.5


class InversionEngine:
    def invert(self, assumption: str) -> InversionResult:
        return self._build(assumption)

    def invert_many(self, assumption: str) -> Sequence[InversionResult]:
        return [self._build(assumption)]

    @staticmethod
    def _build(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result
