from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Contradiction:
    a: str
    b: str
    pattern: str


class ContradictionDetector:
    def __init__(self) -> None:
        self._patterns: List[Contradiction] = [
            Contradiction("A causes B", "B correlates with A", "causality reversal"),
            Contradiction("always", "never", "absolute conflict"),
            Contradiction("must", "must not", "direct negation"),
        ]

    def inspect(self, text: str) -> List[Dict[str, str]]:
        findings: List[Dict[str, str]] = []
        lower = text.lower()
        for pattern in self._patterns:
            present = [term for term in [pattern.a, pattern.b] if term.lower() in lower]
            if len(present) == 2:
                findings.append({
                    "pattern": pattern.pattern,
                    "terms": [pattern.a, pattern.b],
                    "detail": f"Both '{pattern.a}' and '{pattern.b}' appear in the same context.",
                })
        return findings


_detector = ContradictionDetector()


def detector() -> ContradictionDetector:
    return _detector
