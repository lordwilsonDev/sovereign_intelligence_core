from __future__ import annotations

import os
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from security.identity import Identity, PermissionEngine, AuditLog


router = APIRouter()
permission_engine = PermissionEngine(default_deny=True)
audit_log = AuditLog()


class ApproveRequest(BaseModel):
    subject: str
    action: str
    resource: str
    roles: list[str] | None = None
    scopes: list[str] | None = None


@router.get("/security/audit")
def security_audit(_request: Any) -> Dict[str, Any]:
    return {
        "event_count": len(audit_log.events),
        "events": audit_log.events[-20:],
        "policy": "default_deny_true",
    }


@router.post("/security/approve")
def security_approve(body: ApproveRequest) -> Dict[str, Any]:
    identity = Identity(subject=body.subject, roles=body.roles or [], scopes=body.scopes or [])
    decision = permission_engine.check(identity, body.action, body.resource)
    event = audit_log.record(identity=identity, action=body.action, resource=body.resource, decision=decision)
    if not decision.allowed:
        raise HTTPException(status_code=403, detail={"reason": decision.reason, "missing": decision.missing})
    return {"id": body.subject, "action": body.action, "resource": body.resource, "allowed": True, "event": event}
