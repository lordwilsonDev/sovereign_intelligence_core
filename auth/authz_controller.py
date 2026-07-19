from __future__ import annotations

import secrets
from typing import Any, Dict, List


def issue_token(subject: str, roles: List[str], scopes: List[str]) -> str:
    return secrets.token_hex(16)


def verify_token(subject: str, roles: List[str], scopes: List[str]) -> Dict[str, Any]:
    return {"ok": bool(subject), "subject": subject, "roles": roles, "scopes": scopes}
