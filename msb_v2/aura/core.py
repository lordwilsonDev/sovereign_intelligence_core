from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional


class EventPhase(str, Enum):
    PERCEIVE = "PERCEIVE"
    ORIENT = "ORIENT"
    DECIDE = "DECIDE"
    ACT = "ACT"
    REFLECT = "REFLECT"


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    DLQ = "DLQ"


@dataclass
class Task:
    goal: str
    task_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    client_id: str = "default"
    status: str = TaskStatus.PENDING
    created_at: float = field(default_factory=time.time)
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Event:
    event_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    timestamp: float = field(default_factory=time.time)
    session_id: str = ""
    phase: str = EventPhase.PERCEIVE
    actor: str = "AURA"
    tool_name: Optional[str] = None
    latency_ms: Optional[float] = None
    status: str = "SUCCESS"
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class State:
    task: Optional[Task] = None
    phase: str = EventPhase.PERCEIVE
    events: List[Event] = field(default_factory=list)
    last_result: Any = None
    retriever_context: List[str] = field(default_factory=list)
    policy_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task.task_id if self.task else "",
            "goal": self.task.goal if self.task else "",
            "status": self.task.status if self.task else "",
            "phase": self.phase,
            "event_count": len(self.events),
            "last_result": self.last_result,
            "retriever_context": self.retriever_context,
            "policy_notes": self.policy_notes,
        }


def _emit(state: State, phase: str, tool_name: Optional[str], start: float, payload: Dict[str, Any]) -> Event:
    event = Event(session_id=state.task.task_id if state.task else "", phase=phase, actor="AURA", tool_name=tool_name, latency_ms=round((time.time() - start) * 1000, 2), payload=payload)
    state.events.append(event)
    state.phase = phase
    return event


class FakeRetriever:
    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        return [f"memory:{query}"] * top_k


class FakePolicyEngine:
    def redact(self, text: str) -> str:
        return text.replace("secret", "[REDACTED]")


_TOOLS: Dict[str, Callable[[State, Any], Dict[str, Any]]] = {}


def register_tool(name: str):
    def _wrap(fn: Callable[[State, Any], Dict[str, Any]]):
        _TOOLS[name] = fn
        return fn
    return _wrap


@register_tool("echo")
def _tool_echo(state: State, payload: Any) -> Dict[str, Any]:
    text = payload.get("message", state.task.goal if state.task else "")
    return {"status": "ok", "message": text}


@register_tool("get_time")
def _tool_time(state: State, payload: Any) -> Dict[str, Any]:
    return {"status": "ok", "now": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())}


class AURACore:
    def __init__(self, retriever: Any = None, policy_engine: Any = None) -> None:
        self.retriever = retriever or FakeRetriever()
        self.policy = policy_engine or FakePolicyEngine()

    def _fail(self, state: State, error: str) -> Dict[str, Any]:
        if state.task is not None:
            state.task.status = TaskStatus.FAILED
        _emit(state, EventPhase.REFLECT, None, time.time(), {"error": error})
        return {"error": error}

    def run(self, state: State) -> Dict[str, Any]:
        if state.task is None:
            raise ValueError("state.task is None")

        p_start = time.time()
        state.task.status = TaskStatus.RUNNING
        _emit(state, EventPhase.PERCEIVE, None, p_start, {"goal": state.task.goal})

        o_start = time.time()
        state.retriever_context = self.retriever.retrieve(state.task.goal, top_k=3)
        _emit(state, EventPhase.ORIENT, None, o_start, {"context": state.retriever_context})

        d_start = time.time()
        plan = generate_plan(state.task.goal, state.retriever_context)
        _emit(state, EventPhase.DECIDE, None, d_start, {"plan": plan})

        a_start = time.time()
        first = plan[0] if plan else {"tool": "echo", "payload": {"message": state.task.goal}}
        tool = _TOOLS.get(first.get("tool", "echo"), _TOOLS["echo"])
        raw = tool(state, first.get("payload", {}))
        outgoing = self._result_to_text(raw)
        final = self.policy.redact(outgoing)
        state.last_result = final
        _emit(state, EventPhase.ACT, first.get("tool"), a_start, {"result": state.last_result})

        r_start = time.time()
        state.task.status = TaskStatus.COMPLETED
        _emit(state, EventPhase.REFLECT, None, r_start, {"completed": True, "result": state.last_result})
        return state.to_dict()

    @staticmethod
    def _result_to_text(raw: Dict[str, Any]) -> str:
        for key in ("message", "now", "result"):
            if key in raw:
                return str(raw[key])
        return str(raw)


def generate_plan(goal: str, context: List[str]) -> List[Dict[str, Any]]:
    g = (goal or "").lower()
    if any(k in g for k in ["time", "clock"]):
        return [{"tool": "get_time", "payload": {}}]
    return [{"tool": "echo", "payload": {"message": goal}}]
