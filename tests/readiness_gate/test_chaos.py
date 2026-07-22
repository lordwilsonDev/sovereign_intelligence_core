"""Tests for readiness gate chaos harness."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from msb_v2.core.health import ComponentHealth
from msb_v2.readiness_gate.chaos import ChaosInjector, ReadinessChaosHarness


@pytest.fixture()
def harness() -> ReadinessChaosHarness:
    return ReadinessChaosHarness()


def test_record_and_readiness_green(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy"))
    assert harness.readiness().status == "GREEN"
    assert harness.is_ready() is True


def test_degrade_moves_yellow(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy"))
    harness.record(ComponentHealth(id="b", name="B", status="healthy"))
    harness.degrade("a")
    assert harness.readiness().status == "YELLOW"
    snapshot = harness.snapshot()
    assert snapshot["status"] == "YELLOW"
    assert snapshot["sac_ready"] is True


def test_fail_moves_yellow(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy"))
    harness.record(ComponentHealth(id="b", name="B", status="healthy"))
    harness.fail("a")
    assert harness.readiness().status in {"YELLOW", "RED"}


def test_recover_restores_green(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy"))
    harness.fail("a")
    assert harness.readiness().status in {"YELLOW", "RED"}
    harness.recover("a")
    assert harness.readiness().status == "GREEN"


def test_transitions_are_captured(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy"))
    harness.degrade("a")
    harness.fail("a")
    harness.recover("a")
    actions = [t["action"] for t in harness.transitions]
    assert actions == ["degrade", "fail", "recover"]
    assert all("readiness" in t and "sac_ready" in t for t in harness.transitions)


def test_chaos_injector_upserts(harness: ReadinessChaosHarness) -> None:
    injector = ChaosInjector(harness._health)
    first = injector.degrade("x")
    assert first.status == "degraded"
    second = injector.recover("x")
    assert second.status == "healthy"
    assert harness.get_component("x") == second
