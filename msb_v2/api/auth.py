from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from auth.authz_controller import issue_token, verify_token
from security.identity import Identity, PermissionEngine, AuditLog


router = APIRouter(tags=["security", "auth"])
permission_engine = PermissionEngine(default_deny=True)
audit_log = AuditLog()


class ApproveRequest(BaseModel):
    subject: str
    action: str
    resource: str
    roles: list[str] | None = None
    scopes: list[str] | None = None


@router.get("/security/audit")
def security_audit() -> Dict[str, Any]:
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


@router.post("/auth/token/issue")
def auth_token_issue(body: Dict[str, Any]) -> Dict[str, Any]:
    subject = str(body.get("subject", "")).strip()
    roles = list(body.get("roles") or [])
    scopes = list(body.get("scopes") or [])
    if not subject:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="subject is required")
    token = issue_token(subject, roles=roles, scopes=scopes)
    decision = permission_engine.check(Identity(subject=subject, roles=roles, scopes=scopes), "issue_token", "msb")
    event = audit_log.record(identity=Identity(subject=subject, roles=roles, scopes=scopes), action="issue_token", resource="msb", decision=decision)
    return {"subject": subject, "token": token, "allowed": decision.allowed, "event": event}


@router.post("/auth/token/verify")
def auth_token_verify(body: ApproveRequest) -> Dict[str, Any]:
    valid = verify_token(body.subject, body.roles or [], body.scopes or [])
    return {"subject": body.subject, "verified": bool(valid["ok"])}
