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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_sovereign_tool_calls__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_sovereign_tool_calls__mutmut)
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


def x_sovereign_tool_calls__mutmut_orig(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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


def x_sovereign_tool_calls__mutmut_1(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute tool calls through LangGraph if available, otherwise fallback.

    Returns a dict with:
      - backend: "langgraph" or "fallback"
      - results: list of {"tool": str, "output": Any}
    """
    toolbelt = None
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


def x_sovereign_tool_calls__mutmut_2(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute tool calls through LangGraph if available, otherwise fallback.

    Returns a dict with:
      - backend: "langgraph" or "fallback"
      - results: list of {"tool": str, "output": Any}
    """
    toolbelt = Toolbelt()
    available = None
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


def x_sovereign_tool_calls__mutmut_3(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute tool calls through LangGraph if available, otherwise fallback.

    Returns a dict with:
      - backend: "langgraph" or "fallback"
      - results: list of {"tool": str, "output": Any}
    """
    toolbelt = Toolbelt()
    available = {name: toolbelt._registry.get(None) for name in toolbelt.available()}
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


def x_sovereign_tool_calls__mutmut_4(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute tool calls through LangGraph if available, otherwise fallback.

    Returns a dict with:
      - backend: "langgraph" or "fallback"
      - results: list of {"tool": str, "output": Any}
    """
    toolbelt = Toolbelt()
    available = {name: toolbelt._registry.get(name) for name in toolbelt.available()}
    local_tools: List[Any] = None
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


def x_sovereign_tool_calls__mutmut_5(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute tool calls through LangGraph if available, otherwise fallback.

    Returns a dict with:
      - backend: "langgraph" or "fallback"
      - results: list of {"tool": str, "output": Any}
    """
    toolbelt = Toolbelt()
    available = {name: toolbelt._registry.get(name) for name in toolbelt.available()}
    local_tools: List[Any] = []
    for name, fn in available.items():
        if fn is not None:
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


def x_sovereign_tool_calls__mutmut_6(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            break
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


def x_sovereign_tool_calls__mutmut_7(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                local_tools.append(None)
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


def x_sovereign_tool_calls__mutmut_8(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                local_tools.append(_langchain_tool(None, name=name))
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


def x_sovereign_tool_calls__mutmut_9(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                local_tools.append(_langchain_tool(fn, name=None))
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


def x_sovereign_tool_calls__mutmut_10(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                local_tools.append(_langchain_tool(name=name))
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


def x_sovereign_tool_calls__mutmut_11(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                local_tools.append(_langchain_tool(fn, ))
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


def x_sovereign_tool_calls__mutmut_12(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                local_tools.append(None)
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


def x_sovereign_tool_calls__mutmut_13(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            local_tools.append(None)

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


def x_sovereign_tool_calls__mutmut_14(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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

    if _LANGGRAPH_AVAILABLE and local_tools or tool_calls:
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


def x_sovereign_tool_calls__mutmut_15(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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

    if _LANGGRAPH_AVAILABLE or local_tools and tool_calls:
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


def x_sovereign_tool_calls__mutmut_16(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            app = None
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


def x_sovereign_tool_calls__mutmut_17(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            app = _build_tool_graph(None)
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


def x_sovereign_tool_calls__mutmut_18(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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

            state: Dict[str, Any] = None
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


def x_sovereign_tool_calls__mutmut_19(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                "XXmessagesXX": [HumanMessage(content="tool dispatch", tool_calls=tool_calls)],
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


def x_sovereign_tool_calls__mutmut_20(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                "MESSAGES": [HumanMessage(content="tool dispatch", tool_calls=tool_calls)],
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


def x_sovereign_tool_calls__mutmut_21(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                "messages": [HumanMessage(content=None, tool_calls=tool_calls)],
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


def x_sovereign_tool_calls__mutmut_22(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                "messages": [HumanMessage(content="tool dispatch", tool_calls=None)],
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


def x_sovereign_tool_calls__mutmut_23(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                "messages": [HumanMessage(tool_calls=tool_calls)],
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


def x_sovereign_tool_calls__mutmut_24(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                "messages": [HumanMessage(content="tool dispatch", )],
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


def x_sovereign_tool_calls__mutmut_25(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                "messages": [HumanMessage(content="XXtool dispatchXX", tool_calls=tool_calls)],
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


def x_sovereign_tool_calls__mutmut_26(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                "messages": [HumanMessage(content="TOOL DISPATCH", tool_calls=tool_calls)],
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


def x_sovereign_tool_calls__mutmut_27(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                "XXtool_resultsXX": [],
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


def x_sovereign_tool_calls__mutmut_28(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                "TOOL_RESULTS": [],
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


def x_sovereign_tool_calls__mutmut_29(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            result = None
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


def x_sovereign_tool_calls__mutmut_30(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            result = app.invoke(None)
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


def x_sovereign_tool_calls__mutmut_31(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"XXbackendXX": "langgraph", "results": result.get("tool_results", [])}
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


def x_sovereign_tool_calls__mutmut_32(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"BACKEND": "langgraph", "results": result.get("tool_results", [])}
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


def x_sovereign_tool_calls__mutmut_33(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"backend": "XXlanggraphXX", "results": result.get("tool_results", [])}
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


def x_sovereign_tool_calls__mutmut_34(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"backend": "LANGGRAPH", "results": result.get("tool_results", [])}
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


def x_sovereign_tool_calls__mutmut_35(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"backend": "langgraph", "XXresultsXX": result.get("tool_results", [])}
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


def x_sovereign_tool_calls__mutmut_36(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"backend": "langgraph", "RESULTS": result.get("tool_results", [])}
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


def x_sovereign_tool_calls__mutmut_37(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"backend": "langgraph", "results": result.get(None, [])}
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


def x_sovereign_tool_calls__mutmut_38(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"backend": "langgraph", "results": result.get("tool_results", None)}
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


def x_sovereign_tool_calls__mutmut_39(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"backend": "langgraph", "results": result.get([])}
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


def x_sovereign_tool_calls__mutmut_40(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"backend": "langgraph", "results": result.get("tool_results", )}
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


def x_sovereign_tool_calls__mutmut_41(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"backend": "langgraph", "results": result.get("XXtool_resultsXX", [])}
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


def x_sovereign_tool_calls__mutmut_42(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            return {"backend": "langgraph", "results": result.get("TOOL_RESULTS", [])}
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


def x_sovereign_tool_calls__mutmut_43(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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

    results = None
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


def x_sovereign_tool_calls__mutmut_44(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        name = None
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


def x_sovereign_tool_calls__mutmut_45(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        name = call.get(None)
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


def x_sovereign_tool_calls__mutmut_46(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        name = call.get("XXnameXX")
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


def x_sovereign_tool_calls__mutmut_47(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        name = call.get("NAME")
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


def x_sovereign_tool_calls__mutmut_48(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        args = None
        fn = toolbelt._registry.get(name)
        if fn is None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_49(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        args = call.get(None, {})
        fn = toolbelt._registry.get(name)
        if fn is None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_50(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        args = call.get("args", None)
        fn = toolbelt._registry.get(name)
        if fn is None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_51(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        args = call.get({})
        fn = toolbelt._registry.get(name)
        if fn is None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_52(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        args = call.get("args", )
        fn = toolbelt._registry.get(name)
        if fn is None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_53(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        args = call.get("XXargsXX", {})
        fn = toolbelt._registry.get(name)
        if fn is None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_54(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        args = call.get("ARGS", {})
        fn = toolbelt._registry.get(name)
        if fn is None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_55(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        fn = None
        if fn is None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_56(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        fn = toolbelt._registry.get(None)
        if fn is None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_57(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        if fn is not None:
            results.append({"tool": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_58(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            results.append(None)
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_59(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            results.append({"XXtoolXX": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_60(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            results.append({"TOOL": name, "output": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_61(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            results.append({"tool": name, "XXoutputXX": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_62(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            results.append({"tool": name, "OUTPUT": "unknown-tool"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_63(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            results.append({"tool": name, "output": "XXunknown-toolXX"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_64(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
            results.append({"tool": name, "output": "UNKNOWN-TOOL"})
        else:
            try:
                results.append({"tool": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_65(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                results.append(None)
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_66(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                results.append({"XXtoolXX": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_67(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                results.append({"TOOL": name, "output": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_68(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                results.append({"tool": name, "XXoutputXX": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_69(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                results.append({"tool": name, "OUTPUT": fn(**args)})
            except Exception as exc:  # pragma: no cover - defensive fallback
                results.append({"tool": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_70(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                results.append(None)
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_71(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                results.append({"XXtoolXX": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_72(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                results.append({"TOOL": name, "output": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_73(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                results.append({"tool": name, "XXoutputXX": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_74(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
                results.append({"tool": name, "OUTPUT": f"error: {exc}"})
    return {"backend": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_75(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    return {"XXbackendXX": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_76(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    return {"BACKEND": "fallback", "results": results}


def x_sovereign_tool_calls__mutmut_77(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    return {"backend": "XXfallbackXX", "results": results}


def x_sovereign_tool_calls__mutmut_78(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    return {"backend": "FALLBACK", "results": results}


def x_sovereign_tool_calls__mutmut_79(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    return {"backend": "fallback", "XXresultsXX": results}


def x_sovereign_tool_calls__mutmut_80(tool_calls: List[Dict[str, Any]]) -> Dict[str, Any]:
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
    return {"backend": "fallback", "RESULTS": results}

mutants_x_sovereign_tool_calls__mutmut['_mutmut_orig'] = x_sovereign_tool_calls__mutmut_orig # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_1'] = x_sovereign_tool_calls__mutmut_1 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_2'] = x_sovereign_tool_calls__mutmut_2 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_3'] = x_sovereign_tool_calls__mutmut_3 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_4'] = x_sovereign_tool_calls__mutmut_4 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_5'] = x_sovereign_tool_calls__mutmut_5 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_6'] = x_sovereign_tool_calls__mutmut_6 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_7'] = x_sovereign_tool_calls__mutmut_7 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_8'] = x_sovereign_tool_calls__mutmut_8 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_9'] = x_sovereign_tool_calls__mutmut_9 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_10'] = x_sovereign_tool_calls__mutmut_10 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_11'] = x_sovereign_tool_calls__mutmut_11 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_12'] = x_sovereign_tool_calls__mutmut_12 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_13'] = x_sovereign_tool_calls__mutmut_13 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_14'] = x_sovereign_tool_calls__mutmut_14 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_15'] = x_sovereign_tool_calls__mutmut_15 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_16'] = x_sovereign_tool_calls__mutmut_16 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_17'] = x_sovereign_tool_calls__mutmut_17 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_18'] = x_sovereign_tool_calls__mutmut_18 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_19'] = x_sovereign_tool_calls__mutmut_19 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_20'] = x_sovereign_tool_calls__mutmut_20 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_21'] = x_sovereign_tool_calls__mutmut_21 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_22'] = x_sovereign_tool_calls__mutmut_22 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_23'] = x_sovereign_tool_calls__mutmut_23 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_24'] = x_sovereign_tool_calls__mutmut_24 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_25'] = x_sovereign_tool_calls__mutmut_25 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_26'] = x_sovereign_tool_calls__mutmut_26 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_27'] = x_sovereign_tool_calls__mutmut_27 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_28'] = x_sovereign_tool_calls__mutmut_28 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_29'] = x_sovereign_tool_calls__mutmut_29 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_30'] = x_sovereign_tool_calls__mutmut_30 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_31'] = x_sovereign_tool_calls__mutmut_31 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_32'] = x_sovereign_tool_calls__mutmut_32 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_33'] = x_sovereign_tool_calls__mutmut_33 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_34'] = x_sovereign_tool_calls__mutmut_34 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_35'] = x_sovereign_tool_calls__mutmut_35 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_36'] = x_sovereign_tool_calls__mutmut_36 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_37'] = x_sovereign_tool_calls__mutmut_37 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_38'] = x_sovereign_tool_calls__mutmut_38 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_39'] = x_sovereign_tool_calls__mutmut_39 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_40'] = x_sovereign_tool_calls__mutmut_40 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_41'] = x_sovereign_tool_calls__mutmut_41 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_42'] = x_sovereign_tool_calls__mutmut_42 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_43'] = x_sovereign_tool_calls__mutmut_43 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_44'] = x_sovereign_tool_calls__mutmut_44 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_45'] = x_sovereign_tool_calls__mutmut_45 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_46'] = x_sovereign_tool_calls__mutmut_46 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_47'] = x_sovereign_tool_calls__mutmut_47 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_48'] = x_sovereign_tool_calls__mutmut_48 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_49'] = x_sovereign_tool_calls__mutmut_49 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_50'] = x_sovereign_tool_calls__mutmut_50 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_51'] = x_sovereign_tool_calls__mutmut_51 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_52'] = x_sovereign_tool_calls__mutmut_52 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_53'] = x_sovereign_tool_calls__mutmut_53 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_54'] = x_sovereign_tool_calls__mutmut_54 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_55'] = x_sovereign_tool_calls__mutmut_55 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_56'] = x_sovereign_tool_calls__mutmut_56 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_57'] = x_sovereign_tool_calls__mutmut_57 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_58'] = x_sovereign_tool_calls__mutmut_58 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_59'] = x_sovereign_tool_calls__mutmut_59 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_60'] = x_sovereign_tool_calls__mutmut_60 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_61'] = x_sovereign_tool_calls__mutmut_61 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_62'] = x_sovereign_tool_calls__mutmut_62 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_63'] = x_sovereign_tool_calls__mutmut_63 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_64'] = x_sovereign_tool_calls__mutmut_64 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_65'] = x_sovereign_tool_calls__mutmut_65 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_66'] = x_sovereign_tool_calls__mutmut_66 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_67'] = x_sovereign_tool_calls__mutmut_67 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_68'] = x_sovereign_tool_calls__mutmut_68 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_69'] = x_sovereign_tool_calls__mutmut_69 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_70'] = x_sovereign_tool_calls__mutmut_70 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_71'] = x_sovereign_tool_calls__mutmut_71 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_72'] = x_sovereign_tool_calls__mutmut_72 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_73'] = x_sovereign_tool_calls__mutmut_73 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_74'] = x_sovereign_tool_calls__mutmut_74 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_75'] = x_sovereign_tool_calls__mutmut_75 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_76'] = x_sovereign_tool_calls__mutmut_76 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_77'] = x_sovereign_tool_calls__mutmut_77 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_78'] = x_sovereign_tool_calls__mutmut_78 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_79'] = x_sovereign_tool_calls__mutmut_79 # type: ignore # mutmut generated
mutants_x_sovereign_tool_calls__mutmut['x_sovereign_tool_calls__mutmut_80'] = x_sovereign_tool_calls__mutmut_80 # type: ignore # mutmut generated
