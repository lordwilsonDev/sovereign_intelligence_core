from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from msb_v2.engine.rcoh import RCOH, RCOHState
from msb_v2.engine.rcoh_persistence import RCOHPersistence

router = APIRouter()
_persistence = RCOHPersistence()


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class StartCycleRequest(BaseModel):
    context_summary: str = ""
    goals: list[str] = []
    max_iterations: int = 10
    confidence_threshold: float = 0.8
mutants_x__state_to_dict__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__state_to_dict__mutmut)
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


def x__state_to_dict__mutmut_orig(state: RCOHState) -> dict:
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


def x__state_to_dict__mutmut_1(state: RCOHState) -> dict:
    return {
        "XXcycle_idXX": state.cycle_id,
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


def x__state_to_dict__mutmut_2(state: RCOHState) -> dict:
    return {
        "CYCLE_ID": state.cycle_id,
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


def x__state_to_dict__mutmut_3(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "XXphaseXX": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_4(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "PHASE": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_5(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "XXconfidenceXX": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_6(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "CONFIDENCE": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_7(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "XXiterationXX": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_8(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "ITERATION": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_9(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "XXmax_iterationsXX": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_10(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "MAX_ITERATIONS": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_11(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "XXcontext_summaryXX": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_12(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "CONTEXT_SUMMARY": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_13(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "XXgoalsXX": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_14(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "GOALS": state.goals,
        "started_at": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_15(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "XXstarted_atXX": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_16(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "STARTED_AT": state.started_at,
        "updated_at": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_17(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "XXupdated_atXX": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_18(state: RCOHState) -> dict:
    return {
        "cycle_id": state.cycle_id,
        "phase": state.current_phase.value,
        "confidence": state.confidence,
        "iteration": state.iteration,
        "max_iterations": state.max_iterations,
        "context_summary": state.context_summary,
        "goals": state.goals,
        "started_at": state.started_at,
        "UPDATED_AT": state.updated_at,
        "stop_reason": state.stop_reason,
    }


def x__state_to_dict__mutmut_19(state: RCOHState) -> dict:
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
        "XXstop_reasonXX": state.stop_reason,
    }


def x__state_to_dict__mutmut_20(state: RCOHState) -> dict:
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
        "STOP_REASON": state.stop_reason,
    }

mutants_x__state_to_dict__mutmut['_mutmut_orig'] = x__state_to_dict__mutmut_orig # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_1'] = x__state_to_dict__mutmut_1 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_2'] = x__state_to_dict__mutmut_2 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_3'] = x__state_to_dict__mutmut_3 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_4'] = x__state_to_dict__mutmut_4 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_5'] = x__state_to_dict__mutmut_5 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_6'] = x__state_to_dict__mutmut_6 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_7'] = x__state_to_dict__mutmut_7 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_8'] = x__state_to_dict__mutmut_8 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_9'] = x__state_to_dict__mutmut_9 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_10'] = x__state_to_dict__mutmut_10 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_11'] = x__state_to_dict__mutmut_11 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_12'] = x__state_to_dict__mutmut_12 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_13'] = x__state_to_dict__mutmut_13 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_14'] = x__state_to_dict__mutmut_14 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_15'] = x__state_to_dict__mutmut_15 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_16'] = x__state_to_dict__mutmut_16 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_17'] = x__state_to_dict__mutmut_17 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_18'] = x__state_to_dict__mutmut_18 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_19'] = x__state_to_dict__mutmut_19 # type: ignore # mutmut generated
mutants_x__state_to_dict__mutmut['x__state_to_dict__mutmut_20'] = x__state_to_dict__mutmut_20 # type: ignore # mutmut generated


# NOTE: /cycles/recent MUST be declared before /{cycle_id} so FastAPI
# doesn't swallow "cycles" as a cycle_id path parameter.
@router.get("/cycles/recent")
def recent_cycles(limit: int = 20) -> dict:
    cycles = _persistence.recent(limit=limit)
    return {"cycles": cycles}


@router.post("/start")
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
