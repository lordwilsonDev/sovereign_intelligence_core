from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from msb_v2.sn.models import Priority


class PolicyEngine:
    def __init__(
        self,
        rate_limit_per_minute: int = 10,
        quiet_hours_start: Optional[str] = None,
        quiet_hours_end: Optional[str] = None,
    ) -> None:
        self._rate_limit_per_minute = rate_limit_per_minute
        self._quiet_hours_start = quiet_hours_start
        self._quiet_hours_end = quiet_hours_end
        self._recent: list[tuple[datetime, Priority]] = []

    def evaluate(self, priority: Priority, channels: List[str]) -> List[str]:
        if not channels:
            return []
        if not self._within_quiet_hours(priority):
            return []
        if not self._within_rate_limit(priority):
            return []
        return channels

    def _within_quiet_hours(self, priority: Priority) -> bool:
        if priority == Priority.critical:
            return True
        if not self._quiet_hours_start or not self._quiet_hours_end:
            return True
        now = datetime.now(timezone.utc)
        start = datetime.strptime(self._quiet_hours_start, "%H:%M").replace(tzinfo=timezone.utc)
        end = datetime.strptime(self._quiet_hours_end, "%H:%M").replace(tzinfo=timezone.utc)
        if start <= end:
            return not (start <= now <= end)
        return not (now >= start or now <= end)

    def _within_rate_limit(self, priority: Priority) -> bool:
        if self._rate_limit_per_minute <= 0:
            return True
        now = datetime.now(timezone.utc)
        cutoff = now.replace(tzinfo=timezone.utc)
        self._recent = [item for item in self._recent if (now - item[0]).total_seconds() < 60]
        count = sum(1 for item in self._recent if item[1] == priority)
        if count >= self._rate_limit_per_minute:
            return False
        self._recent.append((now, priority))
        return True
