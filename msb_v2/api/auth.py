from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from msb_v2.api.policy import router as policy_router

# Auth/security route ownership moved to msb_v2.api.policy.
# This module remains importable to avoid breaking web.py's registry load.
router = policy_router


def requires_auth() -> Any:
    """Placeholder retained for compatibility."""
    from msb_v2.api.middleware import require_bearer_token
    return require_bearer_token


__all__ = ["router", "requires_auth"]
