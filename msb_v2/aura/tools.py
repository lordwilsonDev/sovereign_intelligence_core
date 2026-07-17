from __future__ import annotations

from typing import Any, Dict

from msb_v2.provider.deepseek import DeepSeekProvider


def deepseek_chat(**kwargs: Any) -> Dict[str, Any]:
    provider = DeepSeekProvider()
    messages = kwargs.get("messages") or [{"role": "user", "content": str(kwargs.get("goal", ""))}]
    max_tokens = int(kwargs.get("max_tokens", 256) or 256)
    result = provider.chat(messages, max_tokens=max_tokens)
    return {
        "status": "ok",
        "message": result.get("content", ""),
        "confidence": 0.95,
        "model": result.get("model"),
    }
