"""Thought emitter — injectable helper for any harness to speak."""
from msb_v2.observer_log.engine import ObserverLog

_observer = ObserverLog()


def emit_thought(source: str, message: str, priority: str = "info"):
    _observer.emit(source, message, priority)
