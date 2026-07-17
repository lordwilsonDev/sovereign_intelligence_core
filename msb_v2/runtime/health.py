from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from msb_v2.runtime.resources import ResourceManager


@dataclass(frozen=True)
class HealthRecord:
    status: str
    detail: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class HealthManager:
    def __init__(self, *, check_interval: float = 10.0) -> None:
        self.check_interval = check_interval
        self._lock = threading.Lock()
        self._history: List[HealthRecord] = []
        self._last_check: Optional[float] = None

    def record(self, status: str, detail: str = "", **metadata: Any) -> HealthRecord:
        record = HealthRecord(status=status, detail=detail, metadata=metadata)
        with self._lock:
            self._history.append(record)
            self._last_check = time.time()
        return record

    def latest(self) -> Dict[str, Any]:
        with self._lock:
            if not self._history:
                return {"status": "unknown", "check_count": 0}
            current = self._history[-1]
            return {
                "status": current.status,
                "detail": current.detail,
                "metadata": current.metadata,
                "check_count": len(self._history),
                "last_check": self._last_check,
            }

    def summary(self) -> Dict[str, Any]:
        latest = self.latest()
        resource_snapshot = self._resource_snapshot()
        return {
            "health": latest,
            "resources": resource_snapshot,
            "capabilities": self._capability_status(),
        }

    def _resource_snapshot(self) -> Dict[str, Any]:
        try:
            resource = ResourceManager()
            return resource.snapshot()
        except Exception:
            return {"error": "resource manager unavailable"}

    def _capability_status(self) -> Dict[str, Any]:
        return {
            "event_log": "enabled",
            "worker_pool": "available",
            "reasoning_scorer": self._bool_from_env("MSB_REASONING_SCORER", False),
        }

    @staticmethod
    def _bool_from_env(name: str, default: bool) -> bool:
        value = os.getenv(name, "")
        if not value:
            return default
        return value.lower() not in {"false", "0", "no", "off"}
