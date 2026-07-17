from __future__ import annotations


from msb_v2.aura.aura_core import AURACore
from msb_v2.aura.models import EventPhase, State
from msb_v2.aura.persistence import Persistence


def test_sprint1_state_survives_db():
    persistence = Persistence(":memory:")
    goal = "Say hello"
    core = AURACore(persistence=persistence)
    result_state = __import__("asyncio").run(core.run(goal=goal, session_id="sprint1-test"))
    assert result_state.current_goal == goal
    row = persistence.get_task(result_state.task_id)
    assert row is not None
    assert row["goal"] == goal


def test_sprint1_event_logging():
    persistence = Persistence(":memory:")
    core = AURACore(persistence=persistence)
    result_state = __import__("asyncio").run(core.run(goal="Say hello", session_id="sprint1-events"))
    events = persistence.recent_events(result_state.session_id, limit=20)
    phases = [e["phase"] for e in events]
    assert EventPhase.PERCEIVE.value in phases
    assert EventPhase.REFLECT.value in phases
    assert len(events) >= 5


def test_toolbelt_echo_and_get_time():
    from msb_v2.aura.toolbelt import Toolbelt
    toolbelt = Toolbelt()
    state = State(session_id="toolbelt-test")
    echo = __import__("asyncio").run(toolbelt.call("echo", state, {"message": "ping"}))
    assert echo["status"] == "ok"
    assert echo["message"] == "ping"
    clock = __import__("asyncio").run(toolbelt.call("get_time", state, {}))
    assert clock["status"] == "ok"
    assert clock["confidence"] == 1.0


def test_toolbelt_unknown_tool():
    from msb_v2.aura.toolbelt import Toolbelt
    toolbelt = Toolbelt()
    state = State(session_id="toolbelt-unknown")
    result = __import__("asyncio").run(toolbelt.call("nope", state, {}))
    assert result["status"] == "error"
    assert "unknown tool" in result["message"].lower()
