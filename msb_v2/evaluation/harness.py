"""Small regression harness for deterministic model evaluations."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Protocol


class PredictiveModel(Protocol):
    def predict(self, value: Any) -> Any: ...


@dataclass(frozen=True)
class EvalCase:
    id: str
    input: Any
    expected: Any


@dataclass(frozen=True)
class EvalResult:
    case_id: str
    passed: bool
    latency_ms: float


@dataclass(frozen=True)
class EvalReport:
    results: tuple[EvalResult, ...]

    @property
    def accuracy(self) -> float:
        return sum(result.passed for result in self.results) / len(self.results) if self.results else 0.0


class EvalHarness:
    def __init__(self, cases: list[EvalCase], scorer: Callable[[Any, Any], bool] | None = None) -> None:
        self.cases = cases
        self.scorer = scorer or (lambda expected, actual: expected == actual)

    def run(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def regression_check(self, candidate: PredictiveModel, baseline: PredictiveModel, tolerance: float = 0.02) -> bool:
        return self.run(candidate).accuracy >= self.run(baseline).accuracy - tolerance
