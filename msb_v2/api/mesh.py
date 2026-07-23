"""Distributed Mesh Protocol API."""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import APIRouter, Depends

from msb_v2.api.middleware import require_bearer_token
from msb_v2.mesh.identity import ChallengeResponse, IdentityChallenge, KeyPair, NodeIdentity, NodeRegistry, _challenge_store, _registry

router = APIRouter()
_logger = logging.getLogger(__name__)


def _audit_mesh_event(event: str, payload: dict) -> None:
    try:
        from msb_v2.audit.audit_engine import AuditEngine
        from msb_v2.audit.events import AuditEvent, EventType, Status
        mapping = {
            "MESH_IDENTITY_REGISTER": EventType.START,
            "MESH_IDENTITY_CHALLENGE": EventType.START,
            "MESH_IDENTITY_RESPOND": EventType.SECURITY_ALERT,
            "MESH_PEERS_LIST": EventType.START,
        }
        status = Status.FAILED if payload.get("valid") is False else Status.SUCCEEDED
        engine = AuditEngine()
        engine.record(AuditEvent(workflow="mesh", event_type=mapping.get(event, EventType.START), status=status, metadata=payload))
    except Exception as exc:
        _logger.error("Mesh audit event recording failed: `%s`", exc)


@router.post("/identity/register")
def register_identity(payload: Dict[str, Any], auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    node_id = str(payload.get("node_id", "")).strip()
    public_key_hex = str(payload.get("public_key", "")).strip()
    display_name = str(payload.get("display_name", node_id)).strip()
    endpoints = payload.get("endpoints") or []
    if not node_id or not public_key_hex:
        return {"status": "error", "error": "node_id and public_key are required"}
    try:
        public_key = bytes.fromhex(public_key_hex)
    except ValueError:
        return {"status": "error", "error": "public_key must be hex-encoded"}
    peer = NodeIdentity(node_id=node_id, public_key=public_key, display_name=display_name, endpoints=[str(e) for e in endpoints])
    _registry.register(peer)
    _audit_mesh_event("MESH_IDENTITY_REGISTER", {"node_id": node_id, "display_name": display_name})
    return {"status": "registered", "node_id": node_id, "display_name": display_name}


@router.post("/identity/challenge")
def issue_challenge(payload: Dict[str, Any], auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    node_id = str(payload.get("node_id", "")).strip()
    if not node_id:
        return {"status": "error", "error": "node_id is required"}
    req = IdentityChallenge.issue(node_id)
    _audit_mesh_event("MESH_IDENTITY_CHALLENGE", {"node_id": node_id})
    return {"status": "challenge_issued", "challenge": req.challenge.hex(), "issued_at": req.issued_at}


@router.post("/identity/respond")
def respond_challenge(payload: Dict[str, Any], auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    node_id = str(payload.get("node_id", "")).strip()
    challenge_hex = str(payload.get("challenge", "")).strip()
    response_hex = str(payload.get("response", "")).strip()
    public_key_hex = str(payload.get("public_key", "")).strip()
    if not all([node_id, challenge_hex, response_hex, public_key_hex]):
        return {"status": "error", "error": "node_id, challenge, response, and public_key are required"}
    try:
        challenge = bytes.fromhex(challenge_hex)
        response = bytes.fromhex(response_hex)
        public_key = bytes.fromhex(public_key_hex)
    except ValueError:
        return {"status": "error", "error": "challenge, response, and public_key must be hex-encoded"}
    try:
        challenge_req = _challenge_store.get(node_id)
    except AttributeError:
        return {"status": "error", "error": "no challenge issued for node"}
    if challenge_req is None:
        return {"status": "error", "error": "no challenge issued for node"}
    resp = ChallengeResponse(node_id=node_id, challenge=challenge, response=response, public_key=public_key)
    valid = IdentityChallenge.verify(challenge_req, resp)
    _audit_mesh_event("MESH_IDENTITY_RESPOND", {"node_id": node_id, "valid": valid})
    return {"status": "verified" if valid else "invalid", "node_id": node_id, "valid": valid}


@router.get("/peers")
def list_peers(auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    peers = [p.to_dict() for p in _registry.all()]
    _audit_mesh_event("MESH_PEERS_LIST", {"count": len(peers)})
    return {"peers": peers, "count": len(peers)}
