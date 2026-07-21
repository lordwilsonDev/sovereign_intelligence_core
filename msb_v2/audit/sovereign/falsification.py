from __future__ import annotations

import hashlib
from collections import deque
from dataclasses import dataclass, field
from typing import Any


@dataclass
class PolicyFalsificationRecord:
    policy: str
    detected_rate: float
    sample_count: int
    blocked: bool
    checksum: str
    outcome: str = "pending"
    improvement: float = 0.0


class PolicyFalsificationTracker:
    def __init__(self, max_records: int = 128) -> None:
        self._records: deque[PolicyFalsificationRecord] = deque(maxlen=max_records)
        self._last_rate: dict[str, float] = {}

    def record_check(self, *, policy: str, detected_rate: float, sample_count: int, blocked: bool, checksum: str) -> str:
        key = policy
        previous = self._last_rate.get(key)
        improvement = 0.0
        if previous is not None:
            improvement = round(previous - detected_rate, 6)
        record = PolicyFalsificationRecord(
            policy=policy,
            detected_rate=detected_rate,
            sample_count=sample_count,
            blocked=blocked,
            checksum=checksum,
            outcome="pending" if improvement >= 0 else "falsified",
            improvement=improvement,
        )
        self._records.append(record)
        self._last_rate[key] = detected_rate
        return checksum

    def snapshot(self) -> dict[str, Any]:
        return {
            "records": [r.__dict__ for r in self._records],
            "count": len(self._records),
            "falsified_count": sum(1 for r in self._records if r.outcome == "falsified"),
        }
