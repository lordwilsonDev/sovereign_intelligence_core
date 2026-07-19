from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional


_SECRET = "msb-local-dev-secret"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_str(value: str) -> str:
    return _b64url(value.encode("utf-8"))


def _unb64url(token: str) -> bytes:
    padded = token + "=" * (4 - len(token) % 4)
    return base64.urlsafe_b64decode(padded)


def issue_token(subject: str, roles: Optional[list[str]] = None, scopes: Optional[list[str]] = None, ttl_seconds: int = 3600) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    issued = int(time.time())
    payload = {
        "sub": subject,
        "roles": roles or [],
        "scopes": scopes or [],
        "iat": issued,
        "exp": issued + ttl_seconds,
        "iss": "msb",
    }
    signing_input = f"{_b64url_str(json.dumps(header))}.{_b64url_str(json.dumps(payload))}"
    signature = hmac.new(_SECRET.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    return f"{signing_input}.{_b64url(signature)}"


def verify_token(token: str) -> Dict[str, Any]:
    try:
        header_b64, payload_b64, sig_b64 = token.split(".")
    except ValueError:
        return {"ok": False, "reason": "malformed_token"}
    signing_input = f"{header_b64}.{payload_b64}"
    expected = hmac.new(_SECRET.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    if not hmac.compare_digest(expected, _unb64url(sig_b64)):
        return {"ok": False, "reason": "invalid_signature"}
    try:
        payload = json.loads(_unb64url(payload_b64))
    except Exception:
        return {"ok": False, "reason": "invalid_payload"}
    now = int(time.time())
    if payload.get("exp") and now >= int(payload["exp"]):
        return {"ok": False, "reason": "token_expired"}
    return {"ok": True, "sub": payload.get("sub"), "roles": payload.get("roles", []), "scopes": payload.get("scopes", [])}
