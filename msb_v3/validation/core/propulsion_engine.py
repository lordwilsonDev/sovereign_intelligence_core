from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class DiscoveryCandidate:
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
    score: float = 0.0


class PropulsionEngine:
    def __init__(self) -> None:
        self._ranked: List[DiscoveryCandidate] = []

    def evaluate(self, candidate: DiscoveryCandidate) -> DiscoveryCandidate:
        score = (
            float(candidate.novelty) * 0.2
            + float(candidate.explanatory_power) * 0.2
            + float(candidate.predictive_value) * 0.2
            + float(candidate.impact) * 0.15
            + float(candidate.leverage) * 0.15
            - float(candidate.risk) * 0.1
        )
        candidate = DiscoveryCandidate(
            **{**candidate.__dict__, "score": max(0.0, min(1.0, score))}
        )
        self._ranked.append(candidate)
        self._ranked.sort(key=lambda item: item.score, reverse=True)
        return candidate

    def ranked(self) -> List[Dict[str, Any]]:
        return [item.__dict__ for item in self._ranked]


_engine = PropulsionEngine()


def propulsion_engine() -> PropulsionEngine:
    return _engine
