from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
import hashlib
import json
import os
import urllib.request
import urllib.error


@dataclass(frozen=True)
class InferenceResult:
    text: str
    model: str
    prompt_hash: str
    backend: str


class InferenceEngine:
    def __init__(self, base_url: str = "http://127.0.0.1:11434") -> None:
        self.base_url = base_url.rstrip("/")

    def generate(self, model_id: str, prompt: str, max_tokens: int = 256, temperature: float = 0.2) -> InferenceResult:
        self._quarantine(prompt)
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
        # Audit hook: write hash-receipt for prompt/output pair
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
        return InferenceResult(text=text, model=model_id, prompt_hash=receipt["prompt_hash"], backend="ollama")

    @staticmethod
    def _quarantine(prompt: str) -> None:
        # Phase 1: enforce local-only input rules.
        # Reject embedded external URLs as a basic sovereign proxy.
        blocked = ["http://", "https://"]
        lower = prompt.lower()
        for token in blocked:
            if token in lower:
                raise ValueError(f"Prompt rejected by quarantine: contains external URL token: {token.strip()}")
        if len(prompt) > 500_000:
            raise ValueError("Prompt rejected: excessive length.")
