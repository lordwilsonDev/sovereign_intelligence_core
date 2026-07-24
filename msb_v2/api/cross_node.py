"""Cross-Node Task Verification API."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.evolution.cross_node_verification import CrossNodeVerification

router = APIRouter(prefix="/cross-node", tags=["cross-node"])
_engine = CrossNodeVerification()


@router.post("/task")
def submit_cross_node_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    return _engine.submit_task(payload)
