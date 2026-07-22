"""Tests for SSHH harness shell."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from msb_v2.core.health import ComponentHealth
from msb_v2.sshh.harness import SovereignSelfHealingHarness


@pytest.fixture()
def harness() -> SovereignSelfHealingHarness:
    return SovereignSelfHealingHarness()


def test_record_and_get_component(harness: SovereignSelfHealingHarness) -> None:
    health = ComponentHealth(id="web-1", name="Primary Web Node", status="healthy")
    harness.record_component(health)
    assert harness.get_component("web-1") == health
    assert harness.get_component("missing") is None


def test_attempt_heal_healthy_skips(harness: SovereignSelfHealingHarness) -> None:
    harness.record_component(ComponentHealth(id="web-1", name="Primary Web Node", status="healthy"))
    assert harness.attempt_heal("web-1")["status"] == "skipped"


def test_attempt_heal_veto_when_not_ready(monkeypatch: pytest.MonkeyPatch, harness: SovereignSelfHealingHarness) -> None:
    harness.record_component(ComponentHealth(id="web-1", name="Primary Web Node", status="degraded"))
    monkeypatch.setattr(harness._gate, "is_ready", lambda: False)
    assert harness.attempt_heal("web-1")["status"] == "veto"


def test_attempt_heal_missing(harness: SovereignSelfHealingHarness) -> None:
    assert harness.attempt_heal("unknown")["status"] == "not_found"
