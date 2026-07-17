from __future__ import annotations

from typing import Any, Dict, List, Optional

from msb_v2.memory.store import MemoryStore
from msb_v2.memory.types import MemoryRecord, MemoryStatus, MemoryKind


class NoeticShard:
    """A privacy-preserving memory partition backed by in-process MemoryStore state."""

    def __init__(self, shard_id: str, *, allowed_tags: Optional[List[str]] = None) -> None:
        self.shard_id = shard_id
        self.allowed_tags = set(allowed_tags or [])
        self.store = MemoryStore()
        self._record_shard_map: Dict[str, str] = {}

    def _tag_allowed(self, record: MemoryRecord) -> bool:
        if not self.allowed_tags:
            return True
        return bool(set(record.tags) & self.allowed_tags)

    def add(self, record: MemoryRecord) -> str:
        if not self._tag_allowed(record):
            raise PermissionError(f"shard {self.shard_id} rejects tag filter for {record.id}")
        id_ = self.store.add(record)
        self._record_shard_map[id_] = self.shard_id
        return id_

    def get(self, id_: str) -> Optional[MemoryRecord]:
        if self._record_shard_map.get(id_) != self.shard_id:
            return None
        return self.store.get(id_)

    def search(self, query: str, *, limit: int = 20) -> List[MemoryRecord]:
        results = []
        for record in self.store.search(query, limit=limit):
            if self._record_shard_map.get(record.id) == self.shard_id:
                results.append(record)
        return results[:limit]

    def mark_status(self, id_: str, status: str) -> None:
        if self._record_shard_map.get(id_) != self.shard_id:
            raise KeyError(f"record {id_} not in shard {self.shard_id}")
        self.store.mark_status(id_, status)

    def health(self) -> Dict[str, Any]:
        active = 0
        for id_ in self._record_shard_map:
            if self._record_shard_map[id_] == self.shard_id and self.store.get(id_) is not None:
                active += 1
        return {
            "shard_id": self.shard_id,
            "active_records": active,
            "allowed_tags": sorted(self.allowed_tags),
        }

    def archive(self, id_: str) -> None:
        self.mark_status(id_, MemoryStatus.ARCHIVED)

    def consolidate(self, kind, *, min_items: int = 3) -> List[MemoryRecord]:
        kind = getattr(kind, "value", kind)
        if kind not in {v for k, v in vars(MemoryKind).items() if isinstance(v, str)}:
            raise ValueError(f"unknown memory kind: {kind}")
        summaries: List[MemoryRecord] = []
        kind_records = [
            rec for rec in self.store._records.values()
            if rec.kind == kind and self._record_shard_map.get(rec.id) == self.shard_id
            and rec.status != MemoryStatus.DELETED
            and rec.status != MemoryStatus.ARCHIVED
        ]
        if len(kind_records) < min_items:
            return summaries
        grouped = {}
        for record in kind_records:
            grouped.setdefault(tuple(sorted(record.tags)), []).append(record)
        for tag_key, records in grouped.items():
            if len(records) < min_items:
                continue
            top = sorted(records, key=lambda item: item.confidence.confidence, reverse=True)
            from msb_v2.memory.store import add_record
            summary = add_record(
                MemoryRecord(
                    id=f"consolidated-{self.shard_id}-{kind}-{'-'.join(tag_key)}",
                    kind=MemoryKind.PROCEDURAL,
                    content=" | ".join(item.content for item in top[:5]),
                    confidence=top[0].confidence,
                    tags=list(tag_key),
                    relationships=[r.id for r in records[:5]],
                    tool=top[0].tool,
                    model=top[0].model,
                    version=top[0].version,
                    status=MemoryStatus.ACTIVE,
                )
            )
            for record in records:
                self.archive(record.id)
            self._record_shard_map[summary.id] = self.shard_id
            summaries.append(summary)
        return summaries


class NoeticStore:
    """Privacy-preserving memory partitioning layer."""

    def __init__(self) -> None:
        self._shards: Dict[str, NoeticShard] = {}

    def create_shard(self, shard_id: str, *, allowed_tags: Optional[List[str]] = None) -> NoeticShard:
        if shard_id in self._shards:
            return self._shards[shard_id]
        shard = NoeticShard(shard_id, allowed_tags=allowed_tags)
        self._shards[shard_id] = shard
        return shard

    def get_shard(self, shard_id: str) -> NoeticShard:
        if shard_id not in self._shards:
            raise KeyError(f"unknown shard: {shard_id}")
        return self._shards[shard_id]

    def shard_health(self) -> Dict[str, Any]:
        return {sid: shard.health() for sid, shard in self._shards.items()}
