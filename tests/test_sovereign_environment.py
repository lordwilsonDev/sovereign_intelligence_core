from __future__ import annotations

from msb_v2.environment.sovereign_environment import SovereignEnvironment


def test_sovereign_environment_initializes_active() -> None:
    env = SovereignEnvironment()
    status = env.get_status()
    assert status.phase == "Phase 7"
    assert status.env_status == "active"
    assert status.last_error is None


def test_sovereign_environment_snapshot_shape() -> None:
    env = SovereignEnvironment()
    snapshot = env.snapshot()
    assert snapshot["phase"] == "Phase 7"
    assert snapshot["status"] == "active"
    assert "components" in snapshot
    for key in ["runtime", "memory", "verification", "evolution", "agent", "studio"]:
        assert snapshot["components"][key] == "active"
