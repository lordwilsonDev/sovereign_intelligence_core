"""Zero-Knowledge proof API endpoints."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.zk_proof.receipts import ZKProofReceipt, verify_proof

router = APIRouter(tags=["zk-proof"])


@router.post("/verify")
def verify_zk_proof(payload: Dict[str, Any]) -> Dict[str, Any]:
    receipt = ZKProofReceipt(
        receipt_id=payload.get("receipt_id", ""),
        axiom_id=payload.get("axiom_id", ""),
        proof=payload.get("proof", ""),
        public_signals=payload.get("public_signals", {}),
    )
    ok = verify_proof(receipt)
    return {"verified": ok, "receipt_id": receipt.receipt_id}
