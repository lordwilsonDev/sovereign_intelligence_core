"""Hardware Identity tests."""
from __future__ import annotations

from pathlib import Path
from typing import Dict
from unittest.mock import MagicMock, patch

import pytest

from msb_v2.hardware_identity.hardware_identity import HardwareIdentity


def test_capture_binds_hardware(tmp_path: Path) -> None:
    card = MagicMock()
    card.node_id.return_value = "node-1"
    engine = HardwareIdentity(identity_dir=tmp_path, card=card)
    root = engine.capture()
    assert root is not None
    assert root.node_id == "node-1"
    assert len(root.hardware_hash) == 16
    assert (tmp_path / "node-1.json").exists()


def test_current_returns_none_when_not_bonded(tmp_path: Path) -> None:
    card = MagicMock()
    card.node_id.return_value = "missing"
    engine = HardwareIdentity(identity_dir=tmp_path, card=card)
    assert engine.current() is None


def test_secure_enclave_detection_true() -> None:
    card = MagicMock()
    card.node_id.return_value = "node-1"
    engine = HardwareIdentity(card=card)
    hw = {"platform": "Darwin", "machine": "arm64", "processor": "model", "secure_enclave": "false"}
    with patch.object(engine, "_collect_hardware", return_value=hw):
        with patch.object(engine, "_stable_hash", return_value="hash123"):
            with patch.object(engine, "_persist"):
                root = engine.capture()
    assert root is not None
    assert root.hardware_hash == "hash123"


def test_secure_enclave_true_branch() -> None:
    card = MagicMock()
    card.node_id.return_value = "node-1"
    engine = HardwareIdentity(card=card)
    hw = {"platform": "Darwin", "machine": "arm64", "processor": "M1", "secure_enclave": "true"}
    with patch.object(engine, "_collect_hardware", return_value=hw):
        with patch.object(engine, "_stable_hash", return_value="hash123"):
            with patch.object(engine, "_persist"):
                root = engine.capture()
    assert root is not None
    assert root.secure_enclave == "true"
