from __future__ import annotations

from datetime import datetime, timedelta

from msb_v2.memory.store import MemoryStore
from msb_v2.memory.types import MemoryConfidence, MemoryKind, MemoryRecord, MemoryStatus


def _record(id_: str, *, content: str = "x", kind: str = MemoryKind.SEMANTIC, status: str = MemoryStatus.ACTIVE) -> MemoryRecord:
    return MemoryRecord(
        id=id_,
        kind=kind,
        content=content,
        confidence=MemoryConfidence(confidence=0.8),
        status=status,
    )


def test_memory_add_get_and_limit() -> None:
    store = MemoryStore()
    rec = _record("m1", content="alpha")
    assert store.add(rec) == "m1"
    assert store.get("m1").content == "alpha"
    try:
        store.add(rec)
    except KeyError:
        pass
    else:
        raise AssertionError("expected duplicate id to raise")
    assert store.get("missing") is None


def test_trust_score_decays_with_age() -> None:
    store = MemoryStore()
    past = datetime.now() - timedelta(hours=10)
    rec = MemoryRecord(
        id="old1",
        kind=MemoryKind.SEMANTIC,
        content="stale fact",
        confidence=MemoryConfidence(confidence=0.9, trust_score=1.0, created=past),
        status=MemoryStatus.ACTIVE,
    )
    store.add(rec)
    trust = store.trust_score("old1")
    assert 0.0 <= trust <= 0.9


def test_detect_contradiction_on_semantic_conflict() -> None:
    store = MemoryStore()
    rec_a = _record("a", content="Server uses AWS")
    rec_b = _record("b", content="Server uses AWS and Lambda")
    store.add(rec_a)
    store.add(rec_b)
    conflicts = store.detect_contradictions(rec_b)
    assert "a" in conflicts


def test_search_returns_ranked_records() -> None:
    store = MemoryStore()
    store.add(_record("r1", content="Rust server", kind=MemoryKind.SEMANTIC))
    stored = store.add(_record("r2", content="Rust runtime", kind=MemoryKind.SEMANTIC))
    results = store.search("rust")
    assert stored in [r.id for r in results]


def test_reflection_engine_counts_preserved_and_mistakes() -> None:
    store = MemoryStore()
    store.add(MemoryRecord(id="refl", kind=MemoryKind.REFLECTIVE, content="lesson", confidence=MemoryConfidence(confidence=0.8)))
    store.add(MemoryRecord(id="good", kind=MemoryKind.EXPERIENCE, content="worked", confidence=MemoryConfidence(confidence=0.8), outcome="success"))
    store.add(MemoryRecord(id="bad", kind=MemoryKind.EXPERIENCE, content="failed hard", confidence=MemoryConfidence(confidence=0.8), outcome="failure"))
    summary = store.active_reflection()
    assert summary["reflection_count"] == 1
    assert summary["experiences_preserved"] == 1
    assert summary["experiences_failed"] == 1


def test_verify_marks_record_and_updates_metadata() -> None:
    store = MemoryStore()
    store.add(
        MemoryRecord(
            id="v1",
            kind=MemoryKind.SEMANTIC,
            content="old version",
            confidence=MemoryConfidence(confidence=0.4, source="web"),
        )
    )
    updated = store.verify("v1")
    assert updated.confidence.verified is True
    assert updated.confidence.last_verified is not None
    assert updated.confidence.access_count == 1


def test_stale_detects_expired_and_unverified() -> None:
    store = MemoryStore()
    expired = datetime.now() - timedelta(days=2)
    store.add(
        MemoryRecord(
            id="s1",
            kind=MemoryKind.SEMANTIC,
            content="expired fact",
            confidence=MemoryConfidence(expires_at=expired),
        )
    )
    store.add(
        MemoryRecord(
            id="s2",
            kind=MemoryKind.SEMANTIC,
            content="interval fact",
            confidence=MemoryConfidence(verification_interval_days=1),
        )
    )
    assert store.stale("s1") is True
    assert store.stale("s2") is True
    assert store.stale("missing") is False


def test_consolidation_is_idempotent_when_no_clusters() -> None:
    store = MemoryStore()
    store.add(MemoryRecord(id="a", kind=MemoryKind.EPISODIC, content="alpha", confidence=MemoryConfidence(), tags=["solo"]))
    first = store.consolidate(MemoryKind.EPISODIC, min_items=2)
    second = store.consolidate(MemoryKind.EPISODIC, min_items=2)
    assert first == []
    assert second == []
    assert store.health().compression_ratio == 0.0
