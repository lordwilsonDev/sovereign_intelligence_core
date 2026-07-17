from __future__ import annotations

import uuid
from typing import Any, Dict

from msb_v2.aura.models import Event, EventPhase, State, Task
from msb_v2.aura.persistence import Persistence
from msb_v2.aura.runtime import log_event, now_ms, update_state
from msb_v2.aura.toolbelt import Toolbelt
from msb_v2.aura.memory.retriever import BM25Retriever
from msb_v2.aura.policies.engine import PolicyEngine
from msb_v2.aura.grounding import GroundingGate


def _decide_tool(goal: str, toolbelt: Toolbelt) -> str:
    goal_lower = goal.lower()
    if "skill" in goal_lower:
        for name in ("list_skills", "get_skill"):
            if name in toolbelt.available():
                return name
    if "time" in goal_lower:
        if "get_time" in toolbelt.available():
            return "get_time"
    if "get_time" in toolbelt.available():
        return "get_time"
    return "echo"


class AURACore:
    def __init__(
        self,
        persistence: Persistence | None = None,
        toolbelt: Toolbelt | None = None,
        grounding_gate: GroundingGate | None = None,
    ) -> None:
        self.persistence = persistence or Persistence()
        self.toolbelt = toolbelt or Toolbelt()
        self.grounding_gate = grounding_gate or GroundingGate()

    async def run(
        self,
        goal: str,
        session_id: str | None = None,
        retriever: Any | None = None,
        policy_engine: Any | None = None,
        identity_id: str | None = None,
    ) -> State:
        state = State(session_id=session_id or str(uuid.uuid4().hex), current_goal=goal)
        state.context["_start_ms"] = now_ms()
        state = update_state(state, "PERCEIVE", goal=goal)
        await self._phase(state, EventPhase.PERCEIVE, goal=goal)

        retriever = retriever or BM25Retriever([])
        policy_engine = policy_engine or PolicyEngine()

        await self._phase(state, EventPhase.ORIENT, action="noop", message="no memory retrieved")
        try:
            memories = await retriever.retrieve(goal, top_k=3)
            redacted = [policy_engine.apply(m) for m in memories]
            await self._phase(state, EventPhase.ORIENT, action="memory", message=f"retrieved {len(redacted)} memories", memories=redacted)
        except Exception as exc:
            await self._phase(state, EventPhase.ORIENT, action="memory", status="ERROR", message=str(exc))

        state = update_state(
            state,
            "DECIDE",
            decision={
                "tool": "echo"
                if goal.lower().startswith("say")
                else _decide_tool(goal, self.toolbelt),
                "arguments": {"message": goal},
            },
        )
        decision = state.context.get("decision", {})
        await self._phase(state, EventPhase.DECIDE, decision=decision)
        act_payload = {"tool": decision.get("tool", "echo"), "arguments": decision.get("arguments", {})}
        await self._phase(state, EventPhase.ACT, **act_payload)
        tool_result = await self.toolbelt.call(decision.get("tool", "echo"), state, decision.get("arguments", {}), identity_id=identity_id)
        tool_result = self.grounding_gate.fuse(tool_result)

        tool_event_id = tool_result.get("event_id")
        if tool_event_id:
            tool_rows = self.persistence.recent_events(state.session_id, limit=10)
            tool_row = next((r for r in tool_rows if r.get("event_id") == tool_event_id), None)
            if tool_row and tool_row.get("status") in {"SUCCESS", "ERROR"}:
                state.context["last_tool_event_id"] = tool_event_id
                state.context["last_tool_status"] = tool_row.get("status", "SUCCESS")

        state = update_state(state, "REFLECT", result=tool_result)
        reflect_payload: Dict[str, Any] = {"result": tool_result}
        reflect_payload["outcome"] = "success" if tool_result.get("status") == "ok" else "failure"
        evt = log_event(state, EventPhase.REFLECT, status=tool_result.get("status", "FAILED"), payload=reflect_payload)
        start_ms = float(state.context.get("_start_ms", now_ms()))
        evt.latency_ms = now_ms() - start_ms
        self.persistence.save_event(evt.__dict__)
        state.context.setdefault("phase_events", []).append({"phase": EventPhase.REFLECT.value, "event_id": evt.event_id})

        task = Task(goal=goal, metadata={"session_id": state.session_id, "step_count": state.step})
        self.persistence.save_task(task.__dict__)
        state.task_id = task.task_id
        state.context["task_status"] = task.status
        if tool_result.get("status") != "ok":
            raise RuntimeError(tool_result.get("message", "tool failed"))
        return state

    async def _phase(self, state: State, phase: EventPhase, **payload: Any) -> Event:
        evt = log_event(state, phase, payload=payload or {})
        self.persistence.save_event(evt.__dict__)
        state.context.setdefault("phase_events", []).append({"phase": phase.value, "event_id": evt.event_id})
        return evt
