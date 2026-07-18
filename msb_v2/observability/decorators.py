from __future__ import annotations

import time

from msb_v2.observability.metrics import get_collector


def observe(name: str):
    collector = get_collector()

    def decorator(fn):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = fn(*args, **kwargs)
                collector.increment(f"{name}.success")
                return result
            except Exception:
                collector.increment(f"{name}.failure")
                raise
            finally:
                duration_ms = (time.perf_counter() - start) * 1000.0
                collector.record(f"{name}.duration_ms", duration_ms)

        return wrapper

    return decorator
