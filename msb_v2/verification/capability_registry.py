from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class CapabilityBenchmark:
    name: str
    description: str
    test_fn: Callable[[], float]
    last_score: float = 0.0
    last_run: Optional[float] = None
    history: List[float] = field(default_factory=list)

    def run(self) -> float:
        score = float(self.test_fn())
        self.last_score = score
        self.last_run = time.time()
        self.history.append(score)
        if len(self.history) > 100:
            self.history.pop(0)
        return score


class CapabilityRegistry:
    def __init__(self) -> None:
        self._benchmarks: Dict[str, CapabilityBenchmark] = {}

    def register(self, name: str, description: str, test_fn: Callable[[], float]) -> None:
        if name in self._benchmarks:
            raise ValueError(f"Benchmark {name} already registered")
        self._benchmarks[name] = CapabilityBenchmark(name, description, test_fn)

    def run_benchmark(self, name: str) -> float:
        bench = self._benchmarks.get(name)
        if not bench:
            raise ValueError(f"Unknown benchmark: {name}")
        return bench.run()

    def run_all(self) -> Dict[str, float]:
        return {name: bench.run() for name, bench in self._benchmarks.items()}

    def get_scores(self) -> Dict[str, float]:
        return {name: bench.last_score for name, bench in self._benchmarks.items()}

    def get_history(self, name: str) -> List[float]:
        bench = self._benchmarks.get(name)
        if not bench:
            raise ValueError(f"Unknown benchmark: {name}")
        return list(bench.history)
