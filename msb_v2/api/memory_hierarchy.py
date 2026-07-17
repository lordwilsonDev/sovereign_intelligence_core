from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.memory.persistence import PersistentMemoryStore

router = APIRouter(tags=["memory"])
_store = PersistentMemoryStore(path="./memory_store.db")


@router.get("/hierarchy")
def memory_hierarchy() -> JSONResponse:
    snapshot = {
        "short_term": _count_by_status(["active"]),
        "working": _count_by_status(["active", "archived"]),
        "long_term": _count_by_status(["active", "archived", "compressed"]),
        "semantic": _count_by_kind("semantic"),
        "episodic": _count_by_kind("episodic"),
        "procedural": _count_by_kind("procedural"),
        "reflective": _count_by_kind("reflective"),
        "policy": _count_by_kind("policy"),
        "strategic": _count_by_kind("strategic"),
    }
    return JSONResponse(snapshot)


def _count_by_status(statuses: List[str]) -> Dict[str, Any]:
    count = 0
    sample_ids: List[str] = []
    for record in _store.iter_all():
        if record.status in statuses:
            count += 1
            if len(sample_ids) < 5:
                sample_ids.append(record.id)
    return {"count": count, "sample_ids": sample_ids}


def _count_by_kind(kind: str) -> Dict[str, Any]:
    count = 0
    sample_ids: List[str] = []
    for record in _store.iter_all():
        if record.kind == kind:
            count += 1
            if len(sample_ids) < 5:
                sample_ids.append(record.id)
    return {"count": count, "sample_ids": sample_ids}
