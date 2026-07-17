from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ValuePreference:
    name: str
    weight: float = 0.5
    priority: int = 0
    immutable: bool = False

    def __post_init__(self) -> None:
        if self.weight < 0.0 or self.weight > 1.0:
            raise ValueError(f"weight must be between 0.0 and 1.0; got {self.weight}")
        if self.priority < 0:
            raise ValueError(f"priority must be non-negative; got {self.priority}")


@dataclass(frozen=True)
class ValueConflict:
    values: List[str]
    outcome: str
    resolution: str
    chosen: str
    rejected: List[str] = field(default_factory=list)


class ValueRegistry:
    def __init__(self) -> None:
        self._preferences: Dict[str, ValuePreference] = {}

    def register(self, preference: ValuePreference) -> None:
        if preference.name in self._preferences and self._preferences[preference.name].immutable:
            raise PermissionError(f"immutable value: {preference.name}")
        self._preferences[preference.name] = preference

    def get(self, name: str) -> Optional[ValuePreference]:
        return self._preferences.get(name)

    def resolve(self, candidates: List[str]) -> ValueConflict:
        if not candidates:
            raise ValueError("candidates must not be empty")
        known = [name for name in candidates if name in self._preferences]
        if not known:
            raise ValueError("no candidate values are registered")
        ranked = sorted(known, key=lambda name: (self._preferences[name].priority, self._preferences[name].weight), reverse=True)
        chosen = ranked[0]
        rejected = [name for name in ranked[1:]]
        return ValueConflict(
            values=list(candidates),
            outcome=f"selected {chosen}",
            resolution="chose highest priority/weight value",
            chosen=chosen,
            rejected=rejected,
        )

    def list_values(self) -> List[ValuePreference]:
        return list(self._preferences.values())
