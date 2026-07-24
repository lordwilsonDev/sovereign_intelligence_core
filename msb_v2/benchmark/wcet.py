"""M4 WCET benchmarking for refactor validation."""
from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional


@dataclass
class WCETResult:
    function: str
    runs: int
    median_ms: float
    p95_ms: float
    max_ms: float


class WCETBenchmark:
    """Measures worst-case execution time for refactored functions."""

    def __init__(self, runs: int = 50):
        self.runs = runs

    def measure(self, func: Callable[[], None], name: Optional[str] = None) -> WCETResult:
        name = name or getattr(func, "__qualname__", getattr(func, "__name__", "anonymous"))
        samples: List[float] = []
        for _ in range(self.runs):
            start = time.perf_counter()
            func()
            samples.append((time.perf_counter() - start) * 1000)
        samples.sort()
        p95_index = max(0, min(int(len(samples) * 0.95), len(samples) - 1))
        return WCETResult(
            function=name,
            runs=self.runs,
            median_ms=statistics.median(samples),
            p95_ms=samples[p95_index],
            max_ms=max(samples),
        )
