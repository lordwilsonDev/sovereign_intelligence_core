from __future__ import annotations

from typing import Any, Dict, List

try:
    from langchain_core.tools import tool as _langchain_tool  # type: ignore[import]
    from langgraph.graph import StateGraph, END  # type: ignore[import]
    from typing_extensions import TypedDict  # type: ignore[import]
    from langchain_core.messages import BaseMessage  # type: ignore[import]

    _LANGGRAPH_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency path
    _LANGGRAPH_AVAILABLE = False
    StateGraph = None  # type: ignore[assignment,misc]
    END = None  # type: ignore[assignment]
    TypedDict = None  # type: ignore[assignment,misc]
    BaseMessage = None  # type: ignore[assignment]

from msb_v2.aura.toolbelt import Toolbelt


if _LANGGRAPH_AVAILABLE:

    class _ToolCallState(TypedDict):
        messages: list
        tool_results: list

    def _build_tool_graph(tools: List[Any]):
        tool_map = {t.name: t for t in tools}

        def tool_node(state: _ToolCallState):
            last = state["messages"][-1]
            calls = getattr(last, "tool_calls", []) or []
            out = []
            for call in calls:
                fn = tool_map.get(call.get("name"))
                if fn is None:
                    out.append({"tool": call.get("name"), "output": "unknown-tool"})
                else:
                    out.append({"tool": call.get("name"), "output": fn.invoke(call.get("args", {}))})
            state["tool_results"] = out
            return {"messages": [{"role": "tool", "content": str(out)}]}

        def router(state: _ToolCallState):
            last = state["messages"][-1]
            return "tool" if getattr(last, "tool_calls", None) else END

        g = StateGraph(_ToolCallState)
        g.add_node("tool", tool_node)
        g.set_conditional_entry_point(router, {"tool": "tool", END: END})
        return g.compile()
else:  # pragma: no cover - optional dependency path
    _ToolCallState = None  # type: ignore[assignment,misc]


def sovereign_tool_calls(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute tool calls through LangGraph if available, otherwise fallback.

    Returns a dict with:
      - backend: "langgraph" or "fallback"
      - results: list of {"tool": str, "output": Any}
    """
    toolbelt = Toolbelt()
    available = {name: toolbelt._registry.get(name) for name in toolbelt.available()}
    local_tools: List[Any] = []
    for name, fn in available.items():
        if fn is None:
            continue
        try:
            if _LANGGRAPH_AVAILABLE:
                local_tools.append(_langchain_tool(fn, name=name))
            else:
                local_tools.append(fn)
        except Exception:
            local_tools.append(fn)

    if _LANGGRAPH_AVAILABLE and local_tools and tool_calls:
        try:
            app = _build_tool_graph(local_tools)
            from langchain_core.messages import HumanMessage  # type: ignore[import]

            state: Dict[str, Any] = {
                "messages": [HumanMessage(content="tool dispatch", tool_calls=tool_calls)],
                "tool_results": [],
            }
            result = app.invoke(state)
            return {"backend": "langgraph", "results": result.get("tool_results", [])}
        except Exception:
            pass

    results = []
    for call in tool_calls:
        name = call.get("name")
        args = call.get("args", {})
        fn = toolbelt._registry.get(name)
        if fn is None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}
