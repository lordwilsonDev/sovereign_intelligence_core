from __future__ import annotations

import threading
from typing import Any, Dict, Optional


class ResourceManager:
    def __init__(
        self,
        *,
        max_cpu_percent: float = 80.0,
        max_memory_mb: Optional[int] = None,
    ) -> None:
        self.max_cpu_percent = max_cpu_percent
        self.max_memory_mb = max_memory_mb
        self._lock = threading.Lock()
        self._active: Dict[str, Dict[str, Any]] = {}

    def acquire(self, job_id: str, estimated_mb: Optional[int] = None) -> bool:
        with self._lock:
            if self.max_memory_mb is not None:
                current = sum(item.get("memory_mb", 0) for item in self._active.values())
                if current + (estimated_mb or 0) > self.max_memory_mb:
                    return False
            self._active[job_id] = {
                "memory_mb": estimated_mb or 0,
                "cpu_hint": 0.0,
            }
            return True

    def release(self, job_id: str) -> None:
        with self._lock:
            self._active.pop(job_id, None)

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "max_cpu_percent": self.max_cpu_percent,
                "max_memory_mb": self.max_memory_mb,
                "active_jobs": len(self._active),
                "reserved_memory_mb": sum(item.get("memory_mb", 0) for item in self._active.values()),
            }
