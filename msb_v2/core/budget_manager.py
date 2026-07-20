from __future__ import annotations

import time
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Dict, Optional

from prometheus_client import Counter, Gauge

_budget_depth_gauge = Gauge("msb_current_depth", "Current reasoning depth", ["trace_id"])
_budget_tool_calls_gauge = Gauge(
    "msb_tool_calls_count", "Tool calls in current trace", ["trace_id"]
)
_budget_breach_counter = Counter(
    "msb_budget_breaches_total", "Budget breaches by type", ["breach_type"]
)
_budget_health_gauge = Gauge("msb_budget_health", "1 if within budget, 0 if breached", ["trace_id"])
_g_load_ratio = Gauge("msb_global_load_ratio", "Global cognitive load ratio 0..1")
_g_circuit_open = Gauge("msb_circuit_breaker_open", "1 if global circuit breaker is open")
_g_traces_total = Counter("msb_reasoning_traces_total", "Reasoning traces started")
_g_tool_calls_total = Counter("msb_reasoning_tool_calls_total", "Reasoning tool calls total")
_g_memory_verification_rate = Gauge("msb_memory_verification_rate", "Memory verification rate 0..1")
_g_reasoning_avg_score = Gauge("msb_reasoning_avg_score", "Average reasoning score")


def record_trace_started(trace_id: Optional[str] = None) -> None:
    _g_traces_total.inc()


@dataclass
class BudgetContext:
    trace_id: str = ""
    depth: int = 0
    tool_calls: int = 0
    tokens: int = 0
    start_time: float = field(default_factory=time.time)
    breached: bool = False
    breach_reason: str = ""
    finished: bool = False


class GlobalCircuitBreaker:
    def __init__(
        self,
        window_seconds: int = 300,
        breach_rate_threshold: float = 0.05,
        min_requests: int = 20,
    ) -> None:
        self.window_seconds = window_seconds
        self.breach_rate_threshold = breach_rate_threshold
        self.min_requests = min_requests
        self._events: deque = deque()
        self._open: bool = False
        self._open_since: float = 0.0
        self._cooldown_seconds: int = 60

    def record_request(self, is_breach: bool) -> None:
        now = time.time()
        self._events.append((now, bool(is_breach)))
        cutoff = now - self.window_seconds
        while self._events and self._events[0][0] < cutoff:
            self._events.popleft()

    def evaluate(self) -> bool:
        now = time.time()
        if self._open and (now - self._open_since) < self._cooldown_seconds:
            return True

        total = len(self._events)
        if total < self.min_requests:
            self._open = False
            _g_circuit_open.set(0)
            return False

        breaches = sum(1 for _, b in self._events if b)
        rate = breaches / total
        if rate > self.breach_rate_threshold:
            self._open = True
            self._open_since = now
            _g_circuit_open.set(1)
            return True

        self._open = False
        _g_circuit_open.set(0)
        return False

    @property
    def open(self) -> bool:
        return self.evaluate()


