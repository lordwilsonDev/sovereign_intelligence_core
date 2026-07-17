from __future__ import annotations

from typing import Any, Dict

import pytest

from msb_v2.aura import langgraph_bridge


def test_fallback_when_no_langgraph_or_tools(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(langgraph_bridge, "_LANGGRAPH_AVAILABLE", False)
    result = langgraph_bridge.sovereign_tool_calls([])
    assert result["backend"] == "fallback"
    assert result["results"] == []


def test_fallback_when_langgraph_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FakeTool:
        name = "echo"

        def invoke(self, args: Dict[str, Any]) -> str:
            return "ok"

    def _raise(*args: Any, **kwargs: Any) -> Any:
        raise RuntimeError("graph failure")

    monkeypatch.setattr(langgraph_bridge, "_LANGGRAPH_AVAILABLE", True, raising=False)
    monkeypatch.setattr(langgraph_bridge, "_build_tool_graph", lambda *args, **kwargs: _raise, raising=False)
    result = langgraph_bridge.sovereign_tool_calls([{"name": "echo", "args": {}}])
    assert result["backend"] == "fallback"
    assert result["results"] == [{"tool": "echo", "output": {"status": "ok", "message": "", "confidence": 1.0}}]
