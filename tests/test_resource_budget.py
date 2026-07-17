from __future__ import annotations

from msb_v2.aura.resources import ResourceBudget


def test_circuit_breaker_opens_when_limit_exceeded() -> None:
    budget = ResourceBudget()
    assert budget.is_circuit_open() is False
    budget.consume(cpu_percent=999.0)
    assert budget.is_circuit_open() is True


def test_circuit_breaker_stays_closed_under_limit() -> None:
    budget = ResourceBudget()
    budget.consume(cpu_percent=10.0, mem_mb=128.0)
    assert budget.is_circuit_open() is False
