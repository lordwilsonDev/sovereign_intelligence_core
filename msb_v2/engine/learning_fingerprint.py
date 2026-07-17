from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class LearningFingerprint:
    history: list[Tuple[str, str]] = field(default_factory=list)

    def record(self, goal: str, hypothesis: str) -> None:
        item = (goal, hypothesis)
        if item not in self.history:
            self.history.append(item)

    def is_novel(self, goal: str, hypothesis: str) -> bool:
        return (goal, hypothesis) not in self.history
