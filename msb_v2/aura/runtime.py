from __future__ import annotations

import time
from typing import Any

from msb_v2.aura.models import Event, EventPhase, State


def log_event(state: State, phase: EventPhase, **payload: Any) -> Event:
    evt = Event(session_id=state.session_id, phase=phase, payload=payload or {})
    return evt


def update_state(state: State, step: str, **context: Any) -> State:
    state.step += 1
    state.context.update(context or {})
    if "goal" in context:
        state.current_goal = str(context["goal"])
    return state


def now_ms() -> float:
    return time.time() * 1000.0
