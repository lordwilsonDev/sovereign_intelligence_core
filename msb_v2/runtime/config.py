from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class RuntimeConfig:
    app_name: str = "msb-v2"
    env: str = field(default_factory=lambda: os.getenv("MSB_ENV", "dev"))
    port: int = field(default_factory=lambda: int(os.getenv("MSB_PORT", "8766")))
    host: str = field(default_factory=lambda: os.getenv("MSB_HOST", "127.0.0.1"))
    log_level: str = field(default_factory=lambda: os.getenv("MSB_LOG_LEVEL", "info"))
    max_tool_calls: int = field(default_factory=lambda: int(os.getenv("MSB_MAX_TOOL_CALLS", "10")))
    max_latency_ms: int = field(default_factory=lambda: int(os.getenv("MSB_MAX_LATENCY_MS", "5000")))
    reasoning_scorer: bool = field(default_factory=lambda: os.getenv("MSB_REASONING_SCORER", "0") == "1")
    event_log_path: str = field(default_factory=lambda: os.getenv("MSB_EVENT_LOG_PATH", "./runtime_events.db"))
    event_log_flush_interval: float = field(default_factory=lambda: float(os.getenv("MSB_EVENT_LOG_FLUSH_INTERVAL", "0.1")))
    event_log_batch_size: int = field(default_factory=lambda: int(os.getenv("MSB_EVENT_LOG_BATCH_SIZE", "100")))
    worker_concurrency: int = field(default_factory=lambda: int(os.getenv("MSB_WORKER_CONCURRENCY", "4")))
    max_memory_mb: Optional[int] = field(default_factory=lambda: _optional_int_env("MSB_MAX_MEMORY_MB"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "app_name": self.app_name,
            "env": self.env,
            "port": self.port,
            "host": self.host,
            "log_level": self.log_level,
            "max_tool_calls": self.max_tool_calls,
            "max_latency_ms": self.max_latency_ms,
            "reasoning_scorer": self.reasoning_scorer,
            "event_log_path": self.event_log_path,
            "event_log_flush_interval": self.event_log_flush_interval,
            "event_log_batch_size": self.event_log_batch_size,
            "worker_concurrency": self.worker_concurrency,
            "max_memory_mb": self.max_memory_mb,
        }


def _optional_int_env(name: str) -> Optional[int]:
    value = os.getenv(name)
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None
