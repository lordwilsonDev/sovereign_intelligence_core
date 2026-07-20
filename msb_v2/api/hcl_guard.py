"""Middleware HCL enforcement hardening + body-size guard."""
from __future__ import annotations

from typing import Callable, Optional

from fastapi import Request
from fastapi.responses import JSONResponse

from msb_v2.v3.contracts import lookup as _hcl_lookup


def _size_limit_for(contract) -> Optional[int]:
    if not contract:
        return None
    return getattr(contract, "max_body_bytes", None) or None


async def enforce_hcl(request: Request) -> Optional[JSONResponse]:
    path = request.url.path
    method = request.method.lower()
    contract = _hcl_lookup(path, method) or _hcl_lookup(path, "any")
    if contract is None:
        return None

    # anonymous gate
    if not getattr(contract, "allow_anonymous", True):
        try:
            from msb_v2.api.middleware import get_auth_context
            auth = get_auth_context(request)
        except Exception:
            auth = {}
        actor = (auth or {}).get("actor") or (auth or {}).get("sub") or "anonymous"
        if str(actor).lower() == "anonymous":
            return JSONResponse(
                status_code=401,
                content={"detail": "anonymous access rejected by HCL contract", "route": path},
            )

    # body-size guard
    limit = _size_limit_for(contract)
    if limit is not None:
        try:
            body = await request.body()
            if len(body) > limit:
                return JSONResponse(
                    status_code=413,
                    content={"detail": f"payload exceeds HCL body-size limit", "limit": limit, "len": len(body)},
                )
        except Exception:
            pass
    return None
