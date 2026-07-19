from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.reasoning.integrity import EventKind, ExecutionEvent
from msb_v2.api.reasoning_integrity import _stream

router = APIRouter(tags=["alerts"])


class AlertPayload(BaseModel):
    alerts: list[dict[str, Any]] | None = None
    status: str | None = None
    commonLabels: Dict[str, str] | None = None
    commonAnnotations: Dict[str, str] | None = None
    externalURL: str | None = None
    version: str | None = None
    groupKey: Dict[str, Any] | None = None
    truncatedAlerts: int | None = None


def _normalize_alerts(payload: AlertPayload) -> list[dict[str, Any]]:
    alerts = payload.alerts or []
    normalized = []
    for alert in alerts:
        labels = dict(alert.get("labels") or {})
        annotations = dict(alert.get("annotations") or {})
        normalized.append(
            {
                "status": alert.get("status") or payload.status or "unknown",
                "labels": labels,
                "annotations": annotations,
                "startsAt": alert.get("startsAt"),
                "endsAt": alert.get("endsAt"),
                "fingerprint": alert.get("fingerprint") or labels.get("alertname") or "unknown",
                "externalURL": payload.externalURL,
            }
        )
    return normalized


@router.post("/webhook", dependencies=[Depends(require_bearer_token)])
def alert_webhook(payload: AlertPayload) -> Dict[str, Any]:
    alerts = _normalize_alerts(payload)
    events = []
    for alert in alerts:
        labels = alert.get("labels") or {}
        alert_name = labels.get("alertname", "unknown")
        severity = labels.get("severity", "info")
        trace_id = f"alert::{alert.get('fingerprint', alert_name)}"
        source = f"prometheus::{alert_name}"
        event = ExecutionEvent(
            event_id=f"{trace_id}::webhook",
            sequence=_stream.events_for_trace(trace_id).__len__() + 1,
            kind=EventKind.ALERT,
            source=source,
            payload={
                "status": alert.get("status"),
                "fingerprint": alert.get("fingerprint"),
                "labels": labels,
                "annotations": alert.get("annotations"),
                "startsAt": alert.get("startsAt"),
                "endsAt": alert.get("endsAt"),
                "externalURL": alert.get("externalURL"),
            },
            trace_id=trace_id,
        )
        normalized_event = _stream.append(event)
        events.append(
            {
                "event_id": normalized_event.event_id,
                "sequence": normalized_event.sequence,
                "kind": normalized_event.kind.value,
                "source": normalized_event.source,
                "status": alert.get("status"),
                "alertname": alert_name,
                "severity": severity,
                "fingerprint": alert.get("fingerprint"),
                "ts": normalized_event.ts,
            }
        )
    return {
        "status": "ok",
        "received": len(alerts),
        "events": events,
        "alerts": len(alerts),
    }
