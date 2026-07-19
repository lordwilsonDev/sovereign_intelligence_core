from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from msb_v2.transport.tls import resolve_tls_paths

router = APIRouter(tags=["transport"])


@router.get("/health/tls")
def health_tls() -> Dict[str, Any]:
    pair = resolve_tls_paths(
        __import__("os").getenv("MSB_TLS_CERT"),
        __import__("os").getenv("MSB_TLS_KEY"),
    )
    return {
        "tls_enabled": pair is not None,
        "cert_path": pair[0] if pair else None,
        "key_path": pair[1] if pair else None,
    }
