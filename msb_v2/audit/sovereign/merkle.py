from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Optional


class AuditMerkleChain:
    """Append-only, tamper-evident audit log with SHA-256 chain."""

    def __init__(self, log_path: Path, secret_key: Optional[bytes] = None) -> None:
        self.log_path = log_path
        self.secret_key = secret_key or os.urandom(32)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("")

    def _previous_hash(self) -> str:
        try:
            with open(self.log_path, "rb") as f:
                f.seek(-64, 2)
                return f.read().decode()
        except Exception:
            return "0" * 64

    def append(self, event: dict) -> str:
        prev = self._previous_hash()
        payload = json.dumps(event, sort_keys=True, default=str)
        combined = f"{prev}{payload}{self.secret_key.hex()}"
        new_hash = hashlib.sha256(combined.encode()).hexdigest()
        with open(self.log_path, "a") as f:
            f.write(json.dumps({"event": event, "hash": new_hash}) + "\n")
        return new_hash

    def verify_chain(self) -> bool:
        if not self.log_path.exists():
            return True
        with open(self.log_path) as f:
            lines = [line for line in f.readlines() if line.strip()]
        if not lines:
            return True
        prev_hash = "0" * 64
        for line in lines:
            entry = json.loads(line)
            payload = json.dumps(entry["event"], sort_keys=True, default=str)
            combined = f"{prev_hash}{payload}{self.secret_key.hex()}"
            expected = hashlib.sha256(combined.encode()).hexdigest()
            if expected != entry["hash"]:
                return False
            prev_hash = entry["hash"]
        return True
