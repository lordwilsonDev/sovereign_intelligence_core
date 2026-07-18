from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class HarnessTelemetry:
    routing_confidence: float = 0.0
    execution_time_s: float = 0.0
    retries: int = 0
    fallback_reason: Optional[str] = None
    memory_bytes: Optional[int] = None
    token_usage: Optional[Dict[str, int]] = None
    error_class: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class HarnessResult:
    ok: bool
    event: str
    payload: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    telemetry: HarnessTelemetry = field(default_factory=HarnessTelemetry)


class BaseHarness(ABC):
    @abstractmethod
    def execute(self, query: str, *args: Any, context: Optional[Dict[str, Any]] = None, **kwargs: Any) -> HarnessResult:
        if context is None:
            context = {}
        return self.evaluate(query, context)

    @abstractmethod
    def evaluate(self, query: str, context: Dict[str, Any]) -> HarnessResult:
        return self.execute(query, context=context)

    def initialize(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"ok": True, "event": "initialized"}

    def observe(self, result: HarnessResult) -> Dict[str, Any]:
        return {"event": result.event, "ok": result.ok}

    def repair(self, result: HarnessResult) -> Optional[HarnessResult]:
        return None

    def shutdown(self) -> Dict[str, Any]:
        return {"ok": True, "event": "shutdown"}
