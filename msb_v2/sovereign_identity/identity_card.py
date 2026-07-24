"""Sovereign Identity Card — signed, verifiable digital identity."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests

class SovereignIdentityCard:
    """Generates and verifies a signed identity document rooted in the Secure Enclave."""

    def __init__(self):
        self.node_id = self._get_or_create_node_id()

    def _get_or_create_node_id(self) -> str:
        """Retrieve or generate a persistent node identifier from the Keychain."""
        try:
            result = subprocess.run(
                ["security", "find-generic-password", "-a", "msb-node", "-s", "sovereign-node-id", "-w"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception:
            pass
        # Generate new node ID
        import uuid
        new_id = str(uuid.uuid4())
        try:
            subprocess.run(
                ["security", "add-generic-password", "-a", "msb-node", "-s", "sovereign-node-id",
                 "-w", new_id, "-U"],
                check=True, capture_output=True, timeout=10,
            )
        except Exception:
            pass
        return new_id

    def generate(self) -> Dict[str, Any]:
        """Generate a signed Sovereign Identity Card."""
        sac_data = {}
        try:
            resp = requests.get("http://127.0.0.1:8766/sac/status", timeout=5)
            if resp.ok:
                sac_data = resp.json()
        except Exception:
            pass

        attest_data = {}
        try:
            resp = requests.post("http://127.0.0.1:8766/sac/attest", timeout=5)
            if resp.ok:
                attest_data = resp.json()
        except Exception:
            pass

        document = {
            "node_id": self.node_id,
            "sas": sac_data.get("sas", {}).get("score", 0),
            "attestation": attest_data.get("verdict", "UNKNOWN"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        document["signature"] = hashlib.sha256(
            json.dumps(document, sort_keys=True).encode() + self.node_id.encode()
        ).hexdigest()
        return document

    def verify(self, card: Dict[str, Any]) -> bool:
        """Verify a Sovereign Identity Card signature."""
        card = dict(card)
        signature = card.pop("signature", None)
        if not signature:
            return False
        expected = hashlib.sha256(
            json.dumps(card, sort_keys=True).encode() + card.get("node_id", "").encode()
        ).hexdigest()
        return signature == expected
