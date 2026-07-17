from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import List


@dataclass
class GoalBinding:
    goal: str
    constraints: List[str] = field(default_factory=list)
    locked: bool = False

    def checksum(self) -> str:
        raw = f"{self.goal}|{'|'.join(self.constraints)}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]

    @classmethod
    def create(cls, goal: str, constraints: List[str] | None = None) -> "GoalBinding":
        return cls(goal=goal, constraints=constraints or [])

    def lock(self) -> None:
        self.locked = True
