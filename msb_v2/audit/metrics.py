from __future__ import annotations

from collections import defaultdict
from typing import Any

from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.events import AuditEvent, EventType
from msb_v2.audit.schemas import stable_workflow


class MetricsEngine:
    def __init__(self, audit: AuditEngine | None = None) -> None:
        self._audit = audit or AuditEngine()

    def snapshot(self) -> dict[str, Any]:
        events = self._audit.events()
        workflows: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for event in events:
            workflow = stable_workflow(event.get("workflow"))
            workflows[workflow].append(event)
        summary: dict[str, Any] = {"workflows": {}}
        for workflow, items in workflows.items():
            total = len(items)
            failed = sum(1 for item in items if item.get("status") in {"failed", "blocked"})
            succeeded = sum(1 for item in items if item.get("status") == "succeeded")
            durations = [item.get("duration_ms", 0) for item in items if isinstance(item.get("duration_ms"), int)]
            avg_latency_ms = (sum(durations) / len(durations)) if durations else 0
            tokens = sum(int(item.get("cost", {}).get("tokens", 0)) for item in items if item.get("cost") is not None)
            usd = sum(float(item.get("cost", {}).get("usd", 0.0)) for item in items if item.get("cost") is not None)
            routing = [item for item in items if item.get("event_type") == EventType.ROUTING_DECISION.value]
            selected = defaultdict(int)
            for item in routing:
                selected[str(item.get("metadata", {}).get("selected_expert"))] += 1
            summary["workflows"][workflow] = {
                "total": total,
                "succeeded": succeeded,
                "failed": failed,
                "success_rate": succeeded / total if total else 0.0,
                "avg_latency_ms": avg_latency_ms,
                "tokens": tokens,
                "usd": usd,
                "selected_expert_counts": dict(selected),
            }
        return summary
