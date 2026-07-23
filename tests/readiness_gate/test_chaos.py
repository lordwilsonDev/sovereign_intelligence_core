"""Tests for readiness gate chaos harness."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from msb_v2.core.health import ComponentHealth
from msb_v2.core.sac_gate import ReadinessGate
from msb_v2.readiness_gate.chaos import ChaosInjector, ReadinessChaosHarness


@pytest.fixture()
def harness() -> ReadinessChaosHarness:
    return ReadinessChaosHarness()


def test_record_and_readiness_green(harness: ReadinessChaosHarness, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(harness._gate, "is_ready", lambda: True)
    harness.record(ComponentHealth(id="a", name="A", status="healthy", metadata={"critical": True}))
    assert harness.readiness().status == "GREEN"
    assert harness.is_ready() is True


def test_degrade_moves_yellow(harness: ReadinessChaosHarness, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(harness._gate, "is_ready", lambda: True)
    harness.record(ComponentHealth(id="a", name="A", status="healthy", metadata={"critical": True}))
    harness.record(ComponentHealth(id="b", name="B", status="healthy", metadata={"critical": True}))
    harness.degrade("a")
    assert harness.readiness().status == "YELLOW"
    snapshot = harness.snapshot()
    assert snapshot["status"] == "YELLOW"
    assert snapshot["sac_ready"] is True


def test_fail_moves_yellow(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy", metadata={"critical": True}))
    harness.record(ComponentHealth(id="b", name="B", status="healthy", metadata={"critical": True}))
    harness.fail("a")
    assert harness.readiness().status in {"YELLOW", "RED"}


def test_recover_restores_green(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy", metadata={"critical": True}))
    harness.fail("a")
    assert harness.readiness().status in {"YELLOW", "RED"}
    harness.recover("a")
    assert harness.readiness().status == "GREEN"


def test_transitions_are_captured(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy", metadata={"critical": True}))
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


def test_multiple_degrades_accumulate(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy", metadata={"critical": True}))
    harness.record(ComponentHealth(id="b", name="B", status="healthy", metadata={"critical": True}))
    harness.record(ComponentHealth(id="c", name="C", status="healthy", metadata={"critical": True}))
    harness.degrade("a")
    harness.degrade("b")
    assert harness.readiness().degraded_count == 2
    assert harness.readiness().status == "YELLOW"


def test_fail_non_critical_does_not_trigger_red(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy", metadata={"critical": False}))
    harness.fail("a")
    assert harness.readiness().status == "YELLOW"


def test_history_limit_respects_max(harness: ReadinessChaosHarness) -> None:
    harness.record(ComponentHealth(id="a", name="A", status="healthy", metadata={"critical": True}))
    for i in range(25):
        harness.degrade(f"c{i}")
    assert len(harness.history(limit=10)) == 10


def test_sac_ready_reflects_gate(harness: ReadinessChaosHarness, monkeypatch: pytest.MonkeyPatch) -> None:
    gate = ReadinessGate()
    monkeypatch.setattr(gate, "is_ready", lambda: True)
    harness._gate = gate
    assert harness.is_ready() is True
    snapshot = harness.snapshot()
    assert snapshot["sac_ready"] is True
