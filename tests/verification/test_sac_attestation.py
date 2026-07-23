"""Hardware attestation SAC integration tests."""

from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path

import pytest

from msb_v2.verification.hardware_attestation import HardwareAttestation


def test_attestation_ok_when_hashes_match(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "proto.bin"
    target.write_bytes(b"sovereign")
    expected = hashlib.sha256(target.read_bytes()).hexdigest()
    attestation = HardwareAttestation(binary_path=target)
    monkeypatch.setattr(
        "msb_v2.verification.hardware_attestation.HardwareAttestation.get_trusted_hash",
        lambda self: expected,
    )
    result = attestation.verify()
    assert result["verdict"] == "OK"
    assert result["expected"] == expected


def test_attestation_tampered_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "proto.bin"
    target.write_bytes(b"sovereign")
    attestation = HardwareAttestation(binary_path=target)
    monkeypatch.setattr(
        "msb_v2.verification.hardware_attestation.HardwareAttestation.get_trusted_hash",
        lambda self: "deadbeef",
    )
    result = attestation.verify()
    assert result["verdict"] == "TAMPERED"
    assert result["expected"] == "deadbeef"


def test_attestation_untrusted_returns_not_established(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    target = tmp_path / "proto.bin"
    target.write_bytes(b"sovereign")
    attestation = HardwareAttestation(binary_path=target)
    monkeypatch.setattr(
        "msb_v2.verification.hardware_attestation.HardwareAttestation.get_trusted_hash",
        lambda self: None,
    )
    result = attestation.verify()
    assert result["verdict"] == "TRUST_NOT_ESTABLISHED"
