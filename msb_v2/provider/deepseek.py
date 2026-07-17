from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional


class DeepSeekProvider:
    """Minimal DeepSeek chat provider.

    Reads `DEEPSEEK_API_KEY` from environment. No key is stored in repo.
    """

    def __init__(self, model: str = "deepseek-chat") -> None:
        self.model = model
        self.api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("DEEPSEEK_API_KEY_DIRECT")
        self._registry = None
        try:
            from msb_v2.models.registry import ModelRegistry
            self._registry = ModelRegistry()
            self._registry.register(_deepseek_record(self.model))
        except Exception:
            pass

    def chat(self, messages: List[Dict[str, str]], max_tokens: int = 256, role: str = "default") -> Optional[Dict[str, Any]]:
        if not self.api_key:
            return None
        start_ms = _now_ms()
        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
        }).encode("utf-8")
        req = __import__("urllib.request", fromlist=["Request"]).Request(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            data=payload,
            method="POST",
        )
        try:
            with __import__("urllib.request", fromlist=["urlopen"]).urlopen(req, timeout=60) as r:
                body = json.loads(r.read().decode("utf-8"))
                choice = (body.get("choices") or [{}])[0]
                message = choice.get("message", {})
                usage = body.get("usage", {})
                latency_ms = _now_ms() - start_ms
                if self._registry is not None:
                    try:
                        self._registry.record_usage(
                            self.model,
                            "live",
                            latency_ms=latency_ms,
                            input_tokens=int(usage.get("prompt_tokens") or 0),
                            output_tokens=int(usage.get("completion_tokens") or 0),
                            role=role,
                        )
                    except Exception:
                        pass
                return {
                    "role": message.get("role", "assistant"),
                    "content": message.get("content", ""),
                    "model": body.get("model", self.model),
                    "latency_ms": latency_ms,
                    "tokens": usage,
                }
        except Exception as exc:
            if self._registry is not None:
                try:
                    self._registry.record_usage(self.model, "live", latency_ms=_now_ms() - start_ms, role=role)
                except Exception:
                    pass
            return {"role": "assistant", "content": f"[deepseek-error] {exc}", "model": self.model, "error": True}

    def plan(self, goal: str, context: Optional[str] = None) -> Dict[str, Any]:
        messages: List[Dict[str, str]] = [
            {
                "role": "user",
                "content": goal if not context else f"{context}\n\nGoal: {goal}",
            }
        ]
        result = self.chat(messages)
        if result is None:
            return {
                "status": "error",
                "message": "missing DEEPSEEK_API_KEY",
                "confidence": 0.0,
            }
        content = result.get("content", "")
        return {
            "status": "ok",
            "message": content,
            "model": result.get("model", self.model),
            "latency_ms": result.get("latency_ms"),
            "tokens": result.get("tokens"),
            "confidence": 0.8,
        }


def _now_ms() -> float:
    return __import__("time").time() * 1000


class _DeepSeekRecord:
    def __init__(self, model: str) -> None:
        self.id = model
        self.version = "live"
        self.provider = "deepseek"
        self.model_type = "chat"
        self.allowed_roles = frozenset({"default"})
        self.input_cost_per_1k = 0.0001
        self.output_cost_per_1k = 0.0002


def _deepseek_record(model: str) -> _DeepSeekRecord:
    return _DeepSeekRecord(model)
