"""Hardware Identity engine — binds sovereign identity to physical hardware roots."""
from __future__ import annotations

import hashlib
import platform
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional


@dataclass
class HardwareRoot:
    node_id: str
    hardware_hash: str
    platform: str
    machine: str
    processor: str
    bonded_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    secure_enclave: bool = False


class HardwareIdentity:
    """Extracts stable hardware fingerprints and binds them to node identity."""

    def __init__(self, identity_dir: Optional[Path] = None, card=None):
        if card is None:
            from msb_v2.sovereign_identity.identity_card import SovereignIdentityCard
            card = SovereignIdentityCard()
        self.card = card
        self.identity_dir = identity_dir or Path(__file__).resolve().parent.parent.parent / "runtime" / "hardware_identity"
        self.identity_dir.mkdir(parents=True, exist_ok=True)

    def capture(self) -> Optional[HardwareRoot]:
        """Capture hardware fingerprint and bind it to the sovereign identity card."""
        try:
            hw = self._collect_hardware()
            node_id = self.card.node_id()
            hw_hash = self._stable_hash(hw)
            root = HardwareRoot(
                node_id=node_id,
                hardware_hash=hw_hash,
                platform=hw.get("platform", ""),
                machine=hw.get("machine", ""),
                processor=hw.get("processor", ""),
                secure_enclave=hw.get("secure_enclave", False),
            )
            self._persist(root)
            return root
        except Exception as exc:
            return None

    def _collect_hardware(self) -> Dict[str, str]:
        info: Dict[str, str] = {
            "platform": platform.system() or "unknown",
            "machine": platform.machine() or "unknown",
            "processor": platform.processor() or "unknown",
            "secure_enclave": "false",
        }

        # macOS Secure Enclave / T2 / chip detection
        if info["platform"] == "Darwin":
            try:
                model = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"], text=True, timeout=5).strip()
                if model:
                    info["processor"] = model
            except Exception:
                pass
            try:
                hw_opt = subprocess.check_output(["system_profiler", "SPHardwareDataType"], text=True, timeout=20).strip()
                if "Secure Enclave" in hw_opt or "T2" in hw_opt or "Apple Silicon" in hw_opt:
                    info["secure_enclave"] = "true"
            except Exception:
                pass

        return info

    def _stable_hash(self, hw: Dict[str, str]) -> str:
        payload = "|".join([
            hw.get("platform", ""),
            hw.get("machine", ""),
            hw.get("processor", ""),
            hw.get("secure_enclave", "false"),
        ])
        return hashlib.sha256(payload.encode()).hexdigest()[:16]

    def _persist(self, root: HardwareRoot) -> None:
        path = self.identity_dir / f"{root.node_id}.json"
        data = {
            "node_id": root.node_id,
            "hardware_hash": root.hardware_hash,
            "platform": root.platform,
            "machine": root.machine,
            "processor": root.processor,
            "secure_enclave": root.secure_enclave,
            "bonded_at": root.bonded_at,
        }
        path.write_text(__import__("json").dumps(data, indent=2))

    def current(self) -> Optional[HardwareRoot]:
        """Return the current hardware root, if bonded."""
        try:
            node_id = self.card.node_id()
            path = self.identity_dir / f"{node_id}.json"
            if not path.exists():
                return None
            data = __import__("json").loads(path.read_text())
            return HardwareRoot(**data)
        except Exception:
            return None
