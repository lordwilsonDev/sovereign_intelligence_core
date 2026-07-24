from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class InferenceReceipt:
    receipt_id: str
    created_at: str
    model_id: str
    prompt_hash: str
    response_hash: str
    backend: str
    metadata: Dict[str, Any]

    @staticmethod
    def build(model_id: str, prompt: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> InferenceReceipt:
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        response_hash = hashlib.sha256(text.encode()).hexdigest()
        receipt_id = hashlib.sha256(f"{prompt_hash}:{response_hash}:{model_id}".encode()).hexdigest()[:12]
        return InferenceReceipt(
            receipt_id=receipt_id,
            created_at=datetime.now(timezone.utc).isoformat(),
            model_id=model_id,
            prompt_hash=prompt_hash,
            response_hash=response_hash,
            backend="ollama",
            metadata=metadata or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "created_at": self.created_at,
            "model_id": self.model_id,
            "prompt_hash": self.prompt_hash,
            "response_hash": self.response_hash,
            "backend": self.backend,
            "metadata": self.metadata,
        }

    def write(self, directory: str) -> Path:
        root = Path(directory)
        root.mkdir(parents=True, exist_ok=True)
        path = root / f"inference-{self.receipt_id}.json"
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return path
