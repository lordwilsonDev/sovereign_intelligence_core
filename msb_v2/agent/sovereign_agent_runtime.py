"""Sovereign Agent Runtime (SAR) Phase 0 core.

This module implements the minimal persistent runtime described in the
Sovereign Agent Runtime Blueprint.  It provides:

* ``SovereignAgentRuntime`` - daemon-style job loop with shutdown control.
* ``LoveGateway`` - lightweight epistemic quarantine for inbound payloads.
* ``AgentProfile`` - a named identity partition with its own memory &
  permission policy stubs.

All I/O, network, and tool-execution surfaces are deferred to later phases.
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional


logger = logging.getLogger("msb_v2.sar")


@dataclass
class AgentProfile:
    """A sovereign employee record stub."""

    profile_id: str
    display_name: str
    memory_partition: str
    tool_allowlist: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "display_name": self.display_name,
            "memory_partition": self.memory_partition,
            "tool_allowlist": self.tool_allowlist,
            "metadata": self.metadata,
        }


class LoveGateway:
    """Quarantine inbound payloads before they reach a profile."""

    def __init__(self, ttl: float = 2.0) -> None:
        self._quarantine: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self.ttl = ttl

    def quarantine(self, payload: Dict[str, Any], reason: str) -> Dict[str, Any]:
        record = {
            "quarantined_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "payload": payload,
        }
        with self._lock:
            self._quarantine.append(record)
        logger.warning("love_gateway.quarantine: %s", reason)
        return {"quarantined": True, "reason": reason, "record": record}

    def rejected(self, payload: Dict[str, Any], reason: str) -> Dict[str, Any]:
        return {"accepted": False, "reason": reason, "record": {"payload": payload}}

    def recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._quarantine)[-max(1, limit) :]


class SovereignAgentRuntime:
    """Persistent daemon-style runtime for one sovereign profile."""

    def __init__(
        self,
        profile: AgentProfile,
        love_gateway: Optional[LoveGateway] = None,
        poll_interval: float = 0.1,
    ) -> None:
        self.profile = profile
        self.love_gateway = love_gateway or LoveGateway()
        self.poll_interval = poll_interval
        self._queue: List[Dict[str, Any]] = []
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.started_at: Optional[datetime] = None
        self.processed_count: int = 0

    def submit(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Accept or quarantine an inbound payload."""
        if not isinstance(payload, dict):
            return self.love_gateway.rejected(payload, "payload_not_dict")
        if payload.get("type") in {"ignore", "injection_attempt"}:
            return self.love_gateway.quarantine(payload, "epistemic_risk")
        if "content" not in payload:
            return self.love_gateway.rejected(payload, "missing_content")
        with self._lock:
            self._queue.append(payload)
        return {"accepted": True, "queue_depth": len(self._queue)}

    def _process(self, payload: Dict[str, Any]) -> None:
        content = payload.get("content", "")
        if content:
            self.processed_count += 1

    def _run(self) -> None:
        while not self._stop.is_set():
            with self._lock:
                batch = self._queue[: self._max_batch]
                self._queue[: self._max_batch] = []
            for item in batch:
                if self._stop.is_set():
                    break
                try:
                    self._process(item)
                except Exception as exc:
                    logger.error("runtime.process_failed: %s", exc)
            time.sleep(self.poll_interval)

    @property
    def _max_batch(self) -> int:
        return max(1, min(20, 2))

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self.started_at = datetime.now(timezone.utc)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2.0)

    def state(self) -> Dict[str, Any]:
        with self._lock:
            queue_depth = len(self._queue)
        return {
            "profile_id": self.profile.profile_id,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "queue_depth": queue_depth,
            "processed_count": self.processed_count,
            "quarantine_count": len(self.love_gateway.recent(limit=2000)),
        }
