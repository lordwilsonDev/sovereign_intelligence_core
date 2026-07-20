from __future__ import annotations

import threading
from collections import defaultdict
from typing import Any

from prometheus_client import Counter, Gauge, Histogram  # type: ignore[import]

from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.auto_healing import AutoHealingPolicyEngine
from msb_v2.audit.events import AuditEvent, EventType
from msb_v2.audit.schemas import stable_workflow

_workflow_total = Counter("msb_audit_workflow_total", "Workflow events by workflow and status", ["workflow", "status"])
_workflow_latency = Histogram("msb_audit_workflow_latency_ms", "Workflow latency in milliseconds", ["workflow"])
_workflow_tokens = Counter("msb_audit_workflow_tokens_total", "Tokens consumed by workflow", ["workflow"])
_workflow_usd = Counter("msb_audit_workflow_usd_total", "USD cost by workflow", ["workflow"])
_event_total = Counter("msb_audit_event_total", "Audit events by event_type and status", ["event_type", "status"])
_workflow_success_rate = Gauge("msb_audit_workflow_success_rate", "Success rate by workflow", ["workflow"])
_policy_action_total = Counter("msb_audit_policy_action_total", "Auto-healing policy actions by policy", ["policy"])
_policy_actions_current = Gauge("msb_audit_policy_actions_current", "Current detected policy actions", ["policy"])


def _update_from_events(events: list[dict[str, Any]]) -> None:
    workflow_items: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        workflow = stable_workflow(event.get("workflow"))
        workflow_items[workflow].append(event)
        _event_total.labels(event_type=event.get("event_type", ""), status=event.get("status", "")).inc()
    for workflow, items in workflow_items.items():
        total = len(items)
        succeeded = sum(1 for item in items if item.get("status") == "succeeded")
        failed = sum(1 for item in items if item.get("status") in {"failed", "blocked"})
        _workflow_total.labels(workflow=workflow, status="succeeded").inc(succeeded)
        _workflow_total.labels(workflow=workflow, status="failed").inc(failed)
        _workflow_total.labels(workflow=workflow, status="total").inc(total)
        _workflow_success_rate.labels(workflow=workflow).set(succeeded / total if total else 0.0)
        durations = [item.get("duration_ms", 0) for item in items if isinstance(item.get("duration_ms"), int)]
        for duration_ms in durations:
            _workflow_latency.labels(workflow=workflow).observe(duration_ms)
        tokens = sum(int(item.get("cost", {}).get("tokens", 0)) for item in items if item.get("cost") is not None)
        usd = sum(float(item.get("cost", {}).get("usd", 0.0)) for item in items if item.get("cost") is not None)
        _workflow_tokens.labels(workflow=workflow).inc(tokens)
        _workflow_usd.labels(workflow=workflow).inc(usd)


def _update_policy_metrics(actions: list[dict[str, Any]]) -> None:
    counts: dict[str, int] = defaultdict(int)
    for action in actions:
        policy = action.get("policy") or "unknown"
        counts[policy] += 1
    for policy, count in counts.items():
        _policy_action_total.labels(policy=policy).inc(count)
        _policy_actions_current.labels(policy=policy).set(count)


class AuditTelemetry:
    def __init__(self, audit: AuditEngine | None = None, resync_interval_seconds: float = 60.0) -> None:
        self._audit = audit or AuditEngine()
        self._interval = resync_interval_seconds
        self._lock = threading.Lock()
        self._last_count = 0
        self._resync_events()

    def _resync_events(self) -> None:
        events = self._audit.events()
        with self._lock:
            self._last_count = len(events)
        _update_from_events(events)

    def resync(self) -> None:
        self._resync_events()

    def maybe_resync(self, force: bool = False) -> None:
        if force:
            self.resync()
            return
        current = len(self._audit.events())
        with self._lock:
            changed = current != self._last_count
        if changed:
            self._resync_events()
