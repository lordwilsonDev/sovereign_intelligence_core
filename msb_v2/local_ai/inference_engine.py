from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import hashlib
import json
import os
import urllib.request
import urllib.error


from msb_v2.verification.hardware_attestation import HardwareAttestation
from msb_v2.audit.sac_audit import get_audit_log, SacAuditEvent


@dataclass(frozen=True)
class InferenceResult:
    text: str
    model: str
    prompt_hash: str
    backend: str


class InferenceEngine:
    def __init__(self, base_url: str = "http://127.0.0.1:11434") -> None:
        self.base_url = base_url.rstrip("/")
        self._binary_path = Path(__file__).resolve().parents[2] / "msb_v2" / "api" / "web.py"

    def generate(self, model_id: str, prompt: str, max_tokens: int = 256, temperature: float = 0.2) -> InferenceResult:
        self._quarantine(prompt)
        self._sac_attest()
        payload = json.dumps({
            "model": model_id,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = data.get("response", "")
        receipt = {
            "type": "inference",
            "model_id": model_id,
            "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest(),
            "response_hash": hashlib.sha256(text.encode()).hexdigest(),
            "backend": "ollama",
        }
        audit_path = Path(os.environ.get("MSB_AUDIT_DIR") or "/tmp/msb-local-audit")
        audit_path.mkdir(parents=True, exist_ok=True)
        (audit_path / f"inference-{receipt['prompt_hash']}.json").write_text(json.dumps(receipt, indent=2))
        try:
            get_audit_log().append(SacAuditEvent(
                event_id=receipt["prompt_hash"],
                kind="inference",
                actor=f"inference_engine:{model_id}",
                payload={
                    "model_id": model_id,
                    "prompt_hash": receipt["prompt_hash"],
                    "response_hash": receipt["response_hash"],
                    "backend": "ollama",
                },
            ))
        except Exception:
            pass
        return InferenceResult(text=text, model=model_id, prompt_hash=receipt["prompt_hash"], backend="ollama")

    def _sac_attest(self) -> None:
        try:
            verdict = HardwareAttestation(binary_path=self._binary_path).verify()
            if verdict.get("verdict") == "TAMPERED":
                raise RuntimeError(f"SAC attestation failed: {verdict}")
        except Exception as exc:
            raise RuntimeError(f"SAC attestation error: {exc}") from exc

    @staticmethod
    def _quarantine(prompt: str) -> None:
        blocked = ["http://", "https://"]
        lower = prompt.lower()
        for token in blocked:
            if token in lower:
                raise ValueError(f"Prompt rejected by quarantine: contains external URL token: {token.strip()}")
        if len(prompt) > 500_000:
            raise ValueError("Prompt rejected: excessive length.")
