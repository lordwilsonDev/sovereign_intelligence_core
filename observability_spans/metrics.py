from __future__ import annotations

import time
from typing import Any, Dict


class MetricsEmitter:
    def __init__(self) -> None:
        self.points: List[Dict[str, Any]] = []

    def observe(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        point = {
            "name": name,
            "value": value,
            "labels": labels or {},
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        self.points.append(point)
        return point
