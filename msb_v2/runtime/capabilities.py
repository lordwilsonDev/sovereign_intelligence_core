from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True)
class CapabilityEvent:
    module: str
    capability: str
    status: str
    detail: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
