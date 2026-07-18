from __future__ import annotations

from msb_v2.observability.metrics import MetricsCollector, get_collector


def test_snapshot_empty():
    c = MetricsCollector()
    snap = c.snapshot()
    assert snap["counters"] == {}
    assert snap["gauges"] == {}
    assert snap["timer_summaries"] == {}


def test_counters_and_gauges():
    c = MetricsCollector()
    c.increment("requests", 1)
    c.increment("requests", 2)
    c.set_gauge("queue_depth", 3.0)
    snap = c.snapshot()
    assert snap["counters"]["requests"] == 3.0
    assert snap["gauges"]["queue_depth"] == 3.0


def test_timer_summary():
    c = MetricsCollector()
    c.record("latency", 10.0)
    c.record("latency", 20.0)
    c.record("latency", 30.0)
    summary = c.timer_summary("latency")
    assert summary["count"] == 3.0
    assert summary["max"] == 30.0
    assert summary["mean"] == 20.0
    assert summary["p50"] == 20.0
    assert summary["p95"] == 30.0


def test_observe_decorator_success():
    from msb_v2.observability.decorators import observe

    @observe("cmd")
    def run():
        return "ok"

    result = run()
    assert result == "ok"
    c = get_collector()
    assert c.snapshot()["counters"]["cmd.success"] >= 1.0


def test_observe_decorator_failure():
    from msb_v2.observability.decorators import observe

    @observe("cmd")
    def run():
        raise RuntimeError("boom")

    try:
        run()
    except RuntimeError:
        pass
    c = get_collector()
    assert c.snapshot()["counters"]["cmd.failure"] >= 1.0
