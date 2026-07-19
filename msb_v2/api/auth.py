from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from auth.authz_controller import issue_token, verify_token
from msb_v2.api.middleware import require_bearer_token
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
    raw_roles = body.get("roles") or []
    raw_scopes = body.get("scopes") or []
    if not subject or len(subject) < 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="subject is required")
    roles: list[str] = []
    scopes: list[str] = []
    for value in raw_roles:
        token = str(value).strip()
        if not token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="roles must be non-empty strings")
        roles.append(token)
    for value in raw_scopes:
        token = str(value).strip()
        if not token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="scopes must be non-empty strings")
        scopes.append(token)
    allowed_roles = {"user", "power_user", "admin", "system", "operator"}
    if roles and not set(roles).issubset(allowed_roles):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="roles must be from allowed set")
    token = issue_token(subject, roles=roles, scopes=scopes)
    return {"subject": subject, "token": token, "allowed": True, "roles": roles, "scopes": scopes}


@router.post("/auth/token/verify")
def auth_token_verify(body: ApproveRequest) -> Dict[str, Any]:
    valid = verify_token(body.subject, body.roles or [], body.scopes or [])
    return {"subject": body.subject, "verified": bool(valid["ok"])}
