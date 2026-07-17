from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass
class Claim:
    id: str
    text: str
    source: str
    inversion_of: str | None = None
    scores: Dict[str, float] = field(default_factory=dict)
    status: str = "pending"


@dataclass
class DebateRound:
    query: str
    claims: List[Claim]
    nodes: List[str]
    votes: List[Tuple[str, str, str, float]]  # claim_id, stance, evidence, confidence
    transcript: List[str]
    transcript_hash: str = ""


class HiveMindNode(ABC):
    """Specialized perspective in MoIE broadcast."""

    role: str = "base"

    @abstractmethod
    def deliberate(self, claim: Claim, context: Dict[str, Any]) -> Tuple[str, str, float]:
        """Return (stance, evidence, confidence)."""
        raise NotImplementedError


class AgentDriver:
    """Wraps an external agent/tool into the HiveMindNode interface."""

    def __init__(self, name: str, runner):
        self.name = name
        self._runner = runner

    async def deliberate(self, claim: Claim, context: Dict[str, Any]) -> Tuple[str, str, float]:
        result = await self._runner(claim=claim, context=context)
        if isinstance(result, dict):
            return str(result.get("stance", "outside_scope")), str(result.get("evidence", "")), float(result.get("confidence", 0.0))
        return "outside_scope", "", 0.0


class DeterministicNode(HiveMindNode):
    """Fallback stub node when no domain-specific agent exists."""

    def deliberate(self, claim: Claim, context: Dict[str, Any]) -> Tuple[str, str, float]:
        score = float(claim.scores.get("impact", 0.5))
        if score >= 0.8:
            return "support", f"High impact score {score:.2f} supports inversion", 0.7
        if score <= 0.2:
            return "reject", f"Low impact score {score:.2f} limits feasibility", 0.7
        return "refine", f"Score {score:.2f} requires additional evidence", 0.5
