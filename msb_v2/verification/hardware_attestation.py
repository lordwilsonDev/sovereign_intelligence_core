"""Hardware-backed attestation for the studio binary."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path
from typing import Dict, Optional


class HardwareAttestation:
    def __init__(self, binary_path: Path, keychain_account: str = "msb-studio", keychain_service: str = "msb-hw-attest") -> None:
        self.binary_path = binary_path
        self.account = keychain_account
        self.service = keychain_service

    def get_current_hash(self) -> str:
        return hashlib.sha256(self.binary_path.read_bytes()).hexdigest()

    def get_trusted_hash(self) -> Optional[str]:
        result = subprocess.run(
            [
                "security",
                "find-generic-password",
                "-a",
                self.account,
                "-s",
                self.service,
                "-w",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip()

    def trust(self) -> Dict[str, Optional[str]]:
        current = self.get_current_hash()
        subprocess.run(
            [
                "security",
                "add-generic-password",
                "-a",
                self.account,
                "-s",
                self.service,
                "-w",
                current,
                "-U",
            ],
            capture_output=True,
            text=True,
        )
        return {"verdict": "TRUST_ESTABLISHED", "current_hash": current, "expected": current}

    def verify(self) -> Dict[str, Optional[str]]:
        current = self.get_current_hash()
        trusted = self.get_trusted_hash()
        if trusted is None:
            return {"verdict": "TRUST_NOT_ESTABLISHED", "current_hash": current, "expected": None}
        if current != trusted:
            return {"verdict": "TAMPERED", "current_hash": current, "expected": trusted}
        return {"verdict": "OK", "current_hash": current, "expected": trusted}
