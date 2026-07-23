"""Snapshot API — trigger sovereign encrypted backups."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.snapshot.engine import SnapshotEngine

router = APIRouter(prefix="/snapshot", tags=["snapshot"])
_engine = SnapshotEngine()


@router.post("/capture")
def capture_snapshot() -> Dict[str, Any]:
    """Take a full encrypted snapshot to local disk."""
    return _engine.capture()


@router.get("/list")
def list_snapshots() -> Dict[str, Any]:
    """List available local snapshots."""
    return {"snapshots": _engine.list_snapshots()}
