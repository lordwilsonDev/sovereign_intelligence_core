"""Hardware Identity API — expose hardware-rooted identity endpoints."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.hardware_identity.hardware_identity import HardwareIdentity

router = APIRouter(tags=["hardware-identity"])
_engine = HardwareIdentity()


@router.post("/capture")
def capture_hardware_identity() -> Dict[str, Any]:
    root = _engine.capture()
    if root is None:
        return {"status": "error"}
    return {
        "status": "bonded",
        "node_id": root.node_id,
        "hardware_hash": root.hardware_hash,
        "platform": root.platform,
        "machine": root.machine,
        "processor": root.processor,
        "secure_enclave": root.secure_enclave,
        "bonded_at": root.bonded_at,
    }


@router.get("/current")
def get_current_hardware_identity() -> Dict[str, Any]:
    root = _engine.current()
    if root is None:
        return {"status": "not_bonded"}
    return {
        "status": "bonded",
        "node_id": root.node_id,
        "hardware_hash": root.hardware_hash,
        "platform": root.platform,
        "machine": root.machine,
        "processor": root.processor,
        "secure_enclave": root.secure_enclave,
        "bonded_at": root.bonded_at,
    }
