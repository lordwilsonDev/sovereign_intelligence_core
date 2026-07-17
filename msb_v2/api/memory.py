from __future__ import annotations

from dataclasses import field
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.memory.persistence import PersistentMemoryStore
from msb_v2.memory.types import MemoryConfidence, MemoryHealth, MemoryRecord, MemoryStatus

router = APIRouter()
_memory_store: PersistentMemoryStore | None = None


def _get_store() -> PersistentMemoryStore:
    global _memory_store
    if _memory_store is None:
        _memory_store = PersistentMemoryStore(path="./memory_store.db")
    return _memory_store


class MemoryAddRequest(BaseModel):
    id: str
    kind: str
    content: str
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
    verification_interval_days: Optional[int] = None
    expires_at: Optional[str] = None
    source_reliability: float = 0.5


class MemoryResponse(BaseModel):
    id: str
    kind: str
    status: str


class MemoryConsolidateRequest(BaseModel):
    kind: str
    min_items: int = 3


@router.post("/add", response_model=MemoryResponse)
def memory_add(payload: MemoryAddRequest) -> MemoryResponse:
    record = MemoryRecord(
        id=payload.id,
        kind=payload.kind,
        content=payload.content,
        confidence=MemoryConfidence(verification_interval_days=payload.verification_interval_days, source_reliability=payload.source_reliability),
        tags=list(payload.tags),
        relationships=list(payload.relationships),
        experimental_group=payload.experimental_group,
        hypothesis_id=payload.hypothesis_id,
        outcome=payload.outcome,
        tool=payload.tool,
        model=payload.model,
        version=payload.version,
        immutable=payload.immutable,
        status=payload.status,
    )
    store = _get_store()
    store.add(record)
    return MemoryResponse(id=record.id, kind=record.kind, status=record.status)


@router.get("/health", response_model=MemoryHealth)
def memory_health() -> MemoryHealth:
    return _get_store().health()


@router.get("/search")
def memory_search(q: str) -> Dict[str, Any]:
    results = _get_store().search(q)
    return {"query": q, "results": [{"id": r.id, "kind": r.kind, "content": r.content} for r in results]}


@router.post("/consolidate")
def memory_consolidate(payload: MemoryConsolidateRequest) -> Dict[str, Any]:
    summaries = _get_store().consolidate(payload.kind, min_items=payload.min_items)
    return {"summaries": [{"id": s.id, "kind": s.kind, "content": s.content} for s in summaries]}


@router.post("/{id_}/verify")
def memory_verify(id_: str) -> Dict[str, Any]:
    record = _get_store().verify(id_)
    return {
        "id": record.id,
        "kind": record.kind,
        "status": record.status,
        "verified": record.confidence.verified,
        "last_verified": record.confidence.last_verified.isoformat() if record.confidence.last_verified else None,
        "access_count": record.confidence.access_count,
    }


@router.post("/{id_}/influence")
def memory_influence(id_: str, delta: float) -> Dict[str, Any]:
    record = _get_store().record_influence(id_, delta)
    return {"id": record.id, "decision_impact_score": record.confidence.decision_impact_score}
