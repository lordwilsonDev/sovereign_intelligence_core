from __future__ import annotations

import re
from typing import Any, Dict


class GroundingGate:
    def __init__(self, max_unsupported_terms: int = 2) -> None:
        self.max_unsupported_terms = max_unsupported_terms
        self._unsupported_patterns = re.compile(
            r"\b(guaranteed|always|never|impossible|certainly|definitely)\b",
            re.IGNORECASE,
        )

    def inspect(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        text = str(candidate.get("message", "") or candidate.get("content", "") or "")
        if not text:
            return {"grounded": True, "risk": "empty", "unsupported_terms": []}
        terms = self._unsupported_patterns.findall(text)
        grounded = len(terms) <= self.max_unsupported_terms
        return {
            "grounded": grounded,
            "risk": "unsupported_claims" if not grounded else "low",
            "unsupported_terms": list(dict.fromkeys(terms)),
        }

    def fuse(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        result = dict(candidate)
        result["grounding"] = self.inspect(candidate)
        result["confidence"] = min(float(result.get("confidence", 1.0)), 0.75 if not result["grounding"]["grounded"] else 1.0)
        return result
