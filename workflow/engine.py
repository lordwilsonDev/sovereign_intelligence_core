from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


QUEUED = "QUEUED"
RUNNING = "RUNNING"
CHECKPOINTED = "CHECKPOINTED"
COMPLETED = "COMPLETED"
FAILED = "FAILED"
CANCELLED = "CANCELLED"


@dataclass
class WorkflowStep:
    name: str
    run: Callable[[Dict[str, Any]], Any]
    retries: int = 0
    timeout_s: float = 60.0


@dataclass
class WorkflowRun:
    run_id: str
    goal: str
    state: str = QUEUED
    context: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Any] = None
    error: Optional[str] = None
    checkpoints: List[Dict[str, Any]] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    updated_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))


class WorkflowEngine:
    def __init__(self, event_bus=None) -> None:
        self.runs: Dict[str, WorkflowRun] = {}
        self.steps: Dict[str, List[WorkflowStep]] = {}
        self.event_bus = event_bus

    def register(self, workflow_name: str, steps: List[WorkflowStep]) -> None:
        self.steps[workflow_name] = steps

    def start(self, workflow_name: str, goal: str, context: Optional[Dict[str, Any]] = None) -> WorkflowRun:
        run_id = uuid.uuid4().hex
        run = WorkflowRun(run_id=run_id, goal=goal, context=context or {})
        self.runs[run_id] = run
        if self.event_bus:
            self.event_bus.emit("TaskStarted", {"run_id": run_id, "workflow": workflow_name, "goal": goal})
        self._execute(workflow_name, run)
        return run

    def _execute(self, workflow_name: str, run: WorkflowRun) -> None:
        steps = self.steps.get(workflow_name, [])
        run.state = RUNNING
        run.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for step in steps:
            try:
                result = step.run(run.context)
                run.checkpoints.append({"step": step.name, "ok": True, "ts": run.updated_at})
                run.context[step.name] = result
                if self.event_bus:
                    self.event_bus.emit("StepCompleted", {"run_id": run.run_id, "step": step.name})
            except Exception as exc:
                run.error = str(exc)
                run.state = FAILED
                run.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                if self.event_bus:
                    self.event_bus.emit("TaskFailed", {"run_id": run.run_id, "step": step.name, "error": str(exc)})
                return
        run.state = COMPLETED
        run.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        run.result = run.context
        if self.event_bus:
            self.event_bus.emit("TaskCompleted", {"run_id": run.run_id})

    def get(self, run_id: str) -> WorkflowRun:
        return self.runs[run_id]


class InMemoryEventBus:
    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []

    def emit(self, event: str, payload: Dict[str, Any]) -> None:
        self.events.append({"event": event, "payload": payload, "ts": time.time()})
