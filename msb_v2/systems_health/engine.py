from __future__ import annotations

import logging
import os
import platform
import subprocess
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

import psutil


class HealthStatus(str, Enum):
    healthy = "healthy"
    degraded = "degraded"
    unhealthy = "unhealthy"
    unknown = "unknown"


class CheckMethod(str, Enum):
    http = "http"
    function = "function"
    subprocess = "subprocess"


@dataclass(frozen=True)
class HealthCheck:
    name: str
    status: HealthStatus
    detail: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    duration_ms: float = 0.0


@dataclass(frozen=True)
class SystemHealthReport:
    status: str
    checks: List[HealthCheck]
    storage: Dict[str, Any] = field(default_factory=dict)
    cpu: Dict[str, Any] = field(default_factory=dict)
    memory: Dict[str, Any] = field(default_factory=dict)
    processes: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


logger = logging.getLogger(__name__)


class SystemsHealthEngine:
    def __init__(self) -> None:
        self._history: List[SystemHealthReport] = []
        self._max_history = 500
        self._lock = threading.Lock()
        self._last_zombie_pid_snapshot: set = set()
        self._process_baselines: Dict[str, float] = {}

    def run_check(self) -> SystemHealthReport:
        checks: List[HealthCheck] = []
        storage = self._check_storage()
        checks.append(HealthCheck(name="storage", status=storage.get("status", HealthStatus.unknown), detail=storage.get("detail", ""), duration_ms=float(storage.get("duration_ms", 0))))
        cpu = self._check_cpu()
        checks.append(HealthCheck(name="cpu", status=cpu.get("status", HealthStatus.unknown), detail=cpu.get("detail", ""), duration_ms=float(cpu.get("duration_ms", 0))))
        memory = self._check_memory()
        checks.append(HealthCheck(name="memory", status=memory.get("status", HealthStatus.unknown), detail=memory.get("detail", ""), duration_ms=float(memory.get("duration_ms", 0))))
        processes = self._check_processes()
        checks.append(HealthCheck(name="processes", status=processes.get("status", HealthStatus.unknown), detail=processes.get("detail", ""), duration_ms=float(processes.get("duration_ms", 0))))
        critical_unhealthy = [c.name for c in checks if c.status == HealthStatus.unhealthy]
        overall = "RED" if critical_unhealthy else ("YELLOW" if any(c.status == HealthStatus.degraded for c in checks) else "GREEN")
        report = SystemHealthReport(status=overall, checks=checks, storage=storage, cpu=cpu, memory=memory, processes=processes)
        with self._lock:
            self._history.append(report)
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history:]
        return report

    def _check_storage(self) -> Dict[str, Any]:
        start = time.perf_counter()
        detail = ""
        status = HealthStatus.healthy
        try:
            usage = os.statvfs("/")
            total = usage.f_blocks * usage.f_frsize
            used = (usage.f_blocks - usage.f_bfree) * usage.f_frsize
            percent = (used / total) * 100 if total else 0.0
            duration_ms = (time.perf_counter() - start) * 1000
            if percent > 95:
                status = HealthStatus.unhealthy
                detail = f"Disk {percent:.1f}% full"
            elif percent > 90:
                status = HealthStatus.degraded
                detail = f"Disk {percent:.1f}% full"
            return {"status": status, "detail": detail, "duration_ms": duration_ms, "percent": percent}
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            return {"status": HealthStatus.unhealthy, "detail": str(exc)[:120], "duration_ms": duration_ms, "percent": 0.0}

    def _check_cpu(self) -> Dict[str, Any]:
        start = time.perf_counter()
        detail = ""
        status = HealthStatus.healthy
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            duration_ms = (time.perf_counter() - start) * 1000
            if cpu_percent > 95:
                status = HealthStatus.unhealthy
                detail = f"CPU usage {cpu_percent:.1f}%"
            elif cpu_percent > 85:
                status = HealthStatus.degraded
                detail = f"CPU usage {cpu_percent:.1f}%"
            return {"status": status, "detail": detail, "duration_ms": duration_ms, "cpu_percent": cpu_percent}
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            return {"status": HealthStatus.unhealthy, "detail": str(exc)[:120], "duration_ms": duration_ms, "cpu_percent": 0.0}

    def _check_memory(self) -> Dict[str, Any]:
        start = time.perf_counter()
        detail = ""
        status = HealthStatus.healthy
        try:
            mem = psutil.virtual_memory()
            duration_ms = (time.perf_counter() - start) * 1000
            if mem.percent > 95:
                status = HealthStatus.unhealthy
                detail = f"Memory {mem.percent:.1f}%"
            elif mem.percent > 85:
                status = HealthStatus.degraded
                detail = f"Memory {mem.percent:.1f}%"
            return {"status": status, "detail": detail, "duration_ms": duration_ms, "memory_percent": mem.percent, "available_mb": mem.available / (1024 * 1024)}
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            return {"status": HealthStatus.unhealthy, "detail": str(exc)[:120], "duration_ms": duration_ms, "memory_percent": 0.0}

    def _check_processes(self) -> Dict[str, Any]:
        start = time.perf_counter()
        status = HealthStatus.healthy
        detail = ""
        try:
            current_pids = set()
            zombies = 0
            for proc in psutil.process_iter(['pid', 'status', 'name']):
                try:
                    info = proc.info
                    current_pids.add(info['pid'])
                    if info['status'] == psutil.STATUS_ZOMBIE:
                        zombies += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            new_zombies = zombies > 0
            duration_ms = (time.perf_counter() - start) * 1000
            if new_zombies:
                status = HealthStatus.degraded if zombies < 5 else HealthStatus.unhealthy
                detail = f"{zombies} zombie process{'es' if zombies != 1 else ''}"
            return {"status": status, "detail": detail, "duration_ms": duration_ms, "zombies": zombies}
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            return {"status": HealthStatus.unhealthy, "detail": str(exc)[:120], "duration_ms": duration_ms, "zombies": 0}

    def history(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            items = self._history[-max(0, limit):]
            out = []
            for report in items:
                out.append({
                    "status": report.status,
                    "checks": [c.__dict__ for c in report.checks],
                    "timestamp": report.timestamp,
                })
            return out
