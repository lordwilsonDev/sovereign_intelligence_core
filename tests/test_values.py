from __future__ import annotations

import pytest

from msb_v2.values.registry import ValueRegistry
from msb_v2.values.types import ValuePreference


def test_value_registry_register_and_resolve() -> None:
    registry = ValueRegistry()
    registry.register(ValuePreference(name="safety", weight=0.9, priority=10, immutable=True))
    registry.register(ValuePreference(name="speed", weight=0.6, priority=4))
    result = registry.resolve(["speed", "safety"])
    assert result.chosen == "safety"
    assert result.outcome == "selected safety"
    assert "speed" in result.rejected


def test_value_registry_immutable_reject() -> None:
    registry = ValueRegistry()
    registry.register(ValuePreference(name="truthfulness", weight=1.0, priority=10, immutable=True))
    with pytest.raises(PermissionError):
        registry.register(ValuePreference(name="truthfulness", weight=0.5, priority=1))


def test_value_registry_empty_candidates_raises() -> None:
    registry = ValueRegistry()
    with pytest.raises(ValueError):
        registry.resolve([])


def test_value_registry_unknown_values_raises() -> None:
    registry = ValueRegistry()
    with pytest.raises(ValueError):
        registry.resolve(["nonexistent"])
