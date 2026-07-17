from __future__ import annotations

import time
from typing import Any

from msb_v2.aura.models import Event, EventPhase, State


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_log_event__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_log_event__mutmut)
def log_event(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = Event(session_id=state.session_id, phase=phase, payload=payload or {})
    return evt


def x_log_event__mutmut_orig(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = Event(session_id=state.session_id, phase=phase, payload=payload or {})
    return evt


def x_log_event__mutmut_1(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = None
    return evt


def x_log_event__mutmut_2(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = Event(session_id=None, phase=phase, payload=payload or {})
    return evt


def x_log_event__mutmut_3(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = Event(session_id=state.session_id, phase=None, payload=payload or {})
    return evt


def x_log_event__mutmut_4(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = Event(session_id=state.session_id, phase=phase, payload=None)
    return evt


def x_log_event__mutmut_5(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = Event(phase=phase, payload=payload or {})
    return evt


def x_log_event__mutmut_6(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = Event(session_id=state.session_id, payload=payload or {})
    return evt


def x_log_event__mutmut_7(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = Event(session_id=state.session_id, phase=phase, )
    return evt


def x_log_event__mutmut_8(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = Event(session_id=state.session_id, phase=phase, payload=payload and {})
    return evt

mutants_x_log_event__mutmut['_mutmut_orig'] = x_log_event__mutmut_orig # type: ignore # mutmut generated
mutants_x_log_event__mutmut['x_log_event__mutmut_1'] = x_log_event__mutmut_1 # type: ignore # mutmut generated
mutants_x_log_event__mutmut['x_log_event__mutmut_2'] = x_log_event__mutmut_2 # type: ignore # mutmut generated
mutants_x_log_event__mutmut['x_log_event__mutmut_3'] = x_log_event__mutmut_3 # type: ignore # mutmut generated
mutants_x_log_event__mutmut['x_log_event__mutmut_4'] = x_log_event__mutmut_4 # type: ignore # mutmut generated
mutants_x_log_event__mutmut['x_log_event__mutmut_5'] = x_log_event__mutmut_5 # type: ignore # mutmut generated
mutants_x_log_event__mutmut['x_log_event__mutmut_6'] = x_log_event__mutmut_6 # type: ignore # mutmut generated
mutants_x_log_event__mutmut['x_log_event__mutmut_7'] = x_log_event__mutmut_7 # type: ignore # mutmut generated
mutants_x_log_event__mutmut['x_log_event__mutmut_8'] = x_log_event__mutmut_8 # type: ignore # mutmut generated
mutants_x_update_state__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_update_state__mutmut)
def update_state(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context or {})
    if "goal" in context:
        state.current_goal = str(context["goal"])
    return state


def x_update_state__mutmut_orig(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context or {})
    if "goal" in context:
        state.current_goal = str(context["goal"])
    return state


def x_update_state__mutmut_1(state: State, step: str, **context: Any) -> State:
    state.step = 1
    state.context.update(context or {})
    if "goal" in context:
        state.current_goal = str(context["goal"])
    return state


def x_update_state__mutmut_2(state: State, step: str, **context: Any) -> State:
    state.step -= 1
    state.context.update(context or {})
    if "goal" in context:
        state.current_goal = str(context["goal"])
    return state


def x_update_state__mutmut_3(state: State, step: str, **context: Any) -> State:
    state.step += 2
    state.context.update(context or {})
    if "goal" in context:
        state.current_goal = str(context["goal"])
    return state


def x_update_state__mutmut_4(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(None)
    if "goal" in context:
        state.current_goal = str(context["goal"])
    return state


def x_update_state__mutmut_5(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context and {})
    if "goal" in context:
        state.current_goal = str(context["goal"])
    return state


def x_update_state__mutmut_6(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context or {})
    if "XXgoalXX" in context:
        state.current_goal = str(context["goal"])
    return state


def x_update_state__mutmut_7(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context or {})
    if "GOAL" in context:
        state.current_goal = str(context["goal"])
    return state


def x_update_state__mutmut_8(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context or {})
    if "goal" not in context:
        state.current_goal = str(context["goal"])
    return state


def x_update_state__mutmut_9(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context or {})
    if "goal" in context:
        state.current_goal = None
    return state


def x_update_state__mutmut_10(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context or {})
    if "goal" in context:
        state.current_goal = str(None)
    return state


def x_update_state__mutmut_11(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context or {})
    if "goal" in context:
        state.current_goal = str(context["XXgoalXX"])
    return state


def x_update_state__mutmut_12(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context or {})
    if "goal" in context:
        state.current_goal = str(context["GOAL"])
    return state

mutants_x_update_state__mutmut['_mutmut_orig'] = x_update_state__mutmut_orig # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_1'] = x_update_state__mutmut_1 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_2'] = x_update_state__mutmut_2 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_3'] = x_update_state__mutmut_3 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_4'] = x_update_state__mutmut_4 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_5'] = x_update_state__mutmut_5 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_6'] = x_update_state__mutmut_6 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_7'] = x_update_state__mutmut_7 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_8'] = x_update_state__mutmut_8 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_9'] = x_update_state__mutmut_9 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_10'] = x_update_state__mutmut_10 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_11'] = x_update_state__mutmut_11 # type: ignore # mutmut generated
mutants_x_update_state__mutmut['x_update_state__mutmut_12'] = x_update_state__mutmut_12 # type: ignore # mutmut generated
mutants_x_now_ms__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_now_ms__mutmut)
def now_ms() -> float:
    return time.time() * 1000.0


def x_now_ms__mutmut_orig() -> float:
    return time.time() * 1000.0


def x_now_ms__mutmut_1() -> float:
    return time.time() / 1000.0


def x_now_ms__mutmut_2() -> float:
    return time.time() * 1001.0

mutants_x_now_ms__mutmut['_mutmut_orig'] = x_now_ms__mutmut_orig # type: ignore # mutmut generated
mutants_x_now_ms__mutmut['x_now_ms__mutmut_1'] = x_now_ms__mutmut_1 # type: ignore # mutmut generated
mutants_x_now_ms__mutmut['x_now_ms__mutmut_2'] = x_now_ms__mutmut_2 # type: ignore # mutmut generated
