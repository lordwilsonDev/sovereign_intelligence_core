from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class ProposalStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    applied = "applied"
    rolled_back = "rolled_back"
    vetoed = "vetoed"


@dataclass(frozen=True)
class OptimizationProposal:
    id: str
    target: str
    current_value: str
    proposed_value: str
    rationale: str
    risk_level: RiskLevel
    status: ProposalStatus = ProposalStatus.pending
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "target": self.target,
            "current_value": self.current_value,
            "proposed_value": self.proposed_value,
            "rationale": self.rationale,
            "risk_level": self.risk_level.value,
            "status": self.status.value,
            "created_at": self.created_at,
            "metadata": self.metadata,
        }


class OptimizationEngine:
    def __init__(self) -> None:
        self._proposals: List[OptimizationProposal] = []
        self._last_run: Optional[str] = None
        self._lock = threading.Lock()

    def analyze(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        candidates = self._rule_based_candidates(metrics)
        with self._lock:
            self._proposals.extend(candidates)
            self._last_run = datetime.now(timezone.utc).isoformat()
        return [c.to_dict() for c in candidates]

    def _rule_based_candidates(self, metrics: Dict[str, Any]) -> List[OptimizationProposal]:
        proposals: List[OptimizationProposal] = []
        cpu = float(metrics.get("cpu_percent", 0.0))
        mem = float(metrics.get("memory_percent", 0.0))
        disk = float(metrics.get("disk_percent", 0.0))
        if cpu > 0.9:
            proposals.append(OptimizationProposal(
                id=_uid(),
                target="cpu_limit",
                current_value="default",
                proposed_value="increase_concurrency",
                rationale="High sustained CPU utilization detected; consider increasing worker concurrency or offloading inference.",
                risk_level=RiskLevel.medium,
            ))
        if mem > 0.9:
            proposals.append(OptimizationProposal(
                id=_uid(),
                target="memory_limit",
                current_value="default",
                proposed_value="reduce_model_offload",
                rationale="Memory pressure is high; reducing model offload or enabling quantization may relieve pressure.",
                risk_level=RiskLevel.medium,
            ))
        if disk > 0.9:
            proposals.append(OptimizationProposal(
                id=_uid(),
                target="disk_cleanup",
                current_value="default",
                proposed_value="purge_temp_cache",
                rationale="Disk usage is high; purging safe temp/cache files may free space.",
                risk_level=RiskLevel.low,
            ))
        return proposals

    def proposals(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            return [p.to_dict() for p in self._proposals[-max(0, limit):]]

    def apply(self, proposal_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            proposal = next((p for p in self._proposals if p.id == proposal_id), None)
        if not proposal:
            return None
        if proposal.status != ProposalStatus.pending:
            return proposal.to_dict()
        proposal = OptimizationProposal(
            id=proposal.id,
            target=proposal.target,
            current_value=proposal.current_value,
            proposed_value=proposal.proposed_value,
            rationale=proposal.rationale,
            risk_level=proposal.risk_level,
            status=ProposalStatus.applied,
            created_at=proposal.created_at,
            metadata=dict(proposal.metadata),
        )
        with self._lock:
            self._proposals = [p for p in self._proposals if p.id != proposal_id]
            self._proposals.append(proposal)
        return proposal.to_dict()

    def rollback(self, proposal_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            proposal = next((p for p in self._proposals if p.id == proposal_id), None)
        if not proposal:
            return None
        proposal = OptimizationProposal(
            id=proposal.id,
            target=proposal.target,
            current_value=proposal.current_value,
            proposed_value=proposal.current_value,
            rationale=f"rollback from {proposal.proposed_value}",
            risk_level=proposal.risk_level,
            status=ProposalStatus.rolled_back,
            created_at=proposal.created_at,
            metadata=dict(proposal.metadata),
        )
        with self._lock:
            self._proposals = [p for p in self._proposals if p.id != proposal_id]
            self._proposals.append(proposal)
        return proposal.to_dict()

    def status(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "status": "ok",
                "last_run": self._last_run,
                "active_proposals": sum(1 for p in self._proposals if p.status == ProposalStatus.pending),
                "applied_count": sum(1 for p in self._proposals if p.status == ProposalStatus.applied),
            }


def _uid() -> str:
    import uuid
    return uuid.uuid4().hex[:8]
