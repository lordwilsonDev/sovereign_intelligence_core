from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


class AuditStore:
    def __init__(self, root: str | Path = "runtime/audit") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._path = self.root / "events.jsonl"

    def append(self, event) -> None:  # type: ignore[no-untyped-def]
        data = event.to_dict() if hasattr(event, "to_dict") else dict(event)
        line = json.dumps(data, separators=(",", ":"), default=str)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    def read(self, limit: int | None = None) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        with self._path.open("r", encoding="utf-8") as handle:
            lines = handle.readlines()
        events: list[dict[str, Any]] = []
        if limit is not None:
            lines = lines[-limit:]
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return events

    def clear(self) -> None:
        self._path.unlink(missing_ok=True)
