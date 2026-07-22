from __future__ import annotations

from unittest.mock import patch

import psutil

from msb_v2.systems_health.engine import HealthStatus, SystemsHealthEngine


def test_run_check_returns_green_by_default():
    engine = SystemsHealthEngine()
    report = engine.run_check()
    assert report.status in {"GREEN", "YELLOW", "RED"}
    assert len(report.checks) == 4
    names = {c.name for c in report.checks}
    assert names == {"storage", "cpu", "memory", "processes"}


def test_high_disk_usage_degraded():
    engine = SystemsHealthEngine()
    fake_stat = type("Stat", (), {"f_blocks": 1000, "f_frsize": 1024, "f_bfree": 50})()
    with patch("msb_v2.systems_health.engine.os.statvfs", return_value=fake_stat):
        report = engine.run_check()
    disk = next(c for c in report.checks if c.name == "storage")
    assert disk.status in {HealthStatus.degraded, HealthStatus.unhealthy}


def test_history_limit():
    engine = SystemsHealthEngine()
    for _ in range(10):
        engine.run_check()
    history = engine.history(limit=3)
    assert len(history) == 3
