from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class EvolutionProposal:
    proposal_id: str
    title: str
    affected_modules: List[str]
    rationale: str
    risk: str = "low"
    status: str = "proposed"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z")
    simulation: Optional[Dict[str, Any]] = None
    approval_status: Optional[str] = None
    failure_reason: Optional[str] = None
    rollback_ref: Optional[str] = None
    fingerprint: Optional[str] = None
    target: Optional[str] = None
