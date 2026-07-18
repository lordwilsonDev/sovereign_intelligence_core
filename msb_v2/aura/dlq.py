from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DeadLetterEntry:
    entry_id: str
    payload: dict[str, Any]
    reason: str = ""


class DeadLetterQueue:
    def __init__(self, maxlen: int = 500) -> None:
        self._items: list[DeadLetterEntry] = []
        self._lock = threading.Lock()
        self._maxlen = maxlen
        self._seq = 0

    def enqueue(self, payload: dict[str, Any], reason: str = "") -> DeadLetterEntry:
        with self._lock:
            self._seq += 1
            entry = DeadLetterEntry(entry_id=f"dlq-{self._seq}", payload=payload, reason=reason)
            self._items.append(entry)
            if len(self._items) > self._maxlen:
                self._items.pop(0)
            return entry

    def drain(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._lock:
            items = self._items[:limit]
            self._items = self._items[len(items):]
            return [{"entry_id": i.entry_id, "reason": i.reason, "payload": i.payload} for i in items]

    def snapshot(self) -> list[dict[str, Any]]:
        with self._lock:
            return [{"entry_id": i.entry_id, "reason": i.reason, "payload": i.payload} for i in self._items]

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)
