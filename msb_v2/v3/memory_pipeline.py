from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass(frozen=True)
class MemoryEntry:
    memory_id: str
    source: str
    content: str
    memory_type: str = "episodic"
    importance: float = 0.5
    created_at: str = ""


class InMemoryStore:
    def __init__(self) -> None:
        self._items: List[MemoryEntry] = []

    def add(self, entry: MemoryEntry) -> bool:
        self._items.append(entry)
        return True

    def add_many(self, entries: List[MemoryEntry]) -> List[MemoryEntry]:
        added: List[MemoryEntry] = []
        for e in entries:
            if self.add(e):
                added.append(e)
        return added

    def recent(self, limit: int = 20) -> List[MemoryEntry]:
        return list(reversed(self._items))[:limit]

    def search(self, query: str, limit: int = 20) -> List[MemoryEntry]:
        q = query.casefold().strip()
        if not q:
            return self.all()[:limit]
        scored = []
        for e in self._items:
            text = f"{e.source} {e.content} {e.memory_type}".casefold()
            scored.append((text.count(q), e))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for score, e in scored[:limit] if score > 0]

    def all(self) -> List[MemoryEntry]:
        return list(self._items)


class EventToMemoryPipeline:
    def __init__(self, store: Any) -> None:
        self.store = store

    def ingest(self, source: str, content: str, memory_type: str = "episodic", importance: float = 0.5) -> MemoryEntry:
        entry = MemoryEntry(
            memory_id=f"{source}:{len(content)}",
            source=source,
            content=content,
            memory_type=memory_type,
            importance=importance,
        )
        self.store.add(entry)
        return entry

    def ingest_batch(self, items: List[dict]) -> List[MemoryEntry]:
        entries: List[MemoryEntry] = []
        for item in items:
            entries.append(self.ingest(
                source=item.get("source", "unknown"),
                content=item.get("content", ""),
                memory_type=item.get("memory_type", "episodic"),
                importance=float(item.get("importance", 0.5)),
            ))
        return entries

    def recall(self, query: str, limit: int = 20) -> List[MemoryEntry]:
        return self.store.search(query, limit=limit)

    def recent(self, limit: int = 20) -> List[MemoryEntry]:
        return self.store.recent(limit)


class MemoryEnhancedPlanner:
    def __init__(self, pipeline: Any, learning_engine: Any = None) -> None:
        self.pipeline = pipeline
        self.learning_engine = learning_engine

    def plan(self, task: str, context: Optional[str] = None) -> dict:
        seen: List[MemoryEntry] = []
        seen_ids: set[str] = set()
        terms = [t for t in task.split() if t]
        for term in terms:
            for mem in self.pipeline.recall(term, limit=10):
                mid = mem.memory_id
                if mid not in seen_ids:
                    seen_ids.add(mid)
                    seen.append(mem)
        if not seen and context:
            terms_ctx = [t for t in context.split() if t]
            for term in terms_ctx:
                for mem in self.pipeline.recall(term, limit=10):
                    mid = mem.memory_id
                    if mid not in seen_ids:
                        seen_ids.add(mid)
                        seen.append(mem)
        recent = self.pipeline.recent(limit=5)
        scored = sorted(seen, key=lambda m: m.importance, reverse=True)
        next_step = None
        if self.learning_engine and scored:
            try:
                rec = self.learning_engine.recommend(scored[0].source)
                next_step = rec.get("next")
            except Exception:
                next_step = None
        return {
            "task": task,
            "context": context,
            "recalled_count": len(scored),
            "recalled_sources": [m.source for m in scored],
            "recent_sources": [m.source for m in recent],
            "next_step": next_step,
            "plan": self._synthesize(task, scored, recent, next_step),
        }

    @staticmethod
    def _synthesize(task: str, memories: List[MemoryEntry], recent: List[MemoryEntry], next_step: Optional[str]) -> str:
        if not memories and not recent:
            return f"Direct execution: {task}"
        if memories:
            base = f"Apply learned pattern from {memories[0].source} to {task}"
            if next_step:
                return f"{base}; next recommended step: {next_step}"
            return base
        return f"Continue recent trajectory on {task} using {recent[0].source}"
