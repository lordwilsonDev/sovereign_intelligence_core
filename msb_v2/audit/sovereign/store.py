from __future__ import annotations

from pathlib import Path
from typing import Optional

from msb_v2.audit.sovereign.merkle import AuditMerkleChain


class SovereignAuditStore:
    def __init__(self, root: str | Path = "runtime/audit", log_name: str = "events_merkle.jsonl") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._path = self.root / "events.jsonl"
        self._legacy = self._path.exists()
        self.merkle = AuditMerkleChain(self.root / log_name)

    def append(self, event) -> None:
        data = event.to_dict() if hasattr(event, "to_dict") else dict(event)
        try:
            self.merkle.append(data)
        except Exception:
            pass
        line = __import__("json").dumps(data, separators=(",", ":"), default=str)
        with self._path.open("a", encoding="utf-8") as handle:
            handle.write(line +"\n")

    def read(self, limit: int | None = None):
        if not self._path.exists():
            return []
        with self._path.open("r", encoding="utf-8") as handle:
            lines = handle.readlines()
        events = []
        if limit is not None:
            lines = lines[-limit:]
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(__import__("json").loads(line))
            except Exception:
                continue
        return events

    def clear(self) -> None:
        self._path.unlink(missing_ok=True)
