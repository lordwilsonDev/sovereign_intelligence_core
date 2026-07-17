from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from msb_v2.memory.types import MemoryConfidence, MemoryHealth, MemoryKind, MemoryRecord, MemoryStatus, influence_penalty


def _now() -> datetime:
    return datetime.now()


def _row_to_record(row: Dict[str, Any]) -> MemoryRecord:
    confidence = MemoryConfidence(
        confidence=row["confidence"],
        importance=row["importance"],
        novelty=row["novelty"],
        trust_score=row["trust_score"],
        last_access=_datetime_from(row["last_access"]),
        last_verified=_datetime_from(row["last_verified"]),
        created=_datetime_from(row["created"]),
        source=row["source"],
        verified=bool(row["verified"]),
        access_count=int(row["access_count"]),
        verification_interval_days=row["verification_interval_days"],
        expires_at=_datetime_from(row["expires_at"]),
        source_reliability=row["source_reliability"],
        retrieval_count=int(row["retrieval_count"]),
        decision_impact_score=row["decision_impact_score"],
    )
    return MemoryRecord(
        id=row["id"],
        kind=row["kind"],
        content=row["content"],
        confidence=confidence,
        tags=_json_list(row["tags"]),
        relationships=_json_list(row["relationships"]),
        experimental_group=row.get("experimental_group"),
        hypothesis_id=row.get("hypothesis_id"),
        outcome=row.get("outcome"),
        tool=row.get("tool"),
        model=row.get("model"),
        version=row.get("version"),
        immutable=bool(row["immutable"]),
        status=row["status"],
        revision_id=row.get("revision_id"),
        revision_of=row.get("revision_of"),
        integrity_hash=row.get("integrity_hash"),
        provenance=row.get("provenance"),
    )


