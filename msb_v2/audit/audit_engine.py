from __future__ import annotations

from typing import Any

from msb_v2.audit.events import AuditEvent
from msb_v2.audit.storage import AuditStore
from msb_v2.audit.validator import AuditValidator


class AuditEngine:
    def __init__(self, store: AuditStore | None = None, validator: AuditValidator | None = None) -> None:
        self._store = store or AuditStore()
        self._validator = validator or AuditValidator()
        self._falsification: dict[str, dict[str, Any]] = {}
        self._assumption_debt_count: int = 0

    def record(self, event: AuditEvent) -> AuditEvent:
        self._validator.validate(event)
        self._store.append(event)
        return event

    def events(self, limit: int | None = None) -> list[dict[str, Any]]:
        return self._store.read(limit=limit)

    def record_policy_falsification(self, *, policy: str, detected_rate: float, sample_count: int, blocked: bool, checksum: str) -> dict[str, Any]:
        previous = self._falsification.get(policy)
        improvement = 0.0 if previous is None else round(previous["detected_rate"] - detected_rate, 6)
        outcome = "pending" if improvement >= 0 else "falsified"
        record = {
            "policy": policy,
            "detected_rate": detected_rate,
            "sample_count": sample_count,
            "blocked": blocked,
            "checksum": checksum,
            "improvement": improvement,
            "outcome": outcome,
        }
        self._falsification[policy] = record
        return record

    def falsification_snapshot(self) -> dict[str, Any]:
        records = list(self._falsification.values())
        falsified_count = sum(1 for r in records if r["outcome"] == "falsified")
        return {"records": records, "count": len(records), "falsified_count": falsified_count}

    def record_assumption_debt(self, count: int = 1) -> None:
        self._assumption_debt_count += max(int(count), 0)

    def assumption_debt_count(self) -> int:
        return self._assumption_debt_count

    def clear(self) -> None:
        self._store.clear()
        self._falsification.clear()
        self._assumption_debt_count = 0
