from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


from msb_v2.schh.engine import ComponentType, CheckMethod


@dataclass(frozen=True)
class Component:
    id: str
    name: str
    type: ComponentType = ComponentType.harness
    health_endpoint: str = ""
    check_method: CheckMethod = CheckMethod.http
    check_interval_seconds: int = 30
    timeout_seconds: int = 5
    critical: bool = True
    auto_heal: bool = False
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
