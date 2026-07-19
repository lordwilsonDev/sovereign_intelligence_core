"""
Minimal production observability: cross-cutting timing + status log for engine stages.
No external deps; emits structured dicts to the MSB logger namespace.
"""
from __future__ import annotations

import functools
import logging
import time
from typing import Any

log = logging.getLogger("msb_v2.engine")


def span(name: str):
    def deco(fn):
        @functools.wraps(fn)
        def wrap(*a: Any, **kw: Any) -> Any:
            t0 = time.perf_counter()
            exc_raised = None
            out = None
            try:
                out = fn(*a, **kw)
            except Exception as exc:
                exc_raised = exc
            ms = round((time.perf_counter() - t0) * 1000, 3)
            ok = _is_ok(out, exc_raised)
            log.debug({"span": name, "ms": ms, "ok": ok, "error": type(exc_raised).__name__ if exc_raised else None})
            if exc_raised is not None:
                raise exc_raised
            return out
        return wrap
    return deco


def _is_ok(out: Any, exc_raised: Exception | None) -> bool:
    if exc_raised is not None:
        return False
    if isinstance(out, dict):
        return out.get("status") != "error"
    return True
