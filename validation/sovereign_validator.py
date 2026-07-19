from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from validation.endpoint_registry import endpoint_registry


class SovereignValidationResult:
    def __init__(self) -> None:
        self.passed: List[str] = []
        self.failed: List[Dict[str, Any]] = []
        self.score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "failed": self.failed,
            "score": self.score,
        }
