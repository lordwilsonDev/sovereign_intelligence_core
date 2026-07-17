from __future__ import annotations

from typing import Any, Dict


def run_tool_agent(**kwargs: Any) -> Dict[str, Any]:
    """Execute or plan a tool call from structured input."""
    tool = str(kwargs.get("tool", "") or "").strip()
    arguments = kwargs.get("arguments", {}) or {}
    if not tool:
        return {"status": "error", "message": "missing tool", "confidence": 0.0}
    return {
        "status": "ok",
        "message": f"Planned tool call: {tool}",
        "confidence": 0.8,
        "tool": tool,
        "arguments": arguments,
    }
