"""AGI Harness API — start, stop, and monitor the perpetual cognition loop."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.agi_harness.engine import AGIHarness

router = APIRouter(prefix="/agi-harness", tags=["agi-harness"])
_harness = AGIHarness()


@router.post("/start")
def start_agi() -> Dict[str, Any]:
    result = _harness.cycle()
    return result


@router.get("/status")
def agi_status() -> Dict[str, Any]:
    return {"running": _harness.running}
