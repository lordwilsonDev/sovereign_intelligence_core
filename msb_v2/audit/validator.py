from __future__ import annotations

from typing import Any

from msb_v2.audit.events import AuditEvent, EventType, Status


class AuditValidator:
    REQUIRED_FIELDS = ("trace_id", "span_id", "timestamp", "workflow", "event_type", "status")

    def validate(self, event: AuditEvent) -> AuditEvent:
        data = event.to_dict()
        for field_name in self.REQUIRED_FIELDS:
            if data.get(field_name) is None:
                raise ValueError(f"AuditEvent missing required field: {field_name}")
        try:
            EventType(data["event_type"])
        except ValueError:
            raise ValueError(f"AuditEvent invalid event_type: {data['event_type']}")
        try:
            Status(data["status"])
        except ValueError:
            raise ValueError(f"AuditEvent invalid status: {data['status']}")
        return event

    def is_valid(self, event: AuditEvent) -> bool:
        try:
            self.validate(event)
            return True
        except ValueError:
            return False
