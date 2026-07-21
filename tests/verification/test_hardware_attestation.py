"""Hardware attestation regression tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from msb_v2.verification.hardware_attestation import HardwareAttestation


def _best_effort_current_hash() -> str:
    return HardwareAttestation(Path(__file__).resolve()).get_current_hash()


def test_current_hash_is_hex() -> None:
    assert len(_best_effort_current_hash()) == 64
    assert all(ch in "0123456789abcdef" for ch in _best_effort_current_hash())


def test_trusted_hash_returns_none_or_string(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    target = tmp_path / "attestor.bin"
    target.write_bytes(b"x")
    attestation = HardwareAttestation(binary_path=target)
    monkeypatch.setattr("msb_v2.verification.hardware_attestation.subprocess.run", lambda *args, **kwargs: type("R", (), {"returncode": 1, "stdout": ""})())
    result = attestation.verify()
    assert result["verdict"] == "TRUST_NOT_ESTABLISHED"


def test_tampered_fails_when_trusted_set(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    target = tmp_path / "attestor.bin"
    target.write_bytes(b"x")
    attestation = HardwareAttestation(binary_path=target)
    monkeypatch.setattr("msb_v2.verification.hardware_attestation.subprocess.run", lambda *args, **kwargs: type("R", (), {"returncode": 0, "stdout": "deadbeef\n"}))
    result = attestation.verify()
    assert result["verdict"] == "TAMPERED"
    assert result["expected"] == "deadbeef"
