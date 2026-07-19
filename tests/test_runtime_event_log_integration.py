from __future__ import annotations

import time

from msb_v2.runtime.context import RuntimeContext


def test_runtime_event_log_bus_publish_and_replay() -> None:
    received = []

    ctx = RuntimeContext()
    ctx.start()
    try:
        ctx.events.subscribe("user.action", lambda event: received.append(event))
        ctx.events.publish("user.action", {"action": "login"})
        for _ in range(60):
            if received:
                break
            time.sleep(0.1)
        else:
            raise AssertionError("event bus subscriber never received published event")
    finally:
        ctx.stop(wait=True)