def _datetime_from(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _json_list(value: Optional[str]) -> List[str]:
    if not value:
        return []
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return []


def _schema(path: str) -> None:
    conn = sqlite3.connect(path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS memory (
            id TEXT PRIMARY KEY,
            kind TEXT NOT NULL,
            content TEXT NOT NULL,
            confidence REAL DEFAULT 0.5,
            importance REAL DEFAULT 0.5,
            novelty REAL DEFAULT 0.5,
            trust_score REAL DEFAULT 0.5,
            last_access TEXT,
            last_verified TEXT,
            created TEXT NOT NULL,
            source TEXT DEFAULT 'runtime',
            verified INTEGER DEFAULT 0,
            access_count INTEGER DEFAULT 0,
            verification_interval_days INTEGER,
            expires_at TEXT,
            source_reliability REAL DEFAULT 0.5,
            retrieval_count INTEGER DEFAULT 0,
            decision_impact_score REAL DEFAULT 0.0,
            tags TEXT DEFAULT '[]',
            relationships TEXT DEFAULT '[]',
            experimental_group TEXT,
            hypothesis_id TEXT,
            outcome TEXT,
            tool TEXT,
            model TEXT,
            version TEXT,
            immutable INTEGER DEFAULT 0,
            status TEXT DEFAULT 'active',
            revision_id TEXT,
            revision_of TEXT,
            integrity_hash TEXT,
            provenance TEXT
        )
        """
    )
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_memory_id ON memory(id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_status ON memory(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_memory_kind ON memory(kind)")
    conn.commit()
    conn.close()


class PersistentMemoryStore:
    def __init__(self, path: str = "./memory_store.db") -> None:
        self.path = str(Path(path).resolve())
        self._lock = threading.Lock()
        _schema(self.path)

    def add(self, record: MemoryRecord) -> MemoryRecord:
        with self._lock:
            conn = sqlite3.connect(self.path)
            conn.execute(
                """
                INSERT OR REPLACE INTO memory (
                    id, kind, content, confidence, importance, novelty, trust_score, last_access, last_verified, created, source,
                    verified, access_count, verification_interval_days, expires_at, source_reliability, retrieval_count, decision_impact_score,
                    tags, relationships, experimental_group, hypothesis_id, outcome, tool, model, version, immutable, status,
                    revision_id, revision_of, integrity_hash, provenance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.kind,
                    record.content,
                    record.confidence.confidence,
                    record.confidence.importance,
                    record.confidence.novelty,
                    record.confidence.trust_score,
                    record.confidence.last_access.isoformat() if record.confidence.last_access else None,
                    record.confidence.last_verified.isoformat() if record.confidence.last_verified else None,
                    record.confidence.created.isoformat(),
                    record.confidence.source,
                    int(record.confidence.verified),
                    record.confidence.access_count,
                    record.confidence.verification_interval_days,
                    record.confidence.expires_at.isoformat() if record.confidence.expires_at else None,
                    record.confidence.source_reliability,
                    record.confidence.retrieval_count,
                    record.confidence.decision_impact_score,
                    json.dumps(record.tags),
                    json.dumps(record.relationships),
                    record.experimental_group,
                    record.hypothesis_id,
                    record.outcome,
                    record.tool,
                    record.model,
                    record.version,
                    int(record.immutable),
                    record.status,
                    record.revision_id,
                    record.revision_of,
                    record.integrity_hash,
                    json.dumps(record.provenance),
            ),
            )
            conn.commit()
            conn.close()
        return record

    def get(self, id_: str) -> Optional[MemoryRecord]:
        with self._lock, sqlite3.connect(self.path) as conn:
            cursor = conn.execute("SELECT * FROM memory WHERE id = ?", (id_,))
            row = cursor.fetchone()
            if row is None:
                return None
            column_names = [description[0] for description in cursor.description]
        return _row_to_record(dict(zip(column_names, row)))

    def _apply(self, record: MemoryRecord) -> None:
        with self._lock, sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                UPDATE memory SET
                    kind = ?, content = ?, confidence = ?, importance = ?, novelty = ?, trust_score = ?,
                    last_access = ?, last_verified = ?, status = ?, tags = ?, relationships = ?,
                    experimental_group = ?, hypothesis_id = ?, outcome = ?, tool = ?, model = ?, version = ?,
                    immutable = ?, revision_id = ?, revision_of = ?, integrity_hash = ?, provenance = ?
                WHERE id = ?
                """,
                (
                    record.kind,
                    record.content,
                    record.confidence.confidence,
                    record.confidence.importance,
                    record.confidence.novelty,
                    record.confidence.trust_score,
                    record.confidence.last_access.isoformat() if record.confidence.last_access else None,
                    record.confidence.last_verified.isoformat() if record.confidence.last_verified else None,
                    record.status,
                    json.dumps(record.tags),
                    json.dumps(record.relationships),
                    record.experimental_group,
                    record.hypothesis_id,
                    record.outcome,
                    record.tool,
                    record.model,
                    record.version,
                    int(record.immutable),
                    record.revision_id,
                    record.revision_of,
                    record.integrity_hash,
                    record.provenance,
                    record.id,
                ),
            )
            conn.execute("COMMIT")

    def mark_status(self, id_: str, status: str) -> Optional[MemoryRecord]:
        record = self.get(id_)
        if record is None or record.immutable:
            return record
        return self.add(
            MemoryRecord(
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
                revision_id=record.revision_id,
                revision_of=record.revision_of,
                integrity_hash=record.integrity_hash,
                provenance=record.provenance,
            )
        )

    def search(self, query: str, *, limit: int = 20) -> List[MemoryRecord]:
        rows: List[Dict[str, Any]] = []
        with self._lock, sqlite3.connect(self.path) as conn:
            cursor = conn.execute(
                """
                SELECT id, kind, content, confidence AS confidence, importance, novelty, trust_score,
                       tags, status, created
                FROM memory
                WHERE status != ?
                LIMIT ?
                """,
                (MemoryStatus.DELETED, limit * 4),
            )
            column_names = [description[0] for description in cursor.description]
            rows = [dict(zip(column_names, row)) for row in cursor.fetchall()]

        q = query.strip().casefold()
        if not q:
            return rows[:limit]

        scored: List[tuple[float, MemoryRecord]] = []
        for row in rows:
            record = _row_to_record(row)
            text = f"{record.content} {' '.join(record.tags)}".casefold()
            matches = text.count(q)
            if matches == 0:
                continue
            score = matches * 10.0 + record.confidence.importance * 5.0
            scored.append((score, record))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [record for _, record in scored[:limit]]

    def trust_score(self, id_: str) -> float:
        record = self.get(id_)
        if record is None:
            return 0.0
        from msb_v2.memory.store import _default_decay
        age_hours = max((_now() - record.confidence.created).total_seconds() / 3600.0, 0.0)
        decayed = _default_decay(record.confidence.confidence, age_hours)
        return decayed * record.confidence.trust_score

    def detect_contradictions(self, new_record: MemoryRecord) -> List[str]:
        conflicts: List[str] = []
        if new_record.kind != MemoryKind.SEMANTIC:
            return conflicts
        needle = new_record.content.strip()
        with self._lock, sqlite3.connect(self.path) as conn:
            cursor = conn.execute(
                "SELECT id, content FROM memory WHERE kind = ? AND status != ?",
                (MemoryKind.SEMANTIC, MemoryStatus.DELETED),
            )
            rows = cursor.fetchall()
        for existing_id, content in rows:
            if existing_id == new_record.id:
                continue
            if content.strip() == needle:
                continue
            if needle in content or content in needle:
                conflicts.append(existing_id)
        return conflicts

    def refresh(self, id_: str) -> Optional[MemoryRecord]:
        record = self.get(id_)
        if record is None or record.immutable:
            return record
        age_hours = (_now() - record.confidence.created).total_seconds() / 3600.0
        if age_hours > 24:
            return self.mark_status(id_, MemoryStatus.ARCHIVED)
        return record

    def verify(self, id_: str) -> Optional[MemoryRecord]:
        record = self.get(id_)
        if record is None or record.immutable:
            return record
        return self.add(
            MemoryRecord(
                id=record.id,
                kind=record.kind,
                content=record.content,
                confidence=MemoryConfidence(
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
                status=record.status,
                revision_id=record.revision_id,
                revision_of=record.revision_of,
                integrity_hash=record.integrity_hash,
                provenance=record.provenance,
            )
        )

    def record_influence(self, id_: str, impact_delta: float) -> Optional[MemoryRecord]:
        record = self.get(id_)
        if record is None or record.immutable:
            return record
        return self.add(
            MemoryRecord(
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
                    decision_impact_score=influence_penalty(record.confidence.decision_impact_score, impact_delta),
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
                integrity_hash=record.integrity_hash,
                provenance=record.provenance,
            )
        )

    def active_reflection(self) -> Dict[str, Any]:
        reflective: List[Dict[str, Any]] = []
        preserved = 0
        failed = 0
        mistakes: List[str] = []
        with self._lock, sqlite3.connect(self.path) as conn:
            cursor = conn.execute("SELECT id, kind, content, outcome FROM memory WHERE status != ?", (MemoryStatus.DELETED,))
            rows = cursor.fetchall()
        for id_, kind, content, outcome in rows:
            if kind == MemoryKind.REFLECTIVE:
                reflective.append({"id": id_, "content": content})
            if kind == MemoryKind.EXPERIENCE and outcome == "success":
                preserved += 1
            if kind == MemoryKind.EXPERIENCE and outcome == "failure":
                failed += 1
                mistakes.append(content)
        return {
            "reflection_count": len(reflective),
            "experiences_preserved": preserved,
            "experiences_failed": failed,
            "mistakes": mistakes,
        }

    def health(self) -> MemoryHealth:
        with self._lock, sqlite3.connect(self.path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM memory WHERE status != ?", (MemoryStatus.DELETED,))
            total = cursor.fetchone()[0]
            if total == 0:
                return MemoryHealth()
            cursor = conn.execute("SELECT verified, confidence, created FROM memory WHERE status != ?", (MemoryStatus.DELETED,))
            rows = cursor.fetchall()

        now = _now()
        verified = 0
        stale = 0
        retrievals = 0
        influence_sum = 0.0
        confidence_sum = 0.0
        for row in rows:
            verified_flag, confidence, created = row
            if verified_flag:
                verified += 1
            confidence_sum += confidence
            created_dt = _datetime_from(created)
            if created_dt and (now - created_dt).total_seconds() / 3600 > 24:
                stale += 1
            retrievals += 1
            influence_sum += 0.0
        return MemoryHealth(
            verified_facts=verified,
            unverified_facts=total - verified,
            avg_confidence=confidence_sum / max(1, total),
            stale_records=stale,
            retrievals=retrievals,
            avg_decision_impact_score=influence_sum / max(1, total),
        )

    def all(self, *, exclude_deleted: bool = True) -> List[MemoryRecord]:
        return list(self.iter_all(exclude_deleted=exclude_deleted))

    def iter_all(self, *, exclude_deleted: bool = True) -> Iterator[MemoryRecord]:
        with self._lock, sqlite3.connect(self.path) as conn:
            query = "SELECT * FROM memory"
            if exclude_deleted:
                query += " WHERE status != ?"
                cursor = conn.execute(query, (MemoryStatus.DELETED,))
            else:
                cursor = conn.execute(query)
            column_names = [description[0] for description in cursor.description]
        for row in cursor:
            yield _row_to_record(dict(zip(column_names, row)))
    pass