class CognitiveBudgetManager:
    def __init__(
        self,
        max_depth: int = 5,
        max_tool_calls: int = 10,
        max_latency_ms: int = 5000,
        max_tokens_estimate: int = 8000,
        max_global_depth: int = 120,
        max_global_tool_calls: int = 240,
        max_global_tokens: int = 96000,
    ) -> None:
        self.max_depth = max_depth
        self.max_tool_calls = max_tool_calls
        self.max_latency_ms = max_latency_ms
        self.max_tokens_estimate = max_tokens_estimate
        self.max_global_depth = max_global_depth
        self.max_global_tool_calls = max_global_tool_calls
        self.max_global_tokens = max_global_tokens
        self._contexts: Dict[str, BudgetContext] = {}
        self._labels = {"trace_id": "unknown"}
        self._circuit = GlobalCircuitBreaker()
        self._global_depth = 0
        self._global_tool_calls = 0
        self._global_tokens = 0

    def _current_labels(self, trace_id: Optional[str] = None):
        return {"trace_id": trace_id or self._labels.get("trace_id", "unknown")}

    def _current_ctx(self, trace_id: Optional[str] = None) -> Optional[BudgetContext]:
        return self._contexts.get(trace_id or self._labels.get("trace_id", "unknown"))

    def can_execute(self, trace_id: str) -> bool:
        if self._circuit.open:
            return False
        ctx = self._contexts.get(trace_id)
        if not ctx:
            return True
        if ctx.breached:
            return False
        if ctx.depth >= self.max_depth:
            return False
        if ctx.tool_calls >= self.max_tool_calls:
            return False
        if self._global_depth + 1 > self.max_global_depth:
            return False
        if self._global_tool_calls + 1 > self.max_global_tool_calls:
            return False
        if self._global_tokens + 0 > self.max_global_tokens:
            return False
        return True

    def _update_global_load(self) -> None:
        load = 0.0
        depth_ratio = min(self._global_depth / max(self.max_global_depth, 1), 1.0)
        tool_ratio = min(self._global_tool_calls / max(self.max_global_tool_calls, 1), 1.0)
        token_ratio = min(self._global_tokens / max(self.max_global_tokens, 1), 1.0)
        load = max(depth_ratio, tool_ratio, token_ratio)
        _g_load_ratio.set(load)

    @contextmanager
    def track(self, trace_id: str):
        labels = self._current_labels(trace_id)
        key = trace_id or "unknown"
        ctx = self._contexts.get(key)
        if ctx is None:
            ctx = BudgetContext(trace_id=key)
            self._contexts[key] = ctx
        self._labels = labels
        _budget_depth_gauge.labels(**labels).set(ctx.depth)
        _budget_tool_calls_gauge.labels(**labels).set(ctx.tool_calls)
        _budget_health_gauge.labels(**labels).set(0 if ctx.breached else 1)
        try:
            yield ctx
        finally:
            self._finalize(ctx, labels)

    def increment_depth(self, trace_id: Optional[str] = None) -> None:
        ctx = self._current_ctx(trace_id)
        if not ctx:
            return
        ctx.depth += 1
        self._global_depth += 1
        _budget_depth_gauge.labels(**self._current_labels(trace_id)).set(ctx.depth)
        self._update_global_load()
        self._check_latency(ctx)

    def increment_tool_calls(self, trace_id: Optional[str] = None) -> None:
        ctx = self._current_ctx(trace_id)
        if not ctx:
            return
        ctx.tool_calls += 1
        self._global_tool_calls += 1
        _budget_tool_calls_gauge.labels(**self._current_labels(trace_id)).set(ctx.tool_calls)
        self._update_global_load()
        self._check_latency(ctx)

    def record_tokens(self, tokens: int, trace_id: Optional[str] = None) -> None:
        ctx = self._current_ctx(trace_id)
        if not ctx:
            return
        ctx.tokens += tokens
        self._global_tokens += tokens
        self._update_global_load()
        if tokens > self.max_tokens_estimate:
            self._breach(ctx, f"tokens={tokens}")

    def _check_latency(self, ctx: BudgetContext) -> None:
        elapsed = (time.time() - ctx.start_time) * 1000
        if elapsed > self.max_latency_ms:
            self._breach(ctx, f"latency={elapsed:.0f}ms")

    def _breach(self, ctx: Optional[BudgetContext], reason: str) -> None:
        if not ctx or ctx.breached:
            return
        ctx.breached = True
        ctx.breach_reason = reason
        breach_type = reason.split("=")[0]
        _budget_breach_counter.labels(breach_type=breach_type).inc()
        _budget_health_gauge.labels(**self._labels).set(0)
        self._circuit.record_request(is_breach=True)

    def _finalize(self, ctx: BudgetContext, labels: Dict[str, str]) -> None:
        if ctx.finished:
            return
        ctx.finished = True
        if ctx.depth > self.max_depth:
            self._breach(ctx, f"depth={ctx.depth}")
        if ctx.tool_calls > self.max_tool_calls:
            self._breach(ctx, f"tool_calls={ctx.tool_calls}")
        elapsed = (time.time() - ctx.start_time) * 1000
        if elapsed > self.max_latency_ms:
            self._breach(ctx, f"latency={elapsed:.0f}ms")
        if not ctx.breached:
            self._circuit.record_request(is_breach=False)
        self._update_global_load()
