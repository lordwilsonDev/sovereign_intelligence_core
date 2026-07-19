from __future__ import annotations

import contextlib
import contextvars
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.jwt import verify_token

security = HTTPBearer(auto_error=False)


# contextvar so TestClient runs never leak auth state across tests
_bypass_override: contextvars.ContextVar[Optional[bool]] = contextvars.ContextVar("_bypass_override", default=None)


def set_local_bypass(enabled: Optional[bool]) -> None:
    _bypass_override.set(enabled)


@contextlib.contextmanager
def _bypass_context(enabled: bool):
    token = _bypass_override.set(enabled)
    try:
        yield
    finally:
        _bypass_override.reset(token)


async def require_bearer_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    explicit = _bypass_override.get(None)
    if explicit is True:
        return {"sub": "local", "roles": ["system"], "scopes": ["*"]}
    if explicit is False:
        # force enforcement path
        pass
    elif str(__import__("os").getenv("MSB_AUTH_LOCAL_BYPASS", "")).lower() in {"1", "true", "yes"}:
        return {"sub": "local", "roles": ["system"], "scopes": ["*"]}
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    result = verify_token(credentials.credentials)
    if not result.get("ok"):
        detail = result.get("reason", "invalid_token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
    return result
