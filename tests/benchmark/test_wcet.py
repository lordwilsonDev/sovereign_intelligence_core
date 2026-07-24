"""WCET benchmark tests."""
from __future__ import annotations

import time

import pytest

from msb_v2.benchmark.wcet import WCETBenchmark


@pytest.fixture()
def benchmark():
    return WCETBenchmark(runs=10)


def test_measure_returns_expected_shape(benchmark: WCETBenchmark) -> None:
    def work():
        time.sleep(0)
    result = benchmark.measure(work, name="work")
    assert result.function == "work"
    assert result.runs == 10
    assert result.max_ms >= result.p95_ms >= result.median_ms >= 0


def test_measure_uses_qualname_by_default(benchmark: WCETBenchmark) -> None:
    class Local:
        def method(self):
            time.sleep(0)
    result = benchmark.measure(Local().method)
    assert result.function.endswith(".Local.method")
