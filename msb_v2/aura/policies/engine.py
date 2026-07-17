from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


class Policy:
    name: str = "base"
    description: str = ""

    def apply(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        return text


class PIIRedactionPolicy(Policy):
    name = "pii_redact"
    description = "Redact SSN, phone, and email patterns"

    def apply(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED-SSN]", text)
        text = re.sub(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b", "[REDACTED-PHONE]", text)
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED-EMAIL]", text)
        return text


class PolicyEngine:
    def __init__(self, policies: Optional[List[Policy]] = None) -> None:
        self.policies = policies or [PIIRedactionPolicy()]
        self._registry = {p.name: p for p in self.policies}

    def apply(self, text: str, context: Optional[Dict[str, Any]] = None) -> str:
        for policy in self.policies:
            text = policy.apply(text, context)
        return text

    def get(self, name: str) -> Optional[Policy]:
        return self._registry.get(name)
