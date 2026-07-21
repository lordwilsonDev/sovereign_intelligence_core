from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Assumption:
    statement: str
    confidence: str = "medium"
    evidence: List[str] = field(default_factory=list)


class AssumptionMiner:
    def __init__(self) -> None:
        self._prefixes = [
            "because",
            "since",
            "as",
            "due to",
            "therefore",
            "thus",
            "hence",
        ]

    def mine(self, text: str) -> List[Assumption]:
        statements = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        results: List[Assumption] = []
        for statement in statements:
            lower = statement.lower()
            if any(lower.startswith(prefix) or f" {prefix} " in lower for prefix in self._prefixes):
                results.append(Assumption(statement=statement))
        return results


_miner = AssumptionMiner()


def miner() -> AssumptionMiner:
    return _miner
