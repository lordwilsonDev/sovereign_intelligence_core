from __future__ import annotations

import pytest
import time

from msb_v2.runtime.context import RuntimeContext


def test_event_log_flush_loop_store_and_replay() -> None:  # noqa: ANN001
    ctx = RuntimeContext()
    ctx.start()
    try:
        ctx.event_log.append("user.action", "test", {"action": "login"})
        for _ in range(60):
            events = ctx.event_log.query(limit=10)
            if any(e.get("event_type") == "user.action" for e in events):
                break
            time.sleep(0.1)
        else:
            pytest.fail("event not flushed within timeout")
        events = ctx.event_log.query(limit=10)
        types = {e.get("event_type") for e in events}
        assert "user.action" in types
    finally:
        ctx.stop(wait=True)
