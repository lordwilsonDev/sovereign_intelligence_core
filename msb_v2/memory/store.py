from __future__ import annotations

from collections import deque
from datetime import datetime
from typing import Any, Dict, List, Optional

from msb_v2.memory.types import MemoryConfidence, MemoryKind, MemoryRecord, MemoryStatus, MemoryHealth, influence_penalty


def _now() -> datetime:
    return datetime.now()


def _default_decay(base: float, age_hours: float) -> float:
    return max(0.0, base * (0.95 ** age_hours))


class MemoryStore:
    def __init__(self, *, default_ttl_hours: Optional[float] = None, cool_pool_max: int = 500) -> None:
        self._records: Dict[str, MemoryRecord] = {}
        self._contradiction_pairs: List[List[str]] = []
        self._created_order: deque[str] = deque(maxlen=cool_pool_max)
        self._default_ttl_hours = default_ttl_hours
        self._ins = 0
        self._deleted = 0

    def add(self, record: MemoryRecord) -> str:
        id_ = record.id
        if id_ in self._records:
            raise KeyError(f"duplicate memory id: {id_}")
        self._records[id_] = record
        self._created_order.append(id_)
        self._ins += 1
        return id_

    def get(self, id_: str) -> Optional[MemoryRecord]:
        record = self._records.get(id_)
        if record is None or record.status == MemoryStatus.DELETED:
            return None
        return record

    def mark_status(self, id_: str, status: str) -> None:
        record = self.get(id_)
        if record.immutable:
            raise PermissionError(f"immutable memory: {id_}")
        self._records[id_] = MemoryRecord(
            id=record.id,
            kind=record.kind,
            content=record.content,
            confidence=MemoryConfidence(
                confidence=record.confidence.confidence,
                importance=record.confidence.importance,
                novelty=record.confidence.novelty,
                trust_score=record.confidence.trust_score,
                last_access=_now(),
                last_verified=record.confidence.last_verified,
                created=record.confidence.created,
                source=record.confidence.source,
                verified=record.confidence.verified,
                access_count=record.confidence.access_count + 1,
                verification_interval_days=record.confidence.verification_interval_days,
                expires_at=record.confidence.expires_at,
                source_reliability=record.confidence.source_reliability,
                retrieval_count=record.confidence.retrieval_count,
                decision_impact_score=record.confidence.decision_impact_score,
            ),
            tags=list(record.tags),
            relationships=list(record.relationships),
            experimental_group=record.experimental_group,
            hypothesis_id=record.hypothesis_id,
            outcome=record.outcome,
            tool=record.tool,
            model=record.model,
            version=record.version,
            immutable=record.immutable,
            status=status,
        )

    def trust_score(self, id_: str) -> float:
        record = self.get(id_)
        age_hours = (_now() - record.confidence.created).total_seconds() / 3600.0
        decayed_confidence = _default_decay(record.confidence.confidence, age_hours)
        return decayed_confidence * record.confidence.trust_score

    def detect_contradictions(self, new_record: MemoryRecord) -> List[str]:
        conflicts: List[str] = []
        if new_record.kind != MemoryKind.SEMANTIC:
            return conflicts
        needle = new_record.content.strip()
        for record in self._records.values():
            if record.kind != MemoryKind.SEMANTIC or record.id == new_record.id:
                continue
            if record.content.strip() == needle:
                continue
            if needle in record.content or record.content in needle:
                conflicts.append(record.id)
        if conflicts:
            self._contradiction_pairs.append([new_record.id, *conflicts])
        return conflicts

    def refresh(self, id_: str) -> None:
        record = self.get(id_)
        if record.immutable:
            return
        age_hours = (_now() - record.confidence.created).total_seconds() / 3600.0
        if self._default_ttl_hours is not None and age_hours > self._default_ttl_hours:
            self.mark_status(id_, MemoryStatus.ARCHIVED)

    def search(self, query: str, *, limit: int = 20) -> List[MemoryRecord]:
        q = query.casefold()
        scored: List[tuple[float, str]] = []
        for id_, record in self._records.items():
            if record.status == MemoryStatus.DELETED or record.status == MemoryStatus.ARCHIVED:
                continue
            text = f"{record.content} {' '.join(record.tags)}".casefold()
            similarity = text.count(q) / 10.0
            recency_hours = (_now() - record.confidence.created).total_seconds() / 3600.0
            recency = max(0.0, 1.0 - recency_hours / 168.0)
            influence = record.confidence.decision_impact_score
            score = (
                similarity * 100
                + record.confidence.importance * 10
                + recency * 1.5
                + record.confidence.trust_score * 5
                + max(0.0, influence) * 3
            )
            scored.append((score, id_))
        scored.sort(reverse=True)
        return [self.get(id_) for _, id_ in scored[:limit]]

    def verify(self, id_: str) -> MemoryRecord:
        record = self.get(id_)
        if record.immutable:
            return record
        confidence = MemoryConfidence(
            confidence=record.confidence.confidence,
            importance=record.confidence.importance,
            novelty=record.confidence.novelty,
            trust_score=record.confidence.trust_score,
            last_access=_now(),
            last_verified=_now(),
            created=record.confidence.created,
            source=record.confidence.source,
            verified=True,
            access_count=record.confidence.access_count + 1,
            verification_interval_days=record.confidence.verification_interval_days,
            expires_at=record.confidence.expires_at,
            source_reliability=record.confidence.source_reliability,
        )
        updated = MemoryRecord(
            id=record.id,
            kind=record.kind,
            content=record.content,
            confidence=confidence,
            tags=list(record.tags),
            relationships=list(record.relationships),
            experimental_group=record.experimental_group,
            hypothesis_id=record.hypothesis_id,
            outcome=record.outcome,
            tool=record.tool,
            model=record.model,
            version=record.version,
            immutable=record.immutable,
            status=record.status,
            revision_id=record.revision_id,
            revision_of=record.revision_of,
        )
        self._records[id_] = updated
        return updated

    def stale(self, id_: str) -> bool:
        record = self.get(id_)
        if record is None:
            return False
        now = _now()
        if record.confidence.expires_at and now >= record.confidence.expires_at:
            return True
        if record.confidence.verification_interval_days is None:
            return False
        if record.confidence.last_verified is None:
            return True
        window = record.confidence.verification_interval_days * 86400
        return (now - record.confidence.last_verified).total_seconds() > window

    def _access(self, id_: str) -> Optional[MemoryRecord]:
        record = self.get(id_)
        if record is None or record.immutable:
            return record
        updated = MemoryRecord(
            id=record.id,
            kind=record.kind,
            content=record.content,
            confidence=MemoryConfidence(
                confidence=record.confidence.confidence,
                importance=record.confidence.importance,
                novelty=record.confidence.novelty,
                trust_score=record.confidence.trust_score,
                last_access=_now(),
                last_verified=record.confidence.last_verified,
                created=record.confidence.created,
                source=record.confidence.source,
                verified=record.confidence.verified,
                access_count=record.confidence.access_count + 1,
                verification_interval_days=record.confidence.verification_interval_days,
                expires_at=record.confidence.expires_at,
                source_reliability=record.confidence.source_reliability,
                retrieval_count=record.confidence.retrieval_count + 1,
                decision_impact_score=record.confidence.decision_impact_score,
            ),
            tags=list(record.tags),
            relationships=list(record.relationships),
            experimental_group=record.experimental_group,
            hypothesis_id=record.hypothesis_id,
            outcome=record.outcome,
            tool=record.tool,
            model=record.model,
            version=record.version,
            immutable=record.immutable,
            status=record.status,
            revision_id=record.revision_id,
            revision_of=record.revision_of,
        )
        self._records[id_] = updated
        return updated

    def record_influence(self, id_: str, impact_delta: float) -> Optional[MemoryRecord]:
        record = self.get(id_)
        if record is None or record.immutable:
            return record
        new_score = influence_penalty(record.confidence.decision_impact_score, impact_delta)
        updated = MemoryRecord(
            id=record.id,
            kind=record.kind,
            content=record.content,
            confidence=MemoryConfidence(
                confidence=record.confidence.confidence,
                importance=record.confidence.importance,
                novelty=record.confidence.novelty,
                trust_score=record.confidence.trust_score,
                last_access=_now(),
                last_verified=record.confidence.last_verified,
                created=record.confidence.created,
                source=record.confidence.source,
                verified=record.confidence.verified,
                access_count=record.confidence.access_count + 1,
                verification_interval_days=record.confidence.verification_interval_days,
                expires_at=record.confidence.expires_at,
                source_reliability=record.confidence.source_reliability,
                retrieval_count=record.confidence.retrieval_count + 1,
                decision_impact_score=new_score,
            ),
            tags=list(record.tags),
            relationships=list(record.relationships),
            experimental_group=record.experimental_group,
            hypothesis_id=record.hypothesis_id,
            outcome=record.outcome,
            tool=record.tool,
            model=record.model,
            version=record.version,
            immutable=record.immutable,
            status=record.status,
            revision_id=record.revision_id,
            revision_of=record.revision_of,
        )
        self._records[id_] = updated
        return updated

    def active_reflection(self) -> Dict[str, Any]:
        reflections: List[Dict[str, Any]] = []
        preserved_count = 0
        failed_count = 0
        mistakes: List[str] = []
        for record in self._records.values():
            if record.kind == MemoryKind.REFLECTIVE:
                reflections.append({"id": record.id, "content": record.content})
            if record.kind == MemoryKind.EXPERIENCE and record.outcome == "success":
                preserved_count += 1
            if record.kind == MemoryKind.EXPERIENCE and record.outcome == "failure":
                failed_count += 1
                mistakes.append(record.content)
        return {
            "reflection_count": len(reflections),
            "experiences_preserved": preserved_count,
            "experiences_failed": failed_count,
            "mistakes": mistakes,
        }

    def _collect_current_goals(self) -> list:
        goals = []
        for record in self._records.values():
            if record.kind == MemoryKind.STRATEGIC:
                goals.append(record.content)
            if record.experimental_group:
                goals.append(record.content)
        return goals

    def _collect_statuses(self) -> tuple[list, list]:
        blocked = []
        completed = []
        for record in self._records.values():
            if record.status == MemoryStatus.COMPRESSED:
                blocked.append(record.id)
            tags = set(record.tags)
            if "completed" in tags or record.status == MemoryStatus.COMPRESSED:
                completed.append(record.id)
        return blocked, completed

    def _collect_dependencies(self) -> dict:
        deps = {}
        for record in self._records.values():
            if record.hypothesis_id and record.hypothesis_id not in deps:
                deps[record.hypothesis_id] = []
            if record.hypothesis_id:
                deps[record.hypothesis_id].append(record.id)
        return deps

    def goal_progress(self):
        goals = self._collect_current_goals()
        blocked, completed = self._collect_statuses()
        deps = self._collect_dependencies()
        return {
            "current_goals": goals,
            "blocked": blocked,
            "completed": completed,
            "dependencies": deps,
        }

    def health(self) -> MemoryHealth:
        if not self._records:
            return MemoryHealth()
        verified = sum(1 for r in self._records.values() if r.confidence.verified)
        avg_conf = sum(r.confidence.confidence for r in self._records.values()) / len(self._records)
        stale = sum(1 for r in self._records.values() if self.stale(r.id))
        retrievals = sum(r.confidence.retrieval_count for r in self._records.values())
        avg_influence = sum(r.confidence.decision_impact_score for r in self._records.values()) / max(1, len(self._records))
        return MemoryHealth(
            verified_facts=verified,
            unverified_facts=len(self._records) - verified,
            conflicts=len(self._contradiction_pairs),
            avg_confidence=avg_conf,
            duplicates=len(self._contradiction_pairs),
            growth_rate=self._ins / max(1, len(self._created_order)),
            decay_rate=self._deleted / max(1, len(self._created_order)),
            compression_ratio=sum(1 for r in self._records.values() if r.status == MemoryStatus.COMPRESSED) / max(1, len(self._records)),
            stale_records=stale,
            retrievals=retrievals,
            avg_decision_impact_score=avg_influence,
        )

    def _latest_revision_id(self, base_id: str) -> Optional[str]:
        revision_id = base_id
        for record in self._records.values():
            if record.revision_of == revision_id:
                candidate = self._latest_revision_id(record.id)
                if candidate:
                    return candidate
        return None

    def latest(self, id_: str) -> Optional[MemoryRecord]:
        revision_id = self._latest_revision_id(id_)
        if revision_id is None:
            revision_id = id_
        return self.get(revision_id)

    def consolidate(self, kind: str, *, min_items: int = 3, summary_kind: str = MemoryKind.PROCEDURAL) -> List[MemoryRecord]:
        clusters: Dict[str, List[MemoryRecord]] = {}
        for record in self._records.values():
            if record.kind != kind or record.status == MemoryStatus.DELETED:
                continue
            if not record.tags:
                continue
            key = tuple(sorted(record.tags))
            clusters.setdefault(key, []).append(record)
        summaries: List[MemoryRecord] = []
        for tag_key, records in clusters.items():
            if len(records) < min_items:
                continue
            top = sorted(records, key=lambda item: item.confidence.confidence, reverse=True)
            summary = add_record(
                MemoryRecord(
                    id=f"consolidated-{kind}-{'-'.join(tag_key)}",
                    kind=summary_kind,
                    content=" | ".join(item.content for item in top[:5]),
                    confidence=MemoryConfidence(confidence=min(1.0, top[0].confidence.confidence + 0.1), importance=0.9, trust_score=top[0].confidence.trust_score),
                    tags=list(tag_key),
                    relationships=[r.id for r in records[:5]],
                    tool=top[0].tool,
                    model=top[0].model,
                    version=top[0].version,
                    status=MemoryStatus.ACTIVE,
                )
            )
            for record in records:
                self.mark_status(record.id, MemoryStatus.ARCHIVED)
                self._records[record.id + "-revision"] = MemoryRecord(
                    id=record.id + "-revision",
                    kind=record.kind,
                    content=record.content,
                    confidence=record.confidence,
                    tags=list(record.tags),
                    relationships=list(record.relationships),
                    experimental_group=record.experimental_group,
                    hypothesis_id=record.hypothesis_id,
                    outcome=record.outcome,
                    tool=record.tool,
                    model=record.model,
                    version=record.version,
                    immutable=record.immutable,
                    status=MemoryStatus.ARCHIVED,
                    revision_id=summary.id,
                    revision_of=record.id,
                )
            summaries.append(summary)
        return summaries

def add_record(record: MemoryRecord) -> MemoryRecord:
    return record
