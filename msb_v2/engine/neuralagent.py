"""Thin adapter for executing local neuralagent-style backends."""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, Optional

import urllib.error
import urllib.request

logger = logging.getLogger(__name__)

_DEFAULT_ENDPOINT = os.getenv("MSB_NEURALAGENT_ENDPOINT", "http://localhost:11434")
_DEFAULT_MODEL = os.getenv("MSB_NEURALAGENT_MODEL", "qwen2.5:0.5b")


def _dispatch_local_llm(payload: Dict[str, Any]) -> Dict[str, Any]:
    endpoint = str(payload.get("endpoint") or _DEFAULT_ENDPOINT).rstrip("/")
    model = str(payload.get("model") or _DEFAULT_MODEL)
    prompt = str(payload.get("prompt") or "")
    body = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    request = urllib.request.Request(
        f"{endpoint}/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {"ok": True, "response": data.get("response", ""), "model": model}
    except urllib.error.HTTPError as exc:
        logger.debug("local_llm_http_error: %s", exc)
        return {"ok": False, "error": f"http_{exc.code}", "model": model}
    except Exception as exc:
        logger.debug("local_llm_dispatch_failed: %s", exc)
        return {"ok": False, "error": str(exc), "model": model}


def execute_neuralagent(payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = payload or {}
    provider = str(data.get("provider") or "stub").lower()
    if provider == "ollama":
        return _dispatch_local_llm(data)
    return {
        "backend": "neuralagent",
        "status": "ok",
        "input": data,
        "note": "stubbed_backend",
    }
