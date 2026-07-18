from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from msb_v2.v3.tools import ToolDeclaration, ToolRegistry

router = APIRouter()
registry = ToolRegistry()


def _seed_defaults() -> None:
    if registry.all():
        return
    defaults = [
        ToolDeclaration(
            name="web_search",
            description="Searches the web for any information.",
            parameters={"query": {"type": "STRING", "description": "Search query"},
                        "mode": {"type": "STRING", "description": "search or compare"}},
            required=["query"],
            tags=["search"],
        ),
        ToolDeclaration(
            name="weather_report",
            description="Gives a weather report for the requested city.",
            parameters={"city": {"type": "STRING", "description": "City name"}},
            required=["city"],
            tags=["weather"],
        ),
        ToolDeclaration(
            name="file_controller",
            description="Manages files and folders: list, create, delete, move, copy, read, write.",
            parameters={"action": {"type": "STRING", "description": "write | list | read | delete"},
                        "path": {"type": "STRING", "description": "Path or 'desktop'"},
                        "name": {"type": "STRING", "description": "Filename"}},
            required=["action"],
            tags=["files"],
        ),
        ToolDeclaration(
            name="youtube_video",
            description="Controls YouTube: search, play, trending, summarize.",
            parameters={"action": {"type": "STRING", "description": "play | summarize | trending"},
                        "query": {"type": "STRING", "description": "Search query"}},
            required=["action"],
            tags=["media"],
        ),
        ToolDeclaration(
            name="computer_settings",
            description="Controls system: volume, brightness, keyboard shortcuts, screenshots, dark mode, WiFi.",
            parameters={"action": {"type": "STRING", "description": "Action name"},
                        "description": {"type": "STRING", "description": "Natural language description"}},
            required=[],
            tags=["system"],
        ),
    ]
    for tool in defaults:
        registry.register(tool)


_seed_defaults()


@router.get("/v3/tools")
def list_tools() -> dict[str, Any]:
    return {"tools": [t.name for t in registry.all()]}


@router.get("/v3/tools/schema")
def tool_schema() -> dict[str, Any]:
    return {"tools": registry.to_openai_schema()}


@router.get("/v3/tools/{name}")
def get_tool(name: str) -> dict[str, Any]:
    tool = registry.get(name)
    if not tool:
        return {"error": "not_found"}
    return {
        "name": tool.name,
        "description": tool.description,
        "parameters": tool.parameters,
        "required": tool.required,
        "tags": tool.tags,
    }
