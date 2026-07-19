from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from runtime.rollback import rollback_store


router = APIRouter(tags=["recovery"])


class SnapshotRequest(BaseModel):
    key: str
    snapshot: Dict[str, Any]


@router.post("/recovery/snapshot")
def recovery_snapshot(body: SnapshotRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    rollback_store.save(body.key, body.snapshot)
    return {"ok": True, "key": body.key}


@router.get("/recovery/rollback/{key}")
def recovery_rollback(key: str, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    result = rollback_store.rollback(key)
    return {"key": key, **result}


@router.get("/recovery/{key}")
def recovery_status(key: str) -> Dict[str, Any]:
    snap = rollback_store.load(key)
    return {"key": key, "has_snapshot": bool(snap), "snapshot": snap}
