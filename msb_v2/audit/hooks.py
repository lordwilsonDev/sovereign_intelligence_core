from __future__ import annotations

from typing import Any, Callable

from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.events import AuditEvent, EventType, Status
from msb_v2.audit.schemas import stable_workflow


def build_audit_hook(engine: AuditEngine, workflow: str, agent: str) -> Callable[[str, str, dict[str, Any] | None, str | None], None]:
    _span_lookup: dict[str, dict[str, str]] = {}
    _started: dict[str, str] = {}

    def _ensure_span(task_id: str) -> dict[str, str]:
        if task_id not in _span_lookup:
            parent_span_id = None
            parent = None
            if parent:
                parent_span_id = None
            span_id = None
            _span_lookup[task_id] = {"span_id": span_id, "parent_span_id": parent_span_id}
        return _span_lookup[task_id]

    def hook(event_name: str, task_id: str, payload: dict[str, Any] | None, metadata: str | None) -> None:
        if payload is None:
            payload = {}
        mapping = {
            "dispatch": EventType.START,
            "result": EventType.WORKFLOW_COMPLETE,
            "error": EventType.WORKFLOW_FAILED,
            "blocked": EventType.WORKFLOW_FAILED,
        }
        event_type = mapping.get(event_name, EventType.START)
        status = Status.SUCCEEDED if event_name == "result" else Status.FAILED if event_name in {"error", "blocked"} else Status.RUNNING
        workflow_name = f"{workflow}-{event_name}" if event_name else workflow
        event = AuditEvent(
            workflow=workflow_name,
            agent=agent,
            event_type=event_type,
            status=status,
            metadata={"task_id": task_id, "payload": payload, "metadata": metadata},
        )
        engine.record(event)

    return hook
