from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from msb_v2.sn.models import AckRequest, NotificationRecord, NotificationRequest, UserPreferences
from msb_v2.sn.policy_engine import PolicyEngine
from msb_v2.sn.template_renderer import TemplateRenderer


class NotificationEngine:
    def __init__(
        self,
        renderer: Optional[TemplateRenderer] = None,
        policy: Optional[PolicyEngine] = None,
    ) -> None:
        self._renderer = renderer or TemplateRenderer()
        self._policy = policy or PolicyEngine()
        self._records: Dict[str, NotificationRecord] = {}

    def notify(self, request: NotificationRequest) -> NotificationRecord:
        record = NotificationRecord(
            id=str(uuid.uuid4()),
            request=request.model_dump(),
            status="queued",
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._records[record.id] = record
        channels = self._policy.evaluate(request.priority, request.channels or ["console"])
        rendered = self._renderer.render(request.template, request.template_data)
        record.rendered = rendered
        if not channels:
            record.status = "blocked"
            record.detail = "blocked by policy"
            return record
        if request.require_ack:
            record.status = "awaiting_ack"
            record.channel = ",".join(channels)
            return record
        from msb_v2.sn.dispatcher import Dispatcher
        responses = Dispatcher().dispatch(request, rendered)
        sent = [r for r in responses if r.status == "sent"]
        if sent:
            record.status = "sent"
            record.channel = ",".join([r.channel for r in sent])
        else:
            record.status = "failed"
            record.detail = "; ".join([r.detail for r in responses if r.detail])
        record.updated_at = datetime.now(timezone.utc).isoformat()
        return record

    def ack(self, ack_request: AckRequest) -> Optional[Dict[str, Any]]:
        for record in self._records.values():
            if record.status == "awaiting_ack" and record.id == ack_request.ack_id:
                record.status = "acked"
                record.detail = ack_request.response
                record.updated_at = datetime.now(timezone.utc).isoformat()
                return {"id": record.id, "response": ack_request.response}
        return None

    def status(self, notification_id: str) -> Optional[NotificationRecord]:
        return self._records.get(notification_id)

    def history(self, limit: int = 50) -> List[NotificationRecord]:
        return list(self._records.values())[-limit:]
