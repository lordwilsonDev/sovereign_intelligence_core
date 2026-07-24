from __future__ import annotations

import contextlib
import contextvars
import logging
from typing import Any, Callable, Dict, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.jwt import verify_token
from msb_v2.v3.contracts import lookup as _hcl_lookup

security = HTTPBearer(auto_error=False)

# contextvar so TestClient runs never leak auth state across tests
_unset = object()
_bypass_override: contextvars.ContextVar = contextvars.ContextVar("_bypass_override", default=_unset)
_had_explicit_override: contextvars.ContextVar = contextvars.ContextVar("_had_explicit_override", default=False)

def set_local_bypass(enabled: Optional[bool]) -> None:
    if enabled is None:
        _bypass_override.set(_unset)
    else:
        _bypass_override.set(enabled)
    _had_explicit_override.set(True)


@contextlib.contextmanager
def _bypass_context(enabled: bool):
    token = _bypass_override.set(enabled)
    prev = _had_explicit_override.set(True)
    try:
        yield
    finally:
        _bypass_override.reset(token)
        _had_explicit_override.reset(prev)


async def require_bearer_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Dict[str, Any]:
    explicit = _bypass_override.get(_unset)
    if explicit is True:
        return {"sub": "local", "roles": ["system"], "scopes": ["*"]}
    if explicit is False:
        pass
    elif not _had_explicit_override.get(False):
        if str(__import__("os").getenv("MSB_AUTH_LOCAL_BYPASS", "")).lower() in {"1", "true", "yes"}:
            return {"sub": "local", "roles": ["system"], "scopes": ["*"]}
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    result = verify_token(credentials.credentials)
    if not result.get("ok"):
        detail = result.get("reason", "invalid_token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
    return result


_logger = logging.getLogger("msb_v2.v3.hcl")


async def hcl_contract_middleware(request: Request, call_next: Callable[..., Any]) -> Any:
    strict = __import__("os").getenv("MSB_REQUIRE_HCL", "").lower() in {"2", "strict"}
    enforce = strict or __import__("os").getenv("MSB_REQUIRE_HCL", "").lower() in {"1", "true", "yes"}
    if not enforce:
        return await call_next(request)
    path = request.url.path
    method = request.method.lower()
    contract = _hcl_lookup(path, method)
    if contract is None:
        if strict:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"error": "uncontracted_route", "path": path, "method": method})
        _logger.warning({"event": "hcl_skip", "path": path, "method": method})
        return await call_next(request)
    if not contract.allow_anonymous:
        auth_header = request.headers.get("authorization", "")
        if not auth_header.lower().startswith("bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing_bearer")
    content_type = request.headers.get("content-type", "")
    if request.method in {"POST", "PUT", "PATCH"} and "application/json" in content_type:
        content_length_raw = request.headers.get("content-length")
        max_bytes = int(contract.max_body_bytes)
        if content_length_raw is not None:
            try:
                if int(content_length_raw) > max_bytes:
                    raise HTTPException(status_code=413, detail="payload_too_large")
            except ValueError:
                pass
        body_bytes = await request.body()
        if body_bytes:
            try:
                payload = __import__("json").loads(body_bytes)
            except Exception:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid_json_payload")
            if len(body_bytes) > max_bytes:
                raise HTTPException(status_code=413, detail="payload_too_large")
    return await call_next(request)
