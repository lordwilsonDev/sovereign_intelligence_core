from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


def influence_penalty(score: float, delta: float) -> float:
    return max(-1.0, min(1.0, score + delta))


@dataclass(frozen=True)
class MemoryConfidence:
    confidence: float = 0.5
    importance: float = 0.5
    novelty: float = 0.5
    trust_score: float = 0.5
    last_access: Optional[datetime] = None
    last_verified: Optional[datetime] = None
    created: datetime = field(default_factory=lambda: datetime.now())
    source: str = "runtime"
    verified: bool = False
    access_count: int = 0
    verification_interval_days: Optional[int] = None
    expires_at: Optional[datetime] = None
    source_reliability: float = 0.5
    retrieval_count: int = 0
    decision_impact_score: float = 0.0


@dataclass(frozen=True)
class MemoryHealth:
    verified_facts: int = 0
    unverified_facts: int = 0
    conflicts: int = 0
    avg_confidence: float = 0.0
    duplicates: int = 0
    growth_rate: float = 0.0
    decay_rate: float = 0.0
    compression_ratio: float = 0.0
    stale_records: int = 0
    retrievals: int = 0
    avg_decision_impact_score: float = 0.0


class MemoryStatus:
    ACTIVE = "active"
    ARCHIVED = "archived"
    COMPRESSED = "compressed"
    DELETED = "deleted"


class MemoryKind:
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    STRATEGIC = "strategic"
    REFLECTIVE = "reflective"
    POLICY = "policy"
    SOCIAL = "social"
    TEMPORAL = "temporal"
    EXPERIENCE = "experience"


@dataclass(frozen=True)
class MemoryRecord:
    id: str
    kind: str
    content: str
    confidence: MemoryConfidence
    tags: List[str] = field(default_factory=list)
    relationships: List[str] = field(default_factory=list)
    experimental_group: Optional[str] = None
    hypothesis_id: Optional[str] = None
    outcome: Optional[str] = None
    tool: Optional[str] = None
    model: Optional[str] = None
    version: Optional[str] = None
    immutable: bool = False
    status: str = MemoryStatus.ACTIVE
    revision_id: Optional[str] = None
    revision_of: Optional[str] = None
    integrity_hash: Optional[str] = None
    provenance: Optional[str] = None
