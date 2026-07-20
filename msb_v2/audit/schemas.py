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


_EMPTY_HASH = "0" * 40


def chain_hash(previous_hash: str, event: dict[str, Any]) -> str:
    bound = {
        "previous_hash": previous_hash or _EMPTY_HASH,
        "event_type": event.get("event_type"),
        "workflow": event.get("workflow"),
        "status": event.get("status"),
        "timestamp": event.get("timestamp"),
    }
    try:
        raw = repr(sorted(bound.items())).encode("utf-8")
    except Exception:
        raw = repr(bound).encode("utf-8")
    return hashlib.sha1(raw).hexdigest()


def apply_event_hashes(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Inject deterministic hash + chaining hash into each event copy."""
    hashed: list[dict[str, Any]] = []
    previous = _EMPTY_HASH
    for event in events:
        event_hash = _hash(event)
        next_chain = chain_hash(previous, event)
        enriched = dict(event)
        enriched["event_hash"] = event_hash
        enriched["chain_hash"] = next_chain
        hashed.append(enriched)
        previous = next_chain
    return hashed
