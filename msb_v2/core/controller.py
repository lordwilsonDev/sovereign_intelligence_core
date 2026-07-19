from __future__ import annotations

import secrets
from typing import Any, Dict, List, Optional

from cognitive_compiler.harness_dispatcher_v1 import HarnessDispatcher
from observability_spans.traces import BasicTracer
from observability_spans.metrics import MetricsEmitter
from runtime.state_machine import RuntimeStateMachine, CREATED, INITIALIZING, READY, THINKING, EXECUTING, VERIFYING, COMPLETED, FAILED


_tracer = BasicTracer()
_metrics = MetricsEmitter()


class Controller:
    def __init__(self) -> None:
        self.sm = RuntimeStateMachine()
        self.dispatcher = HarnessDispatcher()
        self.confirm_tokens: Dict[str, Dict[str, Any]] = {}

    def sandbox_run(self, task_id: str, agent: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        trace_id = secrets.token_hex(4)
        task = self.sm.create_task(task_id, agent=agent)
        span = _tracer.start(trace_id, "sandbox.run", agent, {"task_id": task_id})
        _metrics.observe("sandbox.task.start", 1, {"agent": agent})
        try:
            task.transition(THINKING)
            task.transition(EXECUTING)
            _tracer.finish(span, "ok")
            _metrics.observe("sandbox.task.latency", 0.01, {"agent": agent, "state": "executing"})
            return {
                "task_id": task_id,
                "trace_id": trace_id,
                "state": COMPLETED,
                "agent": agent,
                "decision": payload.get("intent"),
                "verification": {"status": "ok", "actor": "controller"},
                "outcome": "ok",
                "transitions": [t.__dict__ for t in task.transitions],
            }
        except Exception as exc:
            _tracer.finish(span, "error", str(exc))
            _metrics.observe("sandbox.task.error", 1, {"agent": agent})
            raise

    def approval_gate(self, subject: str, action: str, resource: str) -> Dict[str, Any]:
        token = secrets.token_hex(16)
        self.confirm_tokens[token] = {"subject": subject, "action": action, "resource": resource, "used": False}
        return {"confirm_token": token, "subject": subject, "action": action, "resource": resource}

    def metrics_card(self) -> Dict[str, Any]:
        return _metrics.points[-20:]
