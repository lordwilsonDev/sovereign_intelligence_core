"""Supply-Chain Merkle Verifier."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class SupplyChainMerkleVerifier:
    def __init__(self, root: Optional[str] = None, trusted_root_path: Optional[str] = None) -> None:
        self.root = Path(root) if root else Path.cwd()
        self.trusted_root_path = Path(trusted_root_path) if trusted_root_path else self.root / "msb_v2" / "pipeline" / "trusted_supply_chain.json"
        self.trusted_root_hash = self._load_trusted_root()

    def _load_trusted_root(self) -> Optional[str]:
        try:
            if self.trusted_root_path.exists():
                data = json.loads(self.trusted_root_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return str(data.get("merkle_root") or data.get("root_hash") or "").strip() or None
                if isinstance(data, str):
                    return data.strip() or None
        except Exception as exc:
            logger.debug("load_trusted_root_failed: %s", exc)
        return None

    def verify(self) -> Dict[str, object]:
        script = Path(__file__).resolve().parents[2] / "scripts" / "merkle_verify_dependencies.sh"
        try:
            proc = subprocess.run(
                ["bash", str(script), str(self.root), str(self.trusted_root_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            current_hash = (proc.stdout or "").strip().splitlines()[-1] if (proc.stdout or "").strip() else ""
        except Exception as exc:
            return {"ok": False, "current_hash": "", "trusted_root_hash": self.trusted_root_hash, "error": str(exc)}
        ok = bool(current_hash) and current_hash == self.trusted_root_hash
        return {
            "ok": ok,
            "current_hash": current_hash,
            "trusted_root_hash": self.trusted_root_hash,
        }
