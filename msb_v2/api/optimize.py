from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Request

from msb_v2.optimization.engine import OptimizationEngine

router = APIRouter()
_engine = OptimizationEngine()


@router.get("/status")
def status() -> Dict[str, Any]:
    return _engine.status()


@router.post("/analyze")
def analyze(request: Request) -> Dict[str, Any]:
    payload = {}
    try:
        body = request.json()
        if isinstance(body, dict):
            payload = body
    except Exception:
        pass
    proposals = _engine.analyze(payload)
    return {"proposals": proposals}


@router.get("/proposals")
def proposals(limit: int = 50) -> Dict[str, Any]:
    return {"items": _engine.proposals(limit=limit)}


@router.post("/apply/{proposal_id}")
def apply(proposal_id: str) -> Dict[str, Any]:
    result = _engine.apply(proposal_id)
    if result is None:
        return {"status": "not_found"}
    return result


@router.post("/rollback/{proposal_id}")
def rollback(proposal_id: str) -> Dict[str, Any]:
    result = _engine.rollback(proposal_id)
    if result is None:
        return {"status": "not_found"}
    return result


@router.get("/history")
def history(limit: int = 50) -> Dict[str, Any]:
    return {"items": _engine.proposals(limit=limit)}
