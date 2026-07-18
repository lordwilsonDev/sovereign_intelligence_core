from __future__ import annotations

from msb_v2.v3.constraints import Constraint, ConstraintEngine
from msb_v2.v3.memory_router import MemoryRouter
from msb_v2.v3.registry import AutonomyLevel, CapabilityNode, CapabilityRegistry, get_registry


def test_get_registry_returns_singleton_shape():
    reg = get_registry()
    assert isinstance(reg, CapabilityRegistry)
    names = [n.capability_id for n in reg.list()]
    assert "cap:brain:run" in names
    assert "cap:runtime:snapshot" in names
    assert "cap:agent:plan" in names


def test_memory_router_default_routes():
    router = MemoryRouter()
    summary = router.summary()
    assert len(summary["routes"]) == 8
    assert all("kind" in r and "tier" in r for r in summary["routes"])


def test_constraint_engine_rejects_cost():
    engine = ConstraintEngine([Constraint(name="budget", description="cap", max_cost=0.1)])
    result = engine.check({"cost_estimate": 5.0, "autonomy_level": "observe"})
    assert result["passed"] is False
    violation_names = [v["constraint"] for v in result["violations"]]
    assert "budget" in violation_names
