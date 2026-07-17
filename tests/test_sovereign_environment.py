from __future__ import annotations

import pytest

from msb_v2.environment.sovereign_environment import Phase7State, SovereignEnvironment


def test_sovereign_environment_initializes_active() -> None:
    env = SovereignEnvironment()
    status = env.get_status()
    assert status.phase == "Phase 7"
    assert status.env_status == Phase7State.ACTIVE.value
    assert status.last_error is None
    assert status.shutdown_reason is None


def test_sovereign_environment_snapshot_shape() -> None:
    env = SovereignEnvironment()
    snapshot = env.snapshot()
    assert snapshot["phase"] == "Phase 7"
    assert snapshot["status"] == Phase7State.ACTIVE.value
    assert "components" in snapshot
    for key in ["runtime", "memory", "verification", "evolution", "agent", "studio"]:
        assert snapshot["components"][key] == "active"


def test_sovereign_environment_transitions() -> None:
    env = SovereignEnvironment()
    assert env.get_status().env_status == Phase7State.ACTIVE.value

    degraded = env.mark_degraded("test failure")
    assert env.get_status().env_status == Phase7State.DEGRADED.value
    assert env.get_status().last_error == "test failure"

    snapshot = env.startup()
    assert snapshot["status"] == Phase7State.ACTIVE.value
    assert env.get_status().env_status == Phase7State.ACTIVE.value

    shutdown = env.shutdown(reason="maintenance")
    assert env.get_status().env_status == Phase7State.STOPPED.value
    assert env.get_status().shutdown_reason == "maintenance"
