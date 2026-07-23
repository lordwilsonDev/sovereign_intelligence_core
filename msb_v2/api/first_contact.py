"""First Contact Protocol API."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.first_contact.engine import FirstContactEngine

router = APIRouter()
_engine = FirstContactEngine()
_sessions: Dict[str, Dict[str, object]] = {}


@router.post("/start")
def first_contact_start() -> Dict[str, Any]:
    session = _engine.start()
    session_id = str(session.get("session_id", ""))
    _sessions[session_id] = dict(session)
    return session


@router.post("/advance")
def first_contact_advance(payload: Dict[str, Any]) -> Dict[str, Any]:
    session_id = str(payload.get("session_id", "")).strip()
    session = _engine.advance(session_id, payload)
    _sessions[session_id] = dict(session)
    return session


@router.get("/status/{session_id}")
def first_contact_status(session_id: str) -> Dict[str, Any]:
    return _engine.status(session_id)
