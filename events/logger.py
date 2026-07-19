from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


class JsonlEventBus:
    def __init__(self, path: str = "runtime/event_bus.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        line = json.dumps({"event": event, "payload": payload, "ts": time.time()})
        self.path.write_text((self.path.read_text() if self.path.exists() else "") + line + "\n")
        return payload


class EventLogger:
    def __init__(self, bus: JsonlEventBus) -> None:
        self.bus = bus
        self.state: Dict[str, Dict[str, Any]] = {}

    def transition(self, task_id: str, from_s: str, to: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        state = {
            "task_id": task_id,
            "from": from_s,
            "to": to,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "metadata": metadata or {},
        }
        self.state.setdefault(task_id, {})["last"] = state
        self.bus.emit("state_transition", state)
        return state

    def verification(self, task_id: str, passed: bool, score: float, evidence: Optional[str] = None) -> Dict[str, Any]:
        event = {"task_id": task_id, "passed": passed, "score": score, "evidence": evidence}
        self.bus.emit("verification", event)
        return event

    def approval(self, task_id: str, identity: str, granted: bool) -> Dict[str, Any]:
        event = {"task_id": task_id, "identity": identity, "granted": granted}
        self.bus.emit("approval", event)
        return event
