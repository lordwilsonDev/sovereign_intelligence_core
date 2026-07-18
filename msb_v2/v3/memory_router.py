from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from typing import Any, Dict, List, Optional


class MemoryKind(str, Enum):
    WORKING = "working"
    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"
    EXECUTION = "execution"
    FAILURE = "failure"
    REFLECTIVE = "reflective"
    ARCHIVE = "archive"


class MemoryTier(str, Enum):
    RAM = "ram"
    SQLITE = "sqlite"
    SNAPSHOT = "snapshot"


@dataclass(frozen=True)
class MemoryRoute:
    kind: MemoryKind
    tier: MemoryTier
    retention: timedelta
    max_entries: Optional[int] = None


_DEFAULT_ROUTES: List[MemoryRoute] = [
    MemoryRoute(kind=MemoryKind.WORKING, tier=MemoryTier.RAM, retention=timedelta(minutes=30), max_entries=200),
    MemoryRoute(kind=MemoryKind.SEMANTIC, tier=MemoryTier.SQLITE, retention=timedelta(days=365), max_entries=5000),
    MemoryRoute(kind=MemoryKind.EPISODIC, tier=MemoryTier.SQLITE, retention=timedelta(days=90), max_entries=2000),
    MemoryRoute(kind=MemoryKind.PROCEDURAL, tier=MemoryTier.SQLITE, retention=timedelta(days=180), max_entries=1000),
    MemoryRoute(kind=MemoryKind.EXECUTION, tier=MemoryTier.SNAPSHOT, retention=timedelta(days=30), max_entries=300),
    MemoryRoute(kind=MemoryKind.FAILURE, tier=MemoryTier.SQLITE, retention=timedelta(days=90), max_entries=1000),
    MemoryRoute(kind=MemoryKind.REFLECTIVE, tier=MemoryTier.SQLITE, retention=timedelta(days=365), max_entries=2000),
    MemoryRoute(kind=MemoryKind.ARCHIVE, tier=MemoryTier.SNAPSHOT, retention=timedelta(days=3650), max_entries=10000),
]


class MemoryRouter:
    def __init__(self, routes: Optional[List[MemoryRoute]] = None) -> None:
        self._routes = routes or list(_DEFAULT_ROUTES)

    def route(self, kind: MemoryKind) -> MemoryRoute:
        for route in self._routes:
            if route.kind == kind:
                return route
        raise ValueError(f"No memory route for kind: {kind.value}")

    def route_by_access_pattern(self, query: str, ttl_hours: Optional[float] = None) -> MemoryRoute:
        q = query.casefold()
        if "how" in q or "procedure" in q or "steps" in q:
            return self.route(MemoryKind.PROCEDURAL)
        if "error" in q or "failed" in q or "failure" in q:
            return self.route(MemoryKind.FAILURE)
        if "reflect" in q or "learn" in q or "improve" in q:
            return self.route(MemoryKind.REFLECTIVE)
        if any(token in q for token in ["recent", "last", "current", "today", "now"]):
            return self.route(MemoryKind.WORKING)
        if ttl_hours is not None and ttl_hours < 2:
            return self.route(MemoryKind.WORKING)
        return self.route(MemoryKind.SEMANTIC)

    def summary(self) -> Dict[str, Any]:
        return {
            "routes": [
                {
                    "kind": r.kind.value,
                    "tier": r.tier.value,
                    "retention_hours": round(r.retention.total_seconds() / 3600.0, 2),
                    "max_entries": r.max_entries,
                }
                for r in self._routes
            ]
        }
