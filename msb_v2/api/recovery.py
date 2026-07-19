from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from runtime.rollback import rollback_store


router = APIRouter(tags=["recovery"])


class SnapshotRequest(BaseModel):
    key: str
    snapshot: Dict[str, Any]


@router.post("/recovery/snapshot")
def recovery_snapshot(body: SnapshotRequest) -> Dict[str, Any]:
    rollback_store.save(body.key, body.snapshot)
    return {"ok": True, "key": body.key}


@router.get("/recovery/rollback/{key}")
def recovery_rollback(key: str) -> Dict[str, Any]:
    result = rollback_store.rollback(key)
    return {"key": key, **result}


@router.get("/recovery/{key}")
def recovery_status(key: str) -> Dict[str, Any]:
    snap = rollback_store.load(key)
    return {"key": key, "has_snapshot": bool(snap), "snapshot": snap}
