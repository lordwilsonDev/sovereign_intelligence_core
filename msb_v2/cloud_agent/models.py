from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class CommandStatus(str, Enum):
    executed = "executed"
    echoed = "echoed"
    vetoed = "vetoed"
    confirmed = "confirmed"
    cancelled = "cancelled"


@dataclass(frozen=True)
class CommandResult:
    command_id: str
    status: CommandStatus
    text: str
    risk: str = "low"
    blast_radius: str = ""
    alternatives: list[str] = field(default_factory=list)
    operator_guidance: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "command_id": self.command_id,
            "status": self.status.value,
            "text": self.text,
            "risk": self.risk,
            "blast_radius": self.blast_radius,
            "alternatives": self.alternatives,
            "operator_guidance": self.operator_guidance,
            "metadata": self.metadata,
        }
