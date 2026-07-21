"""Pipeline Integrity Token."""

from __future__ import annotations

import hashlib
import json
import logging
import os
import platform
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class PipelineIntegrityToken:
    def __init__(self, service: str = "MSB Pipeline", keychain_service: str = "MSB Pipeline Integrity") -> None:
        self.service = service
        self.keychain_service = keychain_service

    def sign(self, payload: str) -> Optional[str]:
        if platform.system() != "Darwin" or not Path("/usr/bin/security").exists():
            return "unsigned"
        try:
            env = os.environ.copy()
            env["CFLOG_DISABLE"] = "1"
            secret = subprocess.check_output(
                ["security", "add-generic-password", "-a", self.service, "-s", self.keychain_service, "-w", payload, "-U"],
                stderr=subprocess.DEVNULL,
                text=True,
                env=env,
            ).strip()
            return secret
        except subprocess.CalledProcessError as exc:
            logger.debug("pit_sign_failed: %s", exc)
            return None

    def verify(self, payload: str, signature: Optional[str]) -> bool:
        if not signature:
            return False
        expected = self.sign(payload)
        return expected is not None and signature == expected
