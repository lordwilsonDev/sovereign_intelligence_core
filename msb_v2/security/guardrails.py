"""Policy-as-code checks applied before model or connector use."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


DEFAULT_PATTERNS = {
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
}


@dataclass(frozen=True)
class GuardrailResult:
    allowed: bool
    text: str
    findings: tuple[str, ...] = ()
    reason: str | None = None


@dataclass
class Guardrails:
    patterns: dict[str, str] = field(default_factory=lambda: DEFAULT_PATTERNS.copy())
    blocked_terms: set[str] = field(default_factory=set)
    min_relevance: float = 0.0

    def inspect(self, text: str, *, relevance: float | None = None) -> GuardrailResult:
        findings: list[str] = []
        redacted = text
        for name, pattern in self.patterns.items():
            redacted, replacements = re.subn(pattern, f"[{name.upper()}_REDACTED]", redacted)
            if replacements:
                findings.append(name)
        lowered = text.casefold()
        blocked = next((term for term in self.blocked_terms if term.casefold() in lowered), None)
        if blocked:
            return GuardrailResult(False, redacted, tuple(findings), f"blocked term: {blocked}")
        if relevance is not None and relevance < self.min_relevance:
            return GuardrailResult(False, redacted, tuple(findings), "below relevance threshold")
        return GuardrailResult(True, redacted, tuple(findings))
