from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ResourceUsage:
    cpu_percent: float = 0.0
    mem_mb: float = 0.0
    disk_mb: float = 0.0
    energy_units: float = 0.0


class ResourceBudget:
    def __init__(self, limits: Optional[Dict[str, float]] = None) -> None:
        self.limits = limits or {
            "cpu_percent": 90.0,
            "mem_mb": 2048.0,
            "disk_mb": 4096.0,
            "energy_units": 1000.0,
        }
        self.usage = ResourceUsage()
        self.warnings: List[str] = []

    def consume(self, **usage: float) -> Dict[str, Any]:
        self.usage.cpu_percent += float(usage.get("cpu_percent", 0.0))
        self.usage.mem_mb += float(usage.get("mem_mb", 0.0))
        self.usage.disk_mb += float(usage.get("disk_mb", 0.0))
        self.usage.energy_units += float(usage.get("energy_units", 0.0))
        return self.check_limits()

    def account(self, usage: Dict[str, Any]) -> Dict[str, Any]:
        return self.consume(
            cpu_percent=float(usage.get("cpu_percent", 0.0)),
            mem_mb=float(usage.get("mem_mb", 0.0)),
            disk_mb=float(usage.get("disk_mb", 0.0)),
            energy_units=float(usage.get("energy_units", 0.0)),
        )

    def check_limits(self) -> Dict[str, Any]:
        exceeded = []
        for key, limit in self.limits.items():
            current = getattr(self.usage, key, 0.0)
            if current > limit:
                exceeded.append(key)
        if exceeded:
            self.warnings.append(f"resource limit exceeded: {', '.join(exceeded)}")
            return {"status": "exceeded", "exceeded": exceeded, "warnings": self.warnings}
        return {"status": "ok", "usage": self.usage.__dict__}

    def is_circuit_open(self) -> bool:
        return any(getattr(self.usage, k, 0.0) > v for k, v in self.limits.items())

    def snapshot(self) -> Dict[str, Any]:
        return {
            "usage": self.usage.__dict__,
            "limits": self.limits,
            "warnings": self.warnings,
        }
