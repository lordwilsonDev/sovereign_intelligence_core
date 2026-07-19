from __future__ import annotations

from auth.jwt import issue_token


def bearer_token() -> str:
    return issue_token(
        "test-user",
        roles=["ops"],
        scopes=["system:read", "runtime:write", "recovery:read", "desktop:execute", "security:write"],
    )
