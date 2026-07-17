from __future__ import annotations

from msb_v2.engine.goal_binding import GoalBinding


def test_goal_binding_checksum_is_deterministic() -> None:
    binding = GoalBinding(goal="ship service", constraints=["offline", "local"])
    first = binding.checksum()
    second = GoalBinding(goal="ship service", constraints=["offline", "local"]).checksum()
    assert first == second
    assert len(first) == 12


def test_goal_binding_lifetime_is_novel_until_recorded() -> None:
    binding = GoalBinding(goal="probe shadow", constraints=["private"])
    assert binding.locked is False
    binding.lock()
    assert binding.locked is True


def test_create_factory_sets_constraints_list() -> None:
    binding = GoalBinding.create("probe market", constraints=["risk-aware"])
    assert binding.constraints == ["risk-aware"]
    assert binding.checksum()
