"""Small regression harness for deterministic model evaluations."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Protocol


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


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
mutants_xǁEvalHarnessǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁEvalHarnessǁrun__mutmut: MutantDict = {}  # type: ignore
mutants_xǁEvalHarnessǁregression_check__mutmut: MutantDict = {}  # type: ignore


class EvalHarness:
    @_mutmut_mutated(mutants_xǁEvalHarnessǁ__init____mutmut)
    def __init__(self, cases: list[EvalCase], scorer: Callable[[Any, Any], bool] | None = None) -> None:
        self.cases = cases
        self.scorer = scorer or (lambda expected, actual: expected == actual)
    def xǁEvalHarnessǁ__init____mutmut_orig(self, cases: list[EvalCase], scorer: Callable[[Any, Any], bool] | None = None) -> None:
        self.cases = cases
        self.scorer = scorer or (lambda expected, actual: expected == actual)
    def xǁEvalHarnessǁ__init____mutmut_1(self, cases: list[EvalCase], scorer: Callable[[Any, Any], bool] | None = None) -> None:
        self.cases = None
        self.scorer = scorer or (lambda expected, actual: expected == actual)
    def xǁEvalHarnessǁ__init____mutmut_2(self, cases: list[EvalCase], scorer: Callable[[Any, Any], bool] | None = None) -> None:
        self.cases = cases
        self.scorer = None
    def xǁEvalHarnessǁ__init____mutmut_3(self, cases: list[EvalCase], scorer: Callable[[Any, Any], bool] | None = None) -> None:
        self.cases = cases
        self.scorer = scorer and (lambda expected, actual: expected == actual)
    def xǁEvalHarnessǁ__init____mutmut_4(self, cases: list[EvalCase], scorer: Callable[[Any, Any], bool] | None = None) -> None:
        self.cases = cases
        self.scorer = scorer or (lambda expected, actual: None)
    def xǁEvalHarnessǁ__init____mutmut_5(self, cases: list[EvalCase], scorer: Callable[[Any, Any], bool] | None = None) -> None:
        self.cases = cases
        self.scorer = scorer or (lambda expected, actual: expected != actual)

    @_mutmut_mutated(mutants_xǁEvalHarnessǁrun__mutmut)
    def run(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_orig(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_1(self, model: PredictiveModel) -> EvalReport:
        results = None
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_2(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = None
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_3(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = None
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_4(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(None)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_5(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(None)
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_6(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(None, self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_7(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, None, (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_8(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), None))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_9(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_10(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_11(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), ))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_12(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(None, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_13(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, None), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_14(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_15(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, ), (perf_counter() - started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_16(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) / 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_17(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() + started) * 1000))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_18(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) * 1001))
        return EvalReport(tuple(results))

    def xǁEvalHarnessǁrun__mutmut_19(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(None)

    def xǁEvalHarnessǁrun__mutmut_20(self, model: PredictiveModel) -> EvalReport:
        results = []
        for case in self.cases:
            started = perf_counter()
            prediction = model.predict(case.input)
            results.append(EvalResult(case.id, self.scorer(case.expected, prediction), (perf_counter() - started) * 1000))
        return EvalReport(tuple(None))

    @_mutmut_mutated(mutants_xǁEvalHarnessǁregression_check__mutmut)
    def regression_check(self, candidate: PredictiveModel, baseline: PredictiveModel, tolerance: float = 0.02) -> bool:
        return self.run(candidate).accuracy >= self.run(baseline).accuracy - tolerance

    def xǁEvalHarnessǁregression_check__mutmut_orig(self, candidate: PredictiveModel, baseline: PredictiveModel, tolerance: float = 0.02) -> bool:
        return self.run(candidate).accuracy >= self.run(baseline).accuracy - tolerance

    def xǁEvalHarnessǁregression_check__mutmut_1(self, candidate: PredictiveModel, baseline: PredictiveModel, tolerance: float = 1.02) -> bool:
        return self.run(candidate).accuracy >= self.run(baseline).accuracy - tolerance

    def xǁEvalHarnessǁregression_check__mutmut_2(self, candidate: PredictiveModel, baseline: PredictiveModel, tolerance: float = 0.02) -> bool:
        return self.run(None).accuracy >= self.run(baseline).accuracy - tolerance

    def xǁEvalHarnessǁregression_check__mutmut_3(self, candidate: PredictiveModel, baseline: PredictiveModel, tolerance: float = 0.02) -> bool:
        return self.run(candidate).accuracy > self.run(baseline).accuracy - tolerance

    def xǁEvalHarnessǁregression_check__mutmut_4(self, candidate: PredictiveModel, baseline: PredictiveModel, tolerance: float = 0.02) -> bool:
        return self.run(candidate).accuracy >= self.run(baseline).accuracy + tolerance

    def xǁEvalHarnessǁregression_check__mutmut_5(self, candidate: PredictiveModel, baseline: PredictiveModel, tolerance: float = 0.02) -> bool:
        return self.run(candidate).accuracy >= self.run(None).accuracy - tolerance

mutants_xǁEvalHarnessǁ__init____mutmut['_mutmut_orig'] = EvalHarness.xǁEvalHarnessǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁ__init____mutmut['xǁEvalHarnessǁ__init____mutmut_1'] = EvalHarness.xǁEvalHarnessǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁ__init____mutmut['xǁEvalHarnessǁ__init____mutmut_2'] = EvalHarness.xǁEvalHarnessǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁ__init____mutmut['xǁEvalHarnessǁ__init____mutmut_3'] = EvalHarness.xǁEvalHarnessǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁ__init____mutmut['xǁEvalHarnessǁ__init____mutmut_4'] = EvalHarness.xǁEvalHarnessǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁ__init____mutmut['xǁEvalHarnessǁ__init____mutmut_5'] = EvalHarness.xǁEvalHarnessǁ__init____mutmut_5 # type: ignore # mutmut generated

mutants_xǁEvalHarnessǁrun__mutmut['_mutmut_orig'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_1'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_2'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_3'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_4'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_4 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_5'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_5 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_6'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_6 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_7'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_7 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_8'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_8 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_9'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_9 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_10'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_10 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_11'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_11 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_12'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_12 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_13'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_13 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_14'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_14 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_15'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_15 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_16'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_16 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_17'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_17 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_18'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_18 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_19'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_19 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁrun__mutmut['xǁEvalHarnessǁrun__mutmut_20'] = EvalHarness.xǁEvalHarnessǁrun__mutmut_20 # type: ignore # mutmut generated

mutants_xǁEvalHarnessǁregression_check__mutmut['_mutmut_orig'] = EvalHarness.xǁEvalHarnessǁregression_check__mutmut_orig # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁregression_check__mutmut['xǁEvalHarnessǁregression_check__mutmut_1'] = EvalHarness.xǁEvalHarnessǁregression_check__mutmut_1 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁregression_check__mutmut['xǁEvalHarnessǁregression_check__mutmut_2'] = EvalHarness.xǁEvalHarnessǁregression_check__mutmut_2 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁregression_check__mutmut['xǁEvalHarnessǁregression_check__mutmut_3'] = EvalHarness.xǁEvalHarnessǁregression_check__mutmut_3 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁregression_check__mutmut['xǁEvalHarnessǁregression_check__mutmut_4'] = EvalHarness.xǁEvalHarnessǁregression_check__mutmut_4 # type: ignore # mutmut generated
mutants_xǁEvalHarnessǁregression_check__mutmut['xǁEvalHarnessǁregression_check__mutmut_5'] = EvalHarness.xǁEvalHarnessǁregression_check__mutmut_5 # type: ignore # mutmut generated
