from __future__ import annotations

from msb_v2.values.types import ValueConflict, ValuePreference


class ValueRegistry:
    def __init__(self) -> None:
        self._preferences: dict[str, ValuePreference] = {}

    def register(self, preference: ValuePreference) -> None:
        if preference.name in self._preferences and self._preferences[preference.name].immutable:
            raise PermissionError(f"immutable value: {preference.name}")
        self._preferences[preference.name] = preference

    def get(self, name: str) -> ValuePreference | None:
        return self._preferences.get(name)

    def resolve(self, candidates: list[str]) -> ValueConflict:
        if not candidates:
            raise ValueError("candidates must not be empty")
        known = [name for name in candidates if name in self._preferences]
        if not known:
            raise ValueError("no candidate values are registered")
        ranked = sorted(known, key=lambda name: (self._preferences[name].priority, self._preferences[name].weight), reverse=True)
        chosen = ranked[0]
        return ValueConflict(
            values=list(candidates),
            outcome=f"selected {chosen}",
            resolution="chose highest priority/weight value",
            chosen=chosen,
            rejected=ranked[1:],
        )

    def list_values(self) -> list[ValuePreference]:
        return list(self._preferences.values())
