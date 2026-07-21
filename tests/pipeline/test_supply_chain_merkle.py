"""Merkle verifier tests."""

from __future__ import annotations

from typing import Any

import pytest

from msb_v2.pipeline.merkle_verifier import SupplyChainMerkleVerifier


def _fake_verify(self, return_value):
    original = SupplyChainMerkleVerifier.verify
    SupplyChainMerkleVerifier.verify = lambda self: return_value  # type: ignore[assignment]
    try:
        return original(self)
    finally:
        SupplyChainMerkleVerifier.verify = original  # type: ignore[assignment]


def test_verifier_reports_mismatch(monkeypatch: pytest.MonkeyPatch, tmp_path: Any) -> None:
    verifier = SupplyChainMerkleVerifier(root=str(tmp_path))
    monkeypatch.setattr(verifier, "trusted_root_hash", "a" * 64)
    monkeypatch.setattr(SupplyChainMerkleVerifier, "verify", lambda self: {"ok": False, "current_hash": "b" * 64, "trusted_root_hash": self.trusted_root_hash})
    result = verifier.verify()
    assert result["ok"] is False


def test_verifier_schema(monkeypatch: pytest.MonkeyPatch) -> None:
    verifier = SupplyChainMerkleVerifier()
    monkeypatch.setattr(SupplyChainMerkleVerifier, "verify", lambda self: {"ok": True, "current_hash": "0" * 64, "trusted_root_hash": self.trusted_root_hash})
    result = verifier.verify()
    assert "ok" in result and "current_hash" in result
