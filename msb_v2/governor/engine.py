from __future__ import annotations

import datetime
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class HarnessRegistration:
    name: str
    url: str
    health_endpoint: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True


@dataclass
class HarnessHealth:
    name: str
    status: str = "unknown"
    last_check: Optional[str] = None
    http_status: Optional[int] = None
    sac_ok: bool = True
    error: Optional[str] = None
    failure_count: int = 0


class GovernorEngine:
    def __init__(self) -> None:
        self._harnesses: Dict[str, HarnessRegistration] = {}
        self._health: Dict[str, HarnessHealth] = {}
        self._lock = threading.Lock()
        self._poll_thread: Optional[threading.Thread] = None
        self._interval_seconds = 60

    def register_harness(self, name: str, url: str, health_endpoint: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        with self._lock:
            registration = HarnessRegistration(name=name, url=url, health_endpoint=health_endpoint, metadata=metadata or {})
            self._harnesses[name] = registration
            self._health.setdefault(name, HarnessHealth(name=name))
        return {"status": "registered", "name": name}

    def unregister_harness(self, name: str) -> Dict[str, Any]:
        with self._lock:
            if name in self._harnesses:
                del self._harnesses[name]
                self._health.pop(name, None)
                return {"status": "unregistered", "name": name}
            return {"status": "not_found", "name": name}

    def harnesses(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [self._registration_to_dict(r) for r in self._harnesses.values()]

    def health_snapshot(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [self._health_to_dict(h) for h in self._health.values()]

    def enable_harness(self, name: str) -> Dict[str, Any]:
        with self._lock:
            registration = self._harnesses.get(name)
            if not registration:
                return {"status": "not_found", "name": name}
            registration.enabled = True
            self._health[name].status = "unknown"
        return {"status": "enabled", "name": name}

    def disable_harness(self, name: str) -> Dict[str, Any]:
        with self._lock:
            registration = self._harnesses.get(name)
            if not registration:
                return {"status": "not_found", "name": name}
            registration.enabled = False
            self._health[name] = HarnessHealth(name=name, status="disabled")
        return {"status": "disabled", "name": name}

    def start_polling(self) -> None:
        def _loop() -> None:
            while True:
                try:
                    self.check_all_harnesses()
                except Exception:
                    pass
                time.sleep(self._interval_seconds)

        self._poll_thread = threading.Thread(target=_loop, daemon=True)
        self._poll_thread.start()

    def check_all_harnesses(self) -> List[Dict[str, Any]]:
        import urllib.request
        import urllib.error

        snapshots: List[Dict[str, Any]] = []
        with self._lock:
            names = list(self._harnesses.keys())
        for name in names:
            snapshots.append(self.check_harness(name))
        return snapshots

    def check_harness(self, name: str) -> Dict[str, Any]:
        import urllib.request
        import urllib.error

        with self._lock:
            registration = self._harnesses.get(name)
            health = self._health.setdefault(name, HarnessHealth(name=name))
            if not registration or not registration.enabled:
                return self._health_to_dict(health)

        try:
            req = urllib.request.Request(registration.health_endpoint, method="GET")
            with urllib.request.urlopen(req, timeout=5) as response:
                status = int(response.status)
                health.http_status = status
                if status == 200:
                    health.status = "healthy"
                    health.failure_count = 0
                    health.error = None
                else:
                    health.status = "unhealthy"
                    health.failure_count += 1
                    health.error = f"http_{status}"
        except urllib.error.HTTPError as exc:
            health.status = "unhealthy"
            health.http_status = int(exc.code)
            health.failure_count += 1
            health.error = f"http_{exc.code}"
        except Exception as exc:
            health.status = "unreachable"
            health.http_status = None
            health.failure_count += 1
            health.error = str(exc)[:120]

        health.last_check = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return self._health_to_dict(health)

    def _health_to_dict(self, health: HarnessHealth) -> Dict[str, Any]:
        return {
            "name": health.name,
            "status": health.status,
            "last_check": health.last_check,
            "http_status": health.http_status,
            "sac_ok": health.sac_ok,
            "error": health.error,
            "failure_count": health.failure_count,
        }

    def _registration_to_dict(self, registration: HarnessRegistration) -> Dict[str, Any]:
        return {
            "name": registration.name,
            "url": registration.url,
            "health_endpoint": registration.health_endpoint,
            "enabled": registration.enabled,
            "metadata": registration.metadata,
        }
