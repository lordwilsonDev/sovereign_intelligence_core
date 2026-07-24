"""Zero-Knowledge proof receipt tests."""
from __future__ import annotations

import pytest

from msb_v2.zk_proof.receipts import ZKProofReceipt, verify_proof


def test_verify_proof_returns_true() -> None:
    receipt = ZKProofReceipt(
        receipt_id="r1",
        axiom_id="a1",
        proof="proof",
        public_signals={"x": 1},
    )
    assert verify_proof(receipt) is True
    assert receipt.verified is True
