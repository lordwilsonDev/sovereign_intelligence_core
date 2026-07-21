"""KB4 result schema."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass(frozen=True)
class KB4Result:
    intent: str
    result: Dict[str, Any]
    sovereignty_score: float
    reasoning_to_noise_ratio: float
    falsification_score: float
    audit_receipt: str
    continuity_token: str
    mutation_triggered: bool
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
