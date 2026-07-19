from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter(tags=["security"])


@router.post("/security/rotate")
def security_rotate(body: Dict[str, Any]) -> Dict[str, Any]:
    return {"rotated": False, "reason": "stub", "request": body}


@router.post("/security/secret/store")
def security_secret_store(body: Dict[str, Any]) -> Dict[str, Any]:
    return {"stored": False, "reason": "stub", "request": body}
