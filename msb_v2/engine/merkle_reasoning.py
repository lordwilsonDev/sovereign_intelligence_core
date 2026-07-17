from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class MerkleStep:
    step_id: str
    step_type: str
    payload: dict[str, Any]
    prev_hash: str = ""
    step_hash: str = ""
    timestamp: str = ""


class MerkleReasoningChain:
    def __init__(self) -> None:
        self.chain: list[MerkleStep] = []
        self._root_hash = ""

    def append(self, step_type: str, payload: dict[str, Any]) -> MerkleStep:
        prev_hash = self._root_hash
        raw = json_dumps({"step_type": step_type, "payload": payload, "prev": prev_hash})
        step_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        step = MerkleStep(
            step_id=f"step-{len(self.chain)+1}",
            step_type=step_type,
            payload=payload,
            prev_hash=prev_hash,
            step_hash=step_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(step)
        self._root_hash = step_hash
        return step

    def root_hash(self) -> str:
        return self._root_hash

    def snapshot(self, label: str) -> dict[str, Any]:
        return {
            "label": label,
            "root": self.root_hash(),
            "len": len(self.chain),
            "steps": [
                {
                    "step_id": s.step_id,
                    "step_type": s.step_type,
                    "prev_hash": s.prev_hash,
                    "step_hash": s.step_hash,
                    "ts": s.timestamp,
                }
                for s in self.chain
            ],
        }

    def verify(self) -> bool:
        expected = ""
        for s in self.chain:
            raw = json_dumps({"step_type": s.step_type, "payload": s.payload, "prev": expected})
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if s.step_hash != calc:
                return False
            if s.prev_hash != expected and expected != "":
                return False
            expected = s.step_hash
        self._root_hash = expected
        return True


def json_dumps(obj: Any) -> str:
    import json
    return json.dumps(obj, sort_keys=True, default=str)
