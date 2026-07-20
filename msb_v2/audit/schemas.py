from __future__ import annotations

import hashlib
from typing import Any


def _hash(value: Any) -> str:
    try:
        raw = str(value).encode("utf-8")
    except Exception:
        raw = repr(value).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()


def build_input_hash(workflow: str, payload: dict[str, Any] | None) -> str:
    return _hash(f"{workflow}:{payload or {}}")


def build_output_hash(output: Any) -> str:
    return _hash(output)


def stable_workflow(name: str | None) -> str:
    return (name or "unspecified").strip().lower().replace(" ", "-")
