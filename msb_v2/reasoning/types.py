from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ReasoningStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    CONTRADICTED = "contradicted"


class JustificationKind(str, Enum):
    FACTUAL = "factual"
    PROCEDURAL = "procedural"
    NORMATIVE = "normative"
    HEURISTIC = "heuristic"
    FINANCIAL = "financial"
    STRATEGIC = "strategic"
    TEMPORAL = "temporal"
    EPISTEMIC = "epistemic"


@dataclass(frozen=True)
class ReasoningStep:
    """Single move inside a reasoning trace."""

    step_index: int
    claim: str
    evidence_refs: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    confidence: float = 0.0
    metadata: dict[str, str | float | int | bool] = field(default_factory=dict)


@dataclass(frozen=True)
class ReasoningTrace:
    """Complete trace: why a decision was made."""

    trace_id: str
    title: str
    status: ReasoningStatus
    steps: tuple[ReasoningStep, ...]
    decision_id: Optional[str] = None
    memory_ids: tuple[str, ...] = ()
    conclusion: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    metadata: dict[str, str | float | int | bool] = field(default_factory=dict)

