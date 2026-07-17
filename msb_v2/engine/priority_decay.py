from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class PriorityScore:
    label: str
    urgency: float = 0.5
    impact: float = 0.5
    confidence: float = 0.5

    def composite(self) -> float:
        return (self.urgency * 0.4) + (self.impact * 0.4) + (self.confidence * 0.2)


class PriorityDecay:
    def __init__(self) -> None:
        self.scores: List[PriorityScore] = []

    def add(self, score: PriorityScore) -> None:
        self.scores.append(score)

    def ranked(self) -> List[tuple[str, float]]:
        return sorted([(s.label, s.composite()) for s in self.scores], key=lambda x: x[1], reverse=True)
