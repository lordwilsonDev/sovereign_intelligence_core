"""Dream Mode API — speculative self-simulation endpoints."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.dream_mode.engine import DreamMode

router = APIRouter(prefix="/dream-mode", tags=["dream-mode"])
_engine = DreamMode()


@router.post("/run")
def run_dream_cycle() -> Dict[str, Any]:
    scenario = _engine.generate_scenario()
    return _engine.simulate(scenario)


@router.get("/recent")
def recent_dreams(limit: int = 10) -> Dict[str, Any]:
    return {"dreams": _engine.recent(limit)}
