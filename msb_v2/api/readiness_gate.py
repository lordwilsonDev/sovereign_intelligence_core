"""Readiness Gate API – chaos injection, failover, and telemetry validation."""

from fastapi import APIRouter
from msb_v2.readiness_gate.chaos import ReadinessChaosHarness

router = APIRouter()
_harness = ReadinessChaosHarness()


@router.get("/status")
def readiness_status():
    """Return current readiness gate state and recent chaos history."""
    return _harness.status()


@router.post("/chaos/inject")
def inject_chaos(scenario: str = "random"):
    """Trigger a specific chaos scenario."""
    result = _harness.inject(scenario)
    return {"scenario": scenario, "result": result}


@router.get("/chaos/history")
def chaos_history(limit: int = 10):
    """Return recent chaos injection results."""
    return _harness.history(limit)


@router.post("/failover/trigger")
def trigger_failover(target: str):
    """Manually trigger failover for a target component."""
    return _harness.failover(target)
