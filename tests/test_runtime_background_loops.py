from __future__ import annotations

import time

import pytest

from msb_v2.core.background_tasks import BackgroundTaskRegistry
from msb_v2.runtime.context import RuntimeContext


def test_runtime_registers_event_log_flush_thread() -> None:  # noqa: ANN001
    ctx = RuntimeContext()
    ctx.start()
    try:
        time.sleep(0.1)
        assert ctx.background.pending_count >= 1
        labels = [t.name for t, _ in _threads(ctx) if getattr(t, "name", None)]
        assert any("event-log-flush" in name for name in labels)
    finally:
        ctx.stop(wait=True)


def test_runtime_feedback_collector_loop_registered() -> None:  # noqa: ANN001
    ctx = RuntimeContext()
    ctx.start()
    try:
        class FakeCollector:
            def _on_correction(self, event: object) -> None:
                ...
            def summary(self) -> dict:
                return {"feedback_count": 0}

        collector = FakeCollector()
        ctx.register_feedback_collector(collector)
        time.sleep(0.35)
        assert ctx.background.pending_count >= 2
        labels = [t.name for t, _ in _threads(ctx) if getattr(t, "name", None)]
        assert any("feedback-summary" in name for name in labels)
    finally:
        ctx.stop(wait=True)


def _threads(ctx: RuntimeContext) -> list:
    if hasattr(ctx.background, "_threads"):
        return getattr(ctx.background, "_threads", [])
    return []
