from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class SacAuditEvent:
    def __init__(
        self,
        event_id: str,
        kind: str,
        actor: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
        timestamp: Optional[str] = None,
    ) -> None:
        self.event_id = event_id
        self.kind = kind
        self.actor = actor
        self.payload = payload or {}
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()


class SacAuditLog:
    def __init__(self, path: Optional[str] = None) -> None:
        self.path = Path(path or os.environ.get("MSB_SAC_AUDIT_PATH", "./runtime/sac_audit.jsonl"))
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: SacAuditEvent) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({
                "event_id": event.event_id,
                "kind": event.kind,
                "actor": event.actor,
                "payload": event.payload,
                "timestamp": event.timestamp,
            }) + "\n")

    def recent(self, limit: int = 100) -> List[Dict[str, Any]]:
        events: List[Dict[str, Any]] = []
        try:
            text = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return events
        for line in text.splitlines()[-limit:]:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return events


_DEFAULT_LOG: Optional[SacAuditLog] = None


def get_audit_log(path: Optional[str] = None) -> SacAuditLog:
    global _DEFAULT_LOG
    if _DEFAULT_LOG is None or path is not None:
        _DEFAULT_LOG = SacAuditLog(path=path)
    return _DEFAULT_LOG
