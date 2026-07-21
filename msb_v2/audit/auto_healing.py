from __future__ import annotations

from typing import Any

from cognitive_compiler.sovereign_autonomy_core import QuarantineInversionAgent
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.events import AuditEvent, EventType, Status


class PolicyFalsificationTracker:
    def __init__(self, max_records: int = 128) -> None:
        self._last_rate: dict[str, float] = {}

    def record_check(self, *, policy: str, detected_rate: float, sample_count: int, blocked: bool, checksum: str) -> dict[str, Any]:
        previous = self._last_rate.get(policy)
        improvement = 0.0 if previous is None else round(previous - detected_rate, 6)
        outcome = "pending" if improvement >= 0 else "falsified"
        self._last_rate[policy] = detected_rate
        return {
            "policy": policy,
            "detected_rate": detected_rate,
            "sample_count": sample_count,
            "blocked": blocked,
            "checksum": checksum,
            "improvement": improvement,
            "outcome": outcome,
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "records": [],
            "count": 0,
            "falsified_count": 0,
        }


class AutoHealingPolicyEngine:
    def __init__(self, audit: AuditEngine | None = None) -> None:
        self._audit = audit or AuditEngine()
        self._quarantine = QuarantineInversionAgent()
        self._falsification = PolicyFalsificationTracker()

    def evaluate(self) -> list[dict[str, Any]]:
        events = self._audit.events()
        actions: list[dict[str, Any]] = []
        actions.extend(self._check_timeout_rate(events))
        actions.extend(self._check_retry_rate(events))
        actions.extend(self._check_cache_miss_rate(events))
        return actions

    def record_check(self, *, policy: str, detected_rate: float, sample_count: int, blocked: bool, checksum: str) -> dict[str, Any]:
        return self._falsification.record_check(
            policy=policy,
            detected_rate=detected_rate,
            sample_count=sample_count,
            blocked=blocked,
            checksum=checksum,
        )

    def falsification_snapshot(self) -> dict[str, Any]:
        return self._falsification.snapshot()

    def _check_timeout_rate(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return self._apply_threshold(
            events=events,
            event_types={EventType.TIMEOUT.value},
            all_event_types={EventType.TOOL_CALLED.value, EventType.TOOL_COMPLETED.value, EventType.TIMEOUT.value},
            threshold=0.05,
            label="tool_timeout_rate",
            suggestion="Increase timeout duration for affected tools",
        )

    def _check_retry_rate(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return self._apply_threshold(
            events=events,
            event_types={EventType.RETRY.value},
            all_event_types={EventType.TOOL_CALLED.value, EventType.TOOL_COMPLETED.value, EventType.RETRY.value},
            threshold=0.15,
            label="retry_rate",
            suggestion="Adjust prompt or route to reduce retries",
        )

    def _check_cache_miss_rate(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return self._apply_threshold(
            events=events,
            event_types={EventType.CACHE_MISS.value},
            all_event_types={EventType.CACHE_HIT.value, EventType.CACHE_MISS.value},
            threshold=0.30,
            label="cache_miss_rate",
            suggestion="Adjust caching strategy for frequent misses",
        )

    def _apply_threshold(
        self,
        *,
        events: list[dict[str, Any]],
        event_types: set[str],
        all_event_types: set[str],
        threshold: float,
        label: str,
        suggestion: str,
    ) -> list[dict[str, Any]]:
        total = sum(1 for event in events if event.get("event_type") in all_event_types)
        if total == 0:
            return []
        count = sum(1 for event in events if event.get("event_type") in event_types)
        rate = count / total
        if rate <= threshold:
            return []
        action = {
            "policy": label,
            "detected_rate": rate,
            "sample_count": total,
            "suggestion": suggestion,
        }
        veto = self._quarantine.apply(
            source_label="auto-healing",
            payload={"action": action},
        )
        blocked = veto.required_justification or not veto.weight_override_allowed
        action["status"] = "blocked" if blocked else "allowed"
        action["quarantine_checksum"] = veto.checksum
        action["falsification"] = self.record_check(
            policy=label,
            detected_rate=rate,
            sample_count=total,
            blocked=blocked,
            checksum=veto.checksum,
        )
        self._audit.record(
            AuditEvent(
                workflow="policy-audit",
                event_type=EventType.SELF_CORRECTION_BLOCKED if blocked else EventType.SELF_CORRECTION,
                status=Status.SUCCEEDED,
                metadata={
                    "policy": label,
                    "detected_rate": rate,
                    "sample_count": total,
                    "suggestion": suggestion,
                    "quarantine": {
                        "required_justification": veto.required_justification,
                        "weight_override_allowed": veto.weight_override_allowed,
                        "checksum": veto.checksum,
                    },
                },
            )
        )
        return [action]
