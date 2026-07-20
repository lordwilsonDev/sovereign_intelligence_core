from __future__ import annotations

from typing import Any

from msb_v2.audit.events import AuditEvent
from msb_v2.audit.storage import AuditStore
from msb_v2.audit.validator import AuditValidator


class AuditEngine:
    def __init__(self, store: AuditStore | None = None, validator: AuditValidator | None = None) -> None:
        self._store = store or AuditStore()
        self._validator = validator or AuditValidator()

    def record(self, event: AuditEvent) -> AuditEvent:
        self._validator.validate(event)
        self._store.append(event)
        return event

    def events(self, limit: int | None = None) -> list[dict[str, Any]]:
        return self._store.read(limit=limit)

    def clear(self) -> None:
        self._store.clear()
