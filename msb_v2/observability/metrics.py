from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union


class MetricsCollector:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: Dict[str, float] = {}
        self._gauges: Dict[str, float] = {}
        self._timers: Dict[str, List[float]] = {}

    def increment(self, name: str, amount: float = 1.0) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0.0) + amount

    def set_gauge(self, name: str, value: float) -> None:
        with self._lock:
            self._gauges[name] = value

    def record(self, name: str, duration_ms: float) -> None:
        with self._lock:
            self._timers.setdefault(name, []).append(duration_ms)

    def timer_summary(self, name: str) -> Dict[str, Optional[float]]:
        with self._lock:
            values = list(self._timers.get(name, []))
        if not values:
            return {"count": 0.0, "p50": None, "p95": None, "max": None, "mean": None}
        values.sort()
        count = len(values)
        return {
            "count": float(count),
            "p50": values[int(count * 0.5)],
            "p95": values[min(int(count * 0.95), count - 1)],
            "max": values[-1],
            "mean": sum(values) / count,
        }

    def snapshot(self) -> Dict[str, Union[Dict[str, float], Dict[str, Dict[str, Optional[float]]]]]:
        with self._lock:
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "timer_summaries": {k: self.timer_summary_unlocked(k) for k in self._timers},
            }

    def timer_summary_unlocked(self, name: str) -> Dict[str, Optional[float]]:
        values = list(self._timers.get(name, []))
        if not values:
            return {"count": 0.0, "p50": None, "p95": None, "max": None, "mean": None}
        values.sort()
        count = len(values)
        return {
            "count": float(count),
            "p50": values[int(count * 0.5)],
            "p95": values[min(int(count * 0.95), count - 1)],
            "max": values[-1],
            "mean": sum(values) / count,
        }


_collector: Optional[MetricsCollector] = None
_lock = threading.Lock()


def get_collector() -> MetricsCollector:
    global _collector
    if _collector is None:
        with _lock:
            if _collector is None:
                _collector = MetricsCollector()
    return _collector
