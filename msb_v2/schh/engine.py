from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from msb_v2.core.health import SystemReadiness


class ComponentType(str, Enum):
    harness = "harness"
    database = "database"
    gateway = "gateway"
    external_service = "external-service"
    model = "model"


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
class Component:
    id: str
    name: str
    type: ComponentType = ComponentType.harness
    health_endpoint: str = ""
    check_method: CheckMethod = CheckMethod.http
    check_interval_seconds: int = 30
    timeout_seconds: int = 5
    critical: bool = True
    auto_heal: bool = False
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CheckResult:
    component_id: str
    status: HealthStatus
    duration_ms: float
    detail: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


logger = logging.getLogger(__name__)


class Registry:
    def __init__(self) -> None:
        self._components: Dict[str, Component] = {}
        self._lock = threading.Lock()

    def register(self, component: Component) -> None:
        with self._lock:
            self._components[component.id] = component

    def unregister(self, component_id: str) -> None:
        with self._lock:
            self._components.pop(component_id, None)

    def get(self, component_id: str) -> Optional[Component]:
        with self._lock:
            return self._components.get(component_id)

    def all(self) -> List[Component]:
        with self._lock:
            return list(self._components.values())


class HealthEngine:
    def __init__(self, registry: Optional[Registry] = None) -> None:
        self._registry = registry or Registry()
        self._history: List[CheckResult] = []
        self._max_history = 1000
        self._lock = threading.Lock()
        self._registry_lock = threading.Lock()

    def register_defaults(self) -> None:
        defaults = [
            Component(id="star", name="STAR Scheduler", type=ComponentType.harness, health_endpoint="/star/star/health", check_method=CheckMethod.http, critical=True, auto_heal=False),
            Component(id="scth", name="SCTH Telemetry", type=ComponentType.harness, health_endpoint="/scth/health", check_method=CheckMethod.http, critical=True, auto_heal=False),
            Component(id="snh", name="Notification Harness", type=ComponentType.harness, health_endpoint="/sn/status", check_method=CheckMethod.http, critical=False, auto_heal=False),
            Component(id="governor", name="Sovereign Harness Governor", type=ComponentType.harness, health_endpoint="/governor/health", check_method=CheckMethod.http, critical=True, auto_heal=False),
            Component(id="sac", name="Sovereign Autonomy Core", type=ComponentType.harness, health_endpoint="/sac/status", check_method=CheckMethod.http, critical=True, auto_heal=False),
            Component(id="audit", name="Audit Merkle Chain", type=ComponentType.harness, health_endpoint="/audit/recent", check_method=CheckMethod.http, critical=True, auto_heal=False),
            Component(id="runtime", name="Runtime Lifecycle", type=ComponentType.harness, health_endpoint="/runtime/ping", check_method=CheckMethod.http, critical=True, auto_heal=False),
        ]
        for component in defaults:
            self._registry.register(component)

    def _http_check(self, component: Component, client: Any) -> CheckResult:
        start = time.perf_counter()
        endpoint = component.health_endpoint or "/"
        try:
            response = client.get(endpoint)
            duration_ms = (time.perf_counter() - start) * 1000
            if response.status_code == 200:
                status = HealthStatus.healthy
                detail = f"HTTP {response.status_code}"
            else:
                status = HealthStatus.degraded
                detail = f"HTTP {response.status_code}"
            return CheckResult(component_id=component.id, status=status, duration_ms=duration_ms, detail=detail)
        except Exception as exc:
            duration_ms = (time.perf_counter() - start) * 1000
            return CheckResult(component_id=component.id, status=HealthStatus.unhealthy, duration_ms=duration_ms, detail=str(exc)[:120])

    def _function_check(self, component: Component) -> CheckResult:
        start = time.perf_counter()
        endpoint = component.health_endpoint
        func = _FUNCTION_REGISTRY.get(endpoint)
        detail = ""
        status = HealthStatus.unknown
        if callable(func):
            try:
                result = func()
                status = HealthStatus.healthy if result else HealthStatus.unhealthy
                detail = f"function={endpoint}"
            except Exception as exc:
                status = HealthStatus.unhealthy
                detail = str(exc)[:120]
        else:
            status = HealthStatus.unknown
            detail = f"function not found: {endpoint}"
        duration_ms = (time.perf_counter() - start) * 1000
        return CheckResult(component_id=component.id, status=status, duration_ms=duration_ms, detail=detail)

    def check_component(self, component: Component, client: Any = None) -> CheckResult:
        if component.check_method == CheckMethod.http:
            return self._http_check(component, client)
        if component.check_method == CheckMethod.function:
            return self._function_check(component)
        return CheckResult(component_id=component.id, status=HealthStatus.unknown, duration_ms=0.0, detail="unsupported check method")

    def run_checks(self, client: Any = None) -> List[CheckResult]:
        results: List[CheckResult] = []
        components = self._registry.all()
        for component in components:
            result = self.check_component(component, client=client)
            results.append(result)
            with self._lock:
                self._history.append(result)
                if len(self._history) > self._max_history:
                    self._history = self._history[-self._max_history:]
            if result.status == HealthStatus.unhealthy:
                logger.warning("component unhealthy: %s (%s)", component.id, result.detail)
        return results

    def readiness(self) -> SystemReadiness:
        components = self._registry.all()
        results = [r for r in self._history[-len(components):] if r.component_id in {c.id for c in components}]
        latest: Dict[str, CheckResult] = {}
        for result in reversed(results):
            latest.setdefault(result.component_id, result)
        degraded = [c.id for c in components if latest.get(c.id, CheckResult(c.id, HealthStatus.unknown, 0)).status == HealthStatus.degraded]
        unhealthy = [c.id for c in components if latest.get(c.id, CheckResult(c.id, HealthStatus.unknown, 0)).status == HealthStatus.unhealthy]
        critical_unhealthy = [c.id for c in components if c.critical and c.id in unhealthy]
        healthy_count = sum(1 for c in components if c.id not in degraded and c.id not in unhealthy)
        status = "GREEN"
        if critical_unhealthy:
            status = "RED"
        elif unhealthy or degraded:
            status = "YELLOW"
        return SystemReadiness(status=status, healthy_count=healthy_count, degraded_count=len(degraded), unhealthy_count=len(unhealthy), critical_unhealthy=critical_unhealthy)

    def history(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            return [r.__dict__ for r in self._history[-max(0, limit):]]


_FUNCTION_REGISTRY: Dict[str, Callable[[], bool]] = {}


def register_function_check(name: str, func: Callable[[], bool]) -> None:
    _FUNCTION_REGISTRY[name] = func
