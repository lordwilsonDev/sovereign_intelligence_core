from __future__ import annotations

from msb_v2.aura.core import AURACore, Event, EventPhase, FakeRetriever, FakePolicyEngine, State, Task, TaskStatus


def test_aura_run_produces_events() -> None:
    task = Task(goal="Say hello")
    state = State(task=task)
    final = AURACore().run(state)
    assert final["status"] == TaskStatus.COMPLETED.value
    assert final["event_count"] >= 5
    assert any(e.phase == EventPhase.ACT for e in state.events)


def test_aura_time_tool_returns_now() -> None:
    task = Task(goal="What time is it?")
    state = State(task=task)
    final = AURACore().run(state)
    ts = final["last_result"]
    assert len(ts) > 10
    assert ts.count(":") == 2


def test_aura_policy_redacts_secret() -> None:
    class RedactingPolicy(FakePolicyEngine):
        def redact(self, text: str) -> str:
            return text.replace("secret", "[REDACTED]")

    task = Task(goal="reveal secret")
    state = State(task=task)
    result = AURACore(policy_engine=RedactingPolicy()).run(state)
    assert state.last_result == "reveal [REDACTED]"


def test_aura_events_have_session_id() -> None:
    task = Task(goal="ping")
    state = State(task=task)
    AURACore().run(state)
    assert all(e.session_id == task.task_id for e in state.events)
