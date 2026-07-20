from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from msb_v2.api.middleware import require_bearer_token
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.business_metrics import BusinessMetrics
from msb_v2.audit.storage import AuditStore

router = APIRouter()


def _engine() -> AuditEngine:
    return AuditEngine(store=AuditStore())


@router.get("/recent")
def recent_audit_events(limit: int = 100, engine: AuditEngine = Depends(_engine)) -> list[dict[str, Any]]:
    return engine.events(limit=limit)


@router.get("/summary")
def audit_summary(limit: int = 100, engine: AuditEngine = Depends(_engine)) -> dict[str, Any]:
    engine.events(limit=limit)
    return BusinessMetrics(audit=engine).snapshot()
