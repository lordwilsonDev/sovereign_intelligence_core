"""Cached peer health with TTL to avoid repeated slow timeouts."""
from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple


class PeerHealthCache:
    """TTL cache for peer health results."""

    def __init__(self, ttl_seconds: int = 60) -> None:
        self.ttl = ttl_seconds
        self._cache: Dict[Tuple[str, str, int], Tuple[float, Dict[str, Any]]] = {}

    def get(self, node_id: str, address: str, port: int) -> Optional[Dict[str, Any]]:
        entry = self._cache.get((node_id, address, port))
        if not entry:
            return None
        ts, body = entry
        if time.time() - ts > self.ttl:
            self._cache.pop((node_id, address, port), None)
            return None
        return body

    def put(self, node_id: str, address: str, port: int, body: Dict[str, Any]) -> None:
        self._cache[(node_id, address, port)] = (time.time(), body)
