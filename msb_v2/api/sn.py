from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Request

from msb_v2.sn.engine import NotificationEngine
from msb_v2.sn.models import AckRequest, NotificationRequest, UserPreferences
from msb_v2.sn.policy_engine import PolicyEngine
from msb_v2.sn.template_renderer import TemplateRenderer

router = APIRouter()
_engine = NotificationEngine(renderer=TemplateRenderer(), policy=PolicyEngine())


@router.post("/notify")
def notify(request: NotificationRequest) -> Dict[str, Any]:
    record = _engine.notify(request)
    return {"id": record.id, "status": record.status, "channel": record.channel}


@router.get("/status/{notification_id}")
def status(notification_id: str) -> Dict[str, Any]:
    record = _engine.status(notification_id)
    if not record:
        return {"status": "not_found"}
    return record.model_dump()


@router.post("/ack")
def ack(request: AckRequest) -> Dict[str, Any]:
    result = _engine.ack(request)
    return result or {"status": "not_found"}


@router.get("/templates")
def templates() -> Dict[str, Any]:
    return {"templates": ["job_failed", "daily_summary"]}


@router.get("/preferences")
def preferences() -> Dict[str, Any]:
    return _engine._policy.__dict__


@router.put("/preferences")
def update_preferences(prefs: UserPreferences) -> Dict[str, Any]:
    return {"status": "updated", "preferences": prefs.model_dump()}


@router.get("/history")
def history(limit: int = 50) -> Dict[str, Any]:
    return {"notifications": [r.model_dump() for r in _engine.history(limit=limit)]}
