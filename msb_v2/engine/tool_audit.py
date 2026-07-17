from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ToolCallAudit:
    tool: str
    args_hash: str
    phase: str = ""
    allowed: bool = True
    blocked_reason: str = ""
    result_summary: str = ""
    timestamp: str = ""


class ToolAudit:
    def __init__(self) -> None:
        self.entries: list[ToolCallAudit] = []

    def record(self, **kwargs: Any) -> ToolCallAudit:
        entry = ToolCallAudit(**kwargs)
        self.entries.append(entry)
        return entry

    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def blocked_count(self) -> int:
        return sum(1 for e in self.entries if not e.allowed)
