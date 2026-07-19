from __future__ import annotations

import os
from typing import Any, Dict, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.jwt import verify_token

security = HTTPBearer(auto_error=False)


def _is_bypass() -> bool:
    raw = os.getenv("MSB_AUTH_LOCAL_BYPASS", os.getenv("MSB_AUTH_ALLOW_ANY", "0"))
    return str(raw).lower() in {"1", "true", "yes"}


async def require_bearer_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    if _is_bypass():
        return {"sub": "local", "roles": ["system"], "scopes": ["*"]}
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    result = verify_token(credentials.credentials)
    if not result.get("ok"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=result.get("reason", "invalid_token"))
    return result
