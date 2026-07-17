"""Structured in-memory tracing with an exporter-friendly event shape."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from time import perf_counter
from typing import Iterator
from uuid import uuid4


@dataclass
class TraceEvent:
    name: str
    trace_id: str
    started_at: datetime
    duration_ms: float | None = None
    attributes: dict[str, object] = field(default_factory=dict)
    error: str | None = None


class Tracer:
    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    @contextmanager
    def span(self, name: str, **attributes: object) -> Iterator[TraceEvent]:
        event = TraceEvent(name, str(uuid4()), datetime.now(timezone.utc), attributes=attributes)
        started = perf_counter()
        try:
            yield event
        except Exception as error:
            event.error = f"{type(error).__name__}: {error}"
            raise
        finally:
            event.duration_ms = (perf_counter() - started) * 1000
            self.events.append(event)
