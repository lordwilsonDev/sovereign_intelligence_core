from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from msb_v2.audit.events import AuditEvent
from msb_v2.audit.storage import AuditStore
from msb_v2.audit.validator import AuditValidator


class ReplayEngine:
    def __init__(self, store: AuditStore | None = None, validator: AuditValidator | None = None) -> None:
        self._store = store or AuditStore()
        self._validator = validator or AuditValidator()

    def load_events(self, limit: int | None = None) -> list[dict[str, Any]]:
        return self._store.read(limit=limit)

    def filter(self, workflow: str | None = None, event_type: str | None = None, status: str | None = None) -> list[dict[str, Any]]:
        events = self.load_events()
        result: list[dict[str, Any]] = []
        for event in events:
            if workflow is not None and event.get("workflow") != workflow:
                continue
            if event_type is not None and event.get("event_type") != event_type:
                continue
            if status is not None and event.get("status") != status:
                continue
            result.append(event)
        return result

    def validate_loaded(self, events: list[dict[str, Any]]) -> list[AuditEvent]:
        validated: list[AuditEvent] = []
        errors: list[str] = []
        for event in events:
            try:
                validated.append(AuditEvent.from_dict(event))
            except Exception as error:
                errors.append(str(error))
        if errors:
            raise ValueError("Replay validation failed: " + "; ".join(errors))
        return validated

    def clear(self) -> None:
        self._store.clear()
