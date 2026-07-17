from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

if TYPE_CHECKING:
    from msb_v2.runtime.event_log import PersistentEventLog


@dataclass(frozen=True)
class Event:
    topic: str
    payload: Dict[str, Any] = field(default_factory=dict)


class EventBus:
    def __init__(self, persistent_log: Optional[PersistentEventLog] = None) -> None:
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}
        self._persistent_log = persistent_log

    def subscribe(self, topic: str, handler: Callable[[Event], None]) -> None:
        self._subscribers.setdefault(topic, []).append(handler)

    def publish(self, topic: str, payload: Dict[str, Any] | None = None) -> None:
        event = Event(topic=topic, payload=payload or {})
        if self._persistent_log is not None:
            try:
                self._persistent_log.append(topic, "bus", event.payload)
            except Exception:
                pass
        for handler in list(self._subscribers.get(topic, [])):
            try:
                handler(event)
            except Exception:
                pass

    def clear(self, topic: str) -> None:
        self._subscribers[topic] = []

    def topics(self) -> List[str]:
        return list(self._subscribers.keys())
