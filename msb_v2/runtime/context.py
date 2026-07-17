from __future__ import annotations

import time
from typing import Optional

from msb_v2.core.background_tasks import BackgroundTaskRegistry
from msb_v2.runtime.capabilities import CapabilityEvent
from msb_v2.runtime.config import RuntimeConfig
from msb_v2.runtime.event_log import PersistentEventLog
from msb_v2.runtime.events import EventBus
from msb_v2.runtime.health import HealthManager
from msb_v2.runtime.lifecycle import LifecycleResult, LifecycleManager
from msb_v2.runtime.logging import configure_logging
from msb_v2.runtime.resources import ResourceManager
from msb_v2.runtime.secrets import SecretsLoader
from msb_v2.runtime.version_registry import VersionRegistry
from msb_v2.runtime.worker_pool import WorkerPool


class RuntimeContext:
    def __init__(self, config: Optional[RuntimeConfig] = None) -> None:
        self.config = config or RuntimeConfig()
        self.lifecycle = LifecycleManager()
        self.event_log = PersistentEventLog(
            self.config.event_log_path,
            flush_interval=self.config.event_log_flush_interval,
            batch_size=self.config.event_log_batch_size,
        )
        self.events = EventBus(persistent_log=self.event_log)
        self.workers = WorkerPool(concurrency=self.config.worker_concurrency)
        self.versions = VersionRegistry()
        self.secrets = SecretsLoader()
        self.health = HealthManager(check_interval=10.0)
        self.resources = ResourceManager(max_memory_mb=self.config.max_memory_mb)
        self.background = BackgroundTaskRegistry(name="runtime")
        configure_logging(self.config.log_level)
        self.started_at: float = 0.0
        self.lifecycle.record_component("event_log")
        self.lifecycle.record_component("workers")
        self.lifecycle.record_component("health")
        self.lifecycle.record_component("resources")

    def start(self) -> LifecycleResult:
        result = self.lifecycle.initialize()
        if not result.success:
            return result
        self.started_at = time.time()
        self.lifecycle.start()
        self.health.record("running", detail="runtime started")
        return result

    def stop(self, *, wait: bool = True) -> LifecycleResult:
        self.health.record("stopped", detail="runtime stopped")
        result = self.lifecycle.shutdown()
        self.workers.stop(wait=wait)
        return result

    def record_capability(self, event: CapabilityEvent) -> CapabilityEvent:
        self.health.record(
            event.status,
            detail=event.detail or event.capability,
            module=event.module,
            capability=event.capability,
        )
        return event

    def replay_events(self, limit: int = 100) -> list[dict]:
        return self.event_log.query(limit=limit)

    def summary(self) -> dict:
        worker_status = self.workers.status() if self.workers else {}
        try:
            last_events = self.event_log.query(limit=10)
        except Exception:
            last_events = []
        return {
            "lifecycle": self.lifecycle.summary(),
            "app": self.config.app_name,
            "env": self.config.env,
            "port": self.config.port,
            "host": self.config.host,
            "reasoning_scorer": self.config.reasoning_scorer,
            "max_tool_calls": self.config.max_tool_calls,
            "max_latency_ms": self.config.max_latency_ms,
            "uptime_seconds": time.time() - self.started_at if self.started_at else 0.0,
            "versions": [
                {
                    "service": k,
                    "version": v.version,
                    "sha": v.sha,
                    "since": v.since,
                }
                for k, v in self.versions.all().items()
            ],
            "loaded_plugins": self.events.topics(),
            "worker_pool": worker_status,
            "event_log": {
                "enabled": True,
                "last_events": last_events,
            },
            "health": self.health.summary(),
            "resources": self.resources.snapshot(),
        }
