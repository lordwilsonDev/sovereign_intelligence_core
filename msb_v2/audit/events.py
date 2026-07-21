from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class EventType(str, Enum):
    START = "START"
    INPUT_VALIDATED = "INPUT_VALIDATED"
    MODEL_SELECTED = "MODEL_SELECTED"
    TOOL_CALLED = "TOOL_CALLED"
    TOOL_COMPLETED = "TOOL_COMPLETED"
    RETRY = "RETRY"
    TIMEOUT = "TIMEOUT"
    CACHE_HIT = "CACHE_HIT"
    CACHE_MISS = "CACHE_MISS"
    ROUTING_DECISION = "ROUTING_DECISION"
    HUMAN_OVERRIDE = "HUMAN_OVERRIDE"
    SELF_CORRECTION = "SELF_CORRECTION"
    SELF_CORRECTION_BLOCKED = "SELF_CORRECTION_BLOCKED"
    WORKFLOW_COMPLETE = "WORKFLOW_COMPLETE"
    WORKFLOW_FAILED = "WORKFLOW_FAILED"
    SECURITY_ALERT = "SECURITY_ALERT"


class Status(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"


class AuditEvent:
    __slots__ = (
        "trace_id",
        "span_id",
        "parent_span_id",
        "timestamp",
        "workflow",
        "agent",
        "event_type",
        "status",
        "duration_ms",
        "input_hash",
        "output_hash",
        "cost",
        "confidence",
        "reasoning_summary",
        "exception",
        "metadata",
    )

    def __init__(
        self,
        *,
        trace_id: str | None = None,
        span_id: str | None = None,
        parent_span_id: str | None = None,
        workflow: str = "unspecified",
        agent: str | None = None,
        event_type: str | EventType = EventType.START,
        status: str | Status = Status.PENDING,
        duration_ms: int = 0,
        input_hash: str | None = None,
        output_hash: str | None = None,
        cost: dict[str, Any] | None = None,
        confidence: float = 0.0,
        reasoning_summary: str | None = None,
        exception: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.trace_id = trace_id or str(uuid.uuid4())
        self.span_id = span_id or str(uuid.uuid4())
        self.parent_span_id = parent_span_id
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.workflow = workflow
        self.agent = agent
        self.event_type = event_type.value if isinstance(event_type, EventType) else event_type
        self.status = status.value if isinstance(status, Status) else status
        self.duration_ms = int(duration_ms)
        self.input_hash = input_hash
        self.output_hash = output_hash
        self.cost = cost or {}
        self.confidence = float(confidence)
        self.reasoning_summary = reasoning_summary
        self.exception = exception
        self.metadata = metadata or {}

    def to_dict(self) -> dict[str, Any]:
        return {slot: getattr(self, slot) for slot in self.__slots__}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AuditEvent":
        kwargs = {}
        for slot in cls.__slots__:
            if slot in data and slot != "timestamp":
                kwargs[slot] = data[slot]
        kwargs.setdefault("workflow", "unspecified")
        kwargs.setdefault("status", Status.PENDING)
        kwargs.setdefault("event_type", EventType.START)
        return cls(**kwargs)
