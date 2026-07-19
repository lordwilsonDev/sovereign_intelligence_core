from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from models.registry import default_registry, RegisteredModel, ModelCapabilities


class ModelHealth:
    @staticmethod
    def status() -> Dict[str, Any]:
        items = []
        for name, model in default_registry.models.items():
            items.append({
                "name": model.name,
                "provider": model.provider,
                "enabled": model.enabled,
                "fallback": model.fallback,
                "max_tokens": model.max_tokens,
                "cost_per_1k": model.capabilities.cost_per_1k_tokens,
            })
        return {"models": items, "available_count": len(default_registry.available("reasoning"))}


class ModelRouter:
    @staticmethod
    def route(task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        low = task.lower()
        context_lower = {str(k).lower(): v for k, v in context.items()}
        prefer_local = str(context_lower.get("prefer_local", "")).lower() in {"1", "true", "yes"}
        candidates = default_registry.available("reasoning")
        if not candidates:
            return {"model": "local", "reason": "fallback default", "candidates": []}
        capable = candidates
        if any(k in low for k in ["extract", "parse", "document", "entities"]):
            capable = [m for m in candidates if getattr(m.capabilities, "extraction", False)]
            capable = capable or candidates
        elif any(k in low for k in ["code", "review", "refactor", "function"]):
            capable = [m for m in candidates if getattr(m.capabilities, "coding", False)]
            capable = capable or candidates
        if prefer_local:
            capable = [m for m in capable if getattr(m.provider, "lower", lambda: "")() == "local"] or capable
        ranked = sorted(
            capable,
            key=lambda m: (
                0 if getattr(m.capabilities, "speed", "fast") == "fast" else 1,
                float(m.capabilities.cost_per_1k_tokens or 0),
            ),
        )
        pick = ranked[0]
        return {
            "model": pick.name,
            "provider": pick.provider,
            "reason": "capability match",
            "fallback": pick.fallback,
            "candidates": [m.name for m in candidates],
        }


def compare_outputs(prompt: str, a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "prompt": prompt,
        "a": a,
        "b": b,
        "delta": {
            key: {"a": a.get(key), "b": b.get(key)}
            for key in set(list(a.keys()) + list(b.keys()))
            if a.get(key) != b.get(key)
        },
        "compared_at": time.time(),
    }
