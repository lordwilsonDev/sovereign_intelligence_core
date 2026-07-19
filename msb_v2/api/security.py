from __future__ import annotations

import secrets
import threading
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from msb_v2.api.middleware import require_bearer_token

router = APIRouter(tags=["security"])
_secret_store: Dict[str, Any] = {"current": None, "previous": None, "rotations": 0, "algorithm": "hmac-sha256"}
_secret_lock = threading.Lock()


@router.get("/security/status")
def security_status(auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    return {
        "algorithm": _secret_store["algorithm"],
        "rotation_count": _secret_store["rotations"],
        "current_present": _secret_store["current"] is not None,
        "previous_present": _secret_store["previous"] is not None,
    }


@router.post("/security/secret/store")
def security_secret_store(body: Dict[str, Any], auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    secret = str(body.get("secret", "")).strip()
    if not secret or len(secret) < 16:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="secret must be at least 16 characters")
    metadata = {
        "algorithm": _secret_store["algorithm"],
        "length": len(secret),
        "stored_at": int(__import__("time").time()),
    }
    with _secret_lock:
        _secret_store["previous"] = _secret_store["current"]
        _secret_store["current"] = {"secret": secret, "metadata": metadata}
    return {"stored": True, "metadata": metadata}


@router.post("/security/rotate")
def security_rotate(body: Dict[str, Any], auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    new_secret = secrets.token_hex(32)
    metadata = {
        "algorithm": _secret_store["algorithm"],
        "length": len(new_secret),
        "rotated_at": int(__import__("time").time()),
    }
    with _secret_lock:
        _secret_store["previous"] = _secret_store["current"]
        _secret_store["current"] = {"secret": new_secret, "metadata": metadata}
        _secret_store["rotations"] += 1
    return {
        "rotated": True,
        "rotation_count": _secret_store["rotations"],
        "metadata": metadata,
    }
