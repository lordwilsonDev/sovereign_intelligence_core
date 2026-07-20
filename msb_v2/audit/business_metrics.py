from __future__ import annotations

import random
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.events import EventType
from msb_v2.audit.schemas import apply_event_hashes, stable_workflow


class BusinessMetrics:
    def __init__(self, audit: AuditEngine | None = None) -> None:
        self._audit = audit or AuditEngine()

    def snapshot(self, now: datetime | None = None) -> dict[str, Any]:
        now = now or datetime.now(timezone.utc)
        if now.tzinfo is None:
            now = now.replace(tzinfo=timezone.utc)
        events = self._audit.events()
        recent = self._recent(events, now)
        workflows = self._workflow_summary(recent)
        decisions = self._decision_summary(recent)
        errors = self._error_summary(recent)
        business = self._business_impact(recent)
        recommendations = self._recommendations(errors, business)
        cypher = self._immutability_record(recent)
        return {
            "generated_at": now.isoformat(),
            "summary": {
                "total_workflows": workflows["total"],
                "success_rate": workflows["success_rate"],
                "errors_recovered": errors["recovered_count"],
            },
            "workflow_integrity": workflows["items"],
            "decision_record": decisions,
            "error_recovery": errors,
            "business_impact": business,
            "recommendations": recommendations,
            "immutable_record": cypher,
        }

    def _recent(self, events: list[dict[str, Any]], now: datetime) -> list[dict[str, Any]]:
        start = (now - timedelta(days=90)).replace(tzinfo=timezone.utc)
        filtered = []
        for event in events:
            ts = event.get("timestamp")
            if isinstance(ts, str):
                try:
                    ts = datetime.fromisoformat(ts)
                    if ts.tzinfo is None:
                        ts = ts.replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
            if isinstance(ts, datetime) and start <= ts <= now:
                filtered.append(event)
        return filtered

    def _workflow_summary(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        items = []
        succeeded = failed = 0
        for event in events:
            if event.get("event_type") in {EventType.WORKFLOW_COMPLETE.value, EventType.WORKFLOW_FAILED.value}:
                status = event.get("status", "unknown")
                if status == "succeeded":
                    succeeded += 1
                elif status in {"failed", "blocked"}:
                    failed += 1
                items.append({
                    "timestamp": event.get("timestamp"),
                    "workflow": stable_workflow(event.get("workflow")),
                    "status": status,
                    "duration_ms": event.get("duration_ms"),
                    "agent": event.get("agent"),
                })
        total = succeeded + failed
        return {
            "total": total,
            "succeeded": succeeded,
            "failed": failed,
            "success_rate": (succeeded / total) if total else 0.0,
            "items": items[:500],
        }

    def _decision_summary(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        decisions = []
        for event in events:
            if event.get("event_type") == EventType.ROUTING_DECISION.value:
                decisions.append({
                    "timestamp": event.get("timestamp"),
                    "context": event.get("workflow"),
                    "decision": event.get("metadata", {}).get("selected_expert") if isinstance(event.get("metadata"), dict) else None,
                    "confidence": event.get("confidence"),
                    "reasoning": event.get("reasoning_summary"),
                })
        return decisions[:500]

    def _error_summary(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        recovered = 0
        retries = 0
        errors = []
        for event in events:
            status = event.get("status")
            if status in {"failed", "blocked"}:
                errors.append({
                    "timestamp": event.get("timestamp"),
                    "workflow": event.get("workflow"),
                    "error": event.get("exception"),
                    "recovery": event.get("reasoning_summary"),
                })
            if event.get("event_type") == EventType.RETRY.value:
                retries += 1
            if status == "succeeded" and event.get("exception"):
                recovered += 1
        return {
            "recovered_count": recovered,
            "retry_count": retries,
            "items": errors[:500],
        }

    def _business_impact(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        workflows = [e for e in events if e.get("event_type") in {EventType.WORKFLOW_COMPLETE.value, EventType.WORKFLOW_FAILED.value}]
        succeeded = [w for w in workflows if w.get("status") == "succeeded"]
        failed = [w for w in workflows if w.get("status") in {"failed", "blocked"}]
        durations = [w.get("duration_ms", 0) for w in succeeded if isinstance(w.get("duration_ms"), int)]
        avg_latency = (sum(durations) / len(durations)) if durations else 0
        hours_saved = len(succeeded) * 0.15
        revenue_influenced = len(succeeded) * 50.0
        automation_rate = (len(succeeded) / len(workflows)) if workflows else 0.0
        return {
            "hours_saved": round(hours_saved, 1),
            "revenue_influenced": round(revenue_influenced, 2),
            "error_reduction_rate_pct": round((1 - (len(failed) / len(workflows))) * 100, 1) if workflows else 0.0,
            "automation_adoption_rate_pct": round(automation_rate * 100, 1),
            "avg_latency_ms": round(avg_latency, 1),
        }

    def _recommendations(self, errors: dict[str, Any], business: dict[str, Any]) -> list[dict[str, Any]]:
        recommendations = []
        error_items = errors.get("items", [])
        if len(error_items) >= 3:
            recommendations.append({
                "pattern": "recurring_errors",
                "data": f"{len(error_items)} errors detected in the reporting window",
                "impact": "Workflow reliability below target",
                "suggestion": "Review top error workflows and add targeted retry/fallback handling",
            })
        if business.get("avg_latency_ms", 0) > 5000:
            recommendations.append({
                "pattern": "high_latency",
                "data": f"Average workflow latency is {business['avg_latency_ms']} ms",
                "impact": "Slower response times and higher cost",
                "suggestion": "Investigate slow tools or model calls and reduce token/payload size",
            })
        return recommendations

    def _immutability_record(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        enriched = apply_event_hashes(events)
        chain_root = enriched[0].get("chain_hash") if enriched else None
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "root_hash": chain_root or ("0" * 40),
            "total_blocks": len(enriched),
            "note": "Event hash chain over the reporting window.",
        }

