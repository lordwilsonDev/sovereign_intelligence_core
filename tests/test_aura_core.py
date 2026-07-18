from __future__ import annotations

from msb_v2.aura.core import AURACore, EventPhase, State, Task


def test_aura_core_run_greet() -> None:
    task = Task(goal="Say hello")
    state = State(task=task)
    final = AURACore().run(state)
    assert final["status"] == "COMPLETED"
    assert final["last_result"] == "Say hello"
    assert any(e.phase == EventPhase.ACT for e in state.events)


def test_aura_core_run_time() -> None:
    task = Task(goal="What time is it?")
    state = State(task=task)
    final = AURACore().run(state)
    ts = final["last_result"]
    assert len(ts) > 10
    assert ts.count(":") == 2


def test_aura_core_run_policy_redacts() -> None:
    class Redactor:
        def redact(self, text: str) -> str:
            return text.replace("secret", "[REDACTED]")

    task = Task(goal="reveal secret")
    state = State(task=task)
    final = AURACore(policy_engine=Redactor()).run(state)
    assert "[REDACTED]" in final["last_result"]


def test_aura_core_emits_all_phases() -> None:
    task = Task(goal="ping")
    state = State(task=task)
    AURACore().run(state)
    phases = [e.phase for e in state.events]
    for phase in ["PERCEIVE", "ORIENT", "DECIDE", "ACT", "REFLECT"]:
        assert phase in phases
