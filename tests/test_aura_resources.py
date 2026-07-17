from __future__ import annotations

from msb_v2.aura.resources import ResourceBudget


def test_resource_budget_ok_initially() -> None:
    budget = ResourceBudget()
    result = budget.consume(cpu_percent=10.0, mem_mb=128.0)
    assert result["status"] == "ok"


def test_resource_budget_detects_exceeded() -> None:
    budget = ResourceBudget()
    result = budget.consume(cpu_percent=999.0)
    assert result["status"] == "exceeded"
    assert "cpu_percent" in result["exceeded"]


def test_resource_budget_snapshot_stable() -> None:
    budget = ResourceBudget()
    budget.consume(mem_mb=512.0)
    snap = budget.snapshot()
    assert snap["usage"]["mem_mb"] == 512.0
    assert snap["limits"]["mem_mb"] == 2048.0
