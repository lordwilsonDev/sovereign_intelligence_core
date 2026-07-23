"""Tests for SOH harness shell."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from msb_v2.core.health import ComponentHealth
from msb_v2.soh.harness import SystemObservabilityHarness


@pytest.fixture()
def harness() -> SystemObservabilityHarness:
    return SystemObservabilityHarness()


def test_record_and_get_component(harness: SystemObservabilityHarness) -> None:
    health = ComponentHealth(id="db-primary", name="Primary Database", status="healthy", metadata={"tier": "critical"})
    harness.record_component(health)
    assert harness.get_component("db-primary") == health
    assert harness.get_component("missing") is None


def test_empty_readiness_is_healthy(harness: SystemObservabilityHarness) -> None:
    readiness = harness.readiness()
    assert readiness.status == "GREEN"
    assert readiness.healthy_count == 0
    assert readiness.degraded_count == 0
    assert readiness.unhealthy_count == 0


def test_snapshot_contract(harness: SystemObservabilityHarness) -> None:
    harness.record_component(ComponentHealth(id="a", name="A", status="healthy"))
    harness.record_component(ComponentHealth(id="b", name="B", status="degraded"))
    snapshot = harness.snapshot()
    assert snapshot == {
        "readiness": "YELLOW",
        "healthy_count": 1,
        "degraded_count": 1,
        "unhealthy_count": 0,
        "critical_unhealthy": [],
        "updated_at": snapshot["updated_at"],
        "sac_ready": harness.is_ready(),
    }
    assert snapshot["updated_at"]
