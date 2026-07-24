"""Axiom Library API — eternal memory retrieval and ingestion."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.axiom_library.store import AxiomLibraryStore

router = APIRouter(tags=["axiom-library"])
_store = AxiomLibraryStore()


@router.post("/ingest")
def ingest_axiom(payload: Dict[str, Any]) -> Dict[str, Any]:
    from msb_v2.axiom_library.store import AxiomRecord
    record = AxiomRecord(
        source=str(payload.get("source", "")),
        axiom=str(payload.get("axiom", "")),
        inversion=str(payload.get("inversion", "")),
        predictions=[str(x) for x in payload.get("predictions", [])],
        falsified_count=int(payload.get("falsified_count", 0)),
        claim_count=int(payload.get("claim_count", 0)),
        claims_supported=int(payload.get("claims_supported", 0)),
        topic=payload.get("topic"),
        slug=payload.get("slug"),
        metadata=payload.get("metadata") or {},
    )
    return _store.ingest(record)


@router.get("/search")
def search_axioms(query: str = "", limit: int = 20) -> Dict[str, Any]:
    return {"query": query, "results": _store.search(query=query, limit=limit)}


@router.get("/axiom/{axiom_id}")
def get_axiom(axiom_id: str) -> Dict[str, Any]:
    record = _store.get(axiom_id)
    if not record:
        return {"detail": "Not Found"}
    return record


@router.get("/recent")
def recent_axioms(limit: int = 20) -> Dict[str, Any]:
    return {"results": _store.recent(limit=limit)}


@router.get("/random")
def random_axiom() -> Dict[str, Any]:
    return _store.random()


@router.get("/count")
def axiom_count() -> Dict[str, Any]:
    return {"count": _store.count()}
