"""Shared client for local model inference — used by any harness that needs LLM access."""
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LocalInferenceClient:
    """Thin wrapper around the Local AI Harness for synchronous inference."""

    def __init__(self, base_url: str = "http://127.0.0.1:8766", model: str = "qwen2.5:0.5b") -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        """Send a prompt to the local model and return the generated text."""
        try:
            import requests
            resp = requests.post(
                f"{self.base_url}/local-ai/infer",
                json={"model": self.model, "prompt": prompt, "max_tokens": max_tokens},
                timeout=30,
            )
            if resp.ok:
                data = resp.json()
                text = data.get("response") or data.get("generated_text") or data.get("text")
                if isinstance(text, str) and text.strip():
                    return text.strip()
                return str(data)
            return f"[Local model error: {resp.status_code}]"
        except Exception as exc:
            logger.debug("Local inference failed: %s", exc)
            return f"[Local model unreachable: {exc}]"
