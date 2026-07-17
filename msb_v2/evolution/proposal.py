from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from enum import Enum


class ProposalStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    APPLIED = "applied"


@dataclass
class Proposal:
    proposal_id: str
    title: str
    description: str
    target_module: str
    change_type: str = "drift_repair"
    status: ProposalStatus = ProposalStatus.PENDING
    evidence: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProposalEngine:
    def propose_from_drift(self, event: dict[str, Any]) -> Proposal:
        proposal_id = f"prop-{event.get('event_id', 'unknown')}"
        return Proposal(
            proposal_id=proposal_id,
            title=f"Drift repair for {event.get('source', 'unknown')}",
            description=f"Stable repeated invocation detected via {event.get('kind', 'event')}.",
            target_module=event.get("source", "unknown").split(".")[0],
            change_type="drift_repair",
            evidence={
                "event_kind": event.get("kind"),
                "trace_id": event.get("trace_id"),
                "decision_id": event.get("decision_id"),
            },
        )

    def update_status(self, proposal: Proposal, status: ProposalStatus) -> Proposal:
        proposal.status = status
        proposal.updated_at = datetime.now(timezone.utc).isoformat()
        return proposal
