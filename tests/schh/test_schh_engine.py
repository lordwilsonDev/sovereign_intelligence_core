from __future__ import annotations

from typing import Any

from msb_v2.schh.engine import HealthEngine, Registry


def _engine() -> HealthEngine:
    return HealthEngine(registry=Registry())


def test_register_defaults_populates_registry():
    engine = _engine()
    engine.register_defaults()
    components = engine._registry.all()
    assert any(c.id == "star" for c in components)
    assert any(c.id == "scth" for c in components)


def test_check_component_missing_returns_unhealthy():
    engine = _engine()
    result = engine.check_component(_component("missing", "missing"))
    assert result.status.value == "unhealthy"


def test_readiness_counts_unknown_when_no_history():
    engine = _engine()
    engine.register_defaults()
    readiness = engine.readiness()
    assert readiness.status == "GREEN"


def _component(id: str, name: str) -> Any:
    from msb_v2.schh.engine import Component
    return Component(id=id, name=name)
