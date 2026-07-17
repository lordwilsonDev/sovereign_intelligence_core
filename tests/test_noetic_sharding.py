from __future__ import annotations

import pytest

from msb_v2.core.noetic_sharding import NoeticShard, NoeticStore
from msb_v2.memory.types import MemoryRecord, MemoryConfidence, MemoryStatus, MemoryKind


def _record(id_: str, content: str, *, tags=None, status=MemoryStatus.ACTIVE):
    return MemoryRecord(
        id=id_,
        kind=MemoryKind.SEMANTIC,
        content=content,
        confidence=MemoryConfidence(confidence=0.9, importance=0.8, trust_score=0.8),
        tags=tags or [],
        status=status,
        tool="test",
        model="test-model",
        version="1.0",
    )


def test_noetic_shard_tag_filter_rejects() -> None:
    shard = NoeticShard("secure", allowed_tags=["secret"])
    record = _record("r1", "hello", tags=["public"])
    with pytest.raises(PermissionError):
        shard.add(record)


def test_noetic_shard_add_get_search() -> None:
    shard = NoeticShard("alpha")
    shard.add(_record("r1", "hello world", tags=["a"]))
    assert shard.get("r1") is not None
    assert shard.get("missing") is None
    assert shard.search("hello")[0].id == "r1"


def test_noetic_shard_isolation() -> None:
    store = NoeticStore()
    secure = store.create_shard("secure", allowed_tags=["secret"])
    public = store.create_shard("public")
    secure.add(_record("s1", "secret note", tags=["secret"]))
    public.add(_record("p1", "public note", tags=["public"]))
    assert public.get("s1") is None
    assert secure.get("p1") is None


def test_noetic_shard_mark_status() -> None:
    shard = NoeticShard("archive")
    shard.add(_record("a1", "x", tags=[]))
    shard.mark_status("a1", MemoryStatus.ARCHIVED)
    assert shard.get("a1").status == MemoryStatus.ARCHIVED


def test_noetic_shard_health() -> None:
    shard = NoeticShard("h1", allowed_tags=["x"])
    shard.add(_record("h1-1", "v", tags=["x"]))
    h = shard.health()
    assert h["shard_id"] == "h1"
    assert h["active_records"] == 1


def test_noetic_shard_consolidation() -> None:
    shard = NoeticShard("cons")
    shard.add(_record("c1", "alpha", tags=["group"]))
    shard.add(_record("c2", "beta", tags=["group"]))
    shard.add(_record("c3", "gamma", tags=["group"]))
    summaries = shard.consolidate(MemoryKind.SEMANTIC, min_items=2)
    assert len(summaries) == 1
    assert summaries[0].kind == MemoryKind.PROCEDURAL


def test_noetic_store_duplicate_shard_returns_existing() -> None:
    store = NoeticStore()
    a = store.create_shard("x")
    b = store.create_shard("x")
    assert a is b
