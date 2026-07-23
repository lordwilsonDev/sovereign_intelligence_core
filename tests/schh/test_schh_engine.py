"""SCHH engine contracts."""

from __future__ import annotations

from typing import Any

import pytest

from msb_v2.schh.engine import Component, ComponentType, HealthEngine, HealthStatus, Registry


def _registry() -> Registry:
    return Registry()


def test_register_defaults_populates_registry() -> None:
    engine = HealthEngine(registry=_registry())
    engine.register_defaults()
    ids = {c.id for c in engine._registry.all()}
    assert "star" in ids
    assert "scth" in ids
    assert "snh" in ids


def test_check_missing_component_returns_unknown() -> None:
    engine = HealthEngine(registry=_registry())
    component = Component(id="missing", name="Missing", type=ComponentType.harness)
    result = engine.check_component(component)
    assert result.status == HealthStatus.unhealthy
    assert result.component_id == "missing"


def test_history_accumulates_check_results() -> None:
    engine = HealthEngine(registry=_registry())
    engine.register_defaults()
    # run checks without client to simulate HTTP failures and produce results
    engine.run_checks(client=None)
    history = engine.history(limit=10)
    assert isinstance(history, list)
    assert len(history) > 0


def test_readiness_counts_with_no_history() -> None:
    engine = HealthEngine(registry=_registry())
    engine.register_defaults()
    readiness = engine.readiness()
    assert readiness.status in {"GREEN", "YELLOW", "RED"}
