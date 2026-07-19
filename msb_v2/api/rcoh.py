from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.engine.rcoh import RCOH, RCOHState
from msb_v2.engine.rcoh_persistence import RCOHPersistence

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter()
_persistence = RCOHPersistence()


class StartCycleRequest(BaseModel):
    context_summary: str = ""
    goals: list[str] = []
    max_iterations: int = 10
    confidence_threshold: float = 0.8


def _state_to_dict(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


# NOTE: /cycles/recent MUST be declared before /{cycle_id} so FastAPI
# doesn't swallow "cycles" as a cycle_id path parameter.
@router.get("/cycles/recent")
def recent_cycles(limit: int = 20) -> dict:
    cycles = _persistence.recent(limit=limit)
    return {"cycles": cycles}


@router.post("/start", dependencies=[Depends(require_bearer_token)])
def start_cycle(req: StartCycleRequest = StartCycleRequest()) -> dict:
    state = RCOHState(
        cycle_id=RCOH()._new_cycle_id(),
        context_summary=req.context_summary,
        goals=req.goals,
        max_iterations=req.max_iterations,
        confidence_threshold=req.confidence_threshold,
    )
    engine = RCOH(state=state)
    final_state = engine.run(max_iterations=req.max_iterations)
    _persistence.save(final_state)
    return {"status": "ok", "cycle_id": final_state.cycle_id, "cycle": _state_to_dict(final_state)}


@router.get("/{cycle_id}")
def get_cycle(cycle_id: str) -> dict:
    state = _persistence.load(cycle_id)
    if state is None:
        raise HTTPException(status_code=404, detail=f"Cycle '{cycle_id}' not found")
    return {"cycle_id": state.cycle_id, "phase": state.current_phase.value, "cycle": _state_to_dict(state)}
# HCL contract registration
_register_contract(HarnessContract(route="/rcoh/start", method="post", allow_anonymous=False))
