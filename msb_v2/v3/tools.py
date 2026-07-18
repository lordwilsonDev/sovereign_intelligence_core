from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ToolAction(str, Enum):
    SEARCH = "search"
    COMPARE = "compare"
    WRITE = "write"
    READ = "read"
    CREATE = "create"
    DELETE = "delete"
    OPEN = "open"
    PLAY = "play"
    SUMMARIZE = "summarize"


@dataclass
class ToolDeclaration:
    name: str
    description: str
    parameters: dict[str, Any] = field(default_factory=dict)
    required: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDeclaration] = {}

    def register(self, tool: ToolDeclaration) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDeclaration | None:
        return self._tools.get(name)

    def all(self) -> list[ToolDeclaration]:
        return list(self._tools.values())

    def to_openai_schema(self) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": {
                        "type": "object",
                        "properties": t.parameters,
                        "required": t.required,
                    },
                },
            }
            for t in self._tools.values()
        ]
