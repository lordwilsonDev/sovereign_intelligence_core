from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from msb_v2.runtime.contracts import RuntimeContract, registry as _registry

logger = logging.getLogger(__name__)


def _safe_register_capability(
    name: str,
    version: str = "0.0.0",
    *,
    metadata: Optional[Dict[str, Any]] = None,
    validate: Optional[Any] = None,
) -> RuntimeContract:
    contract = RuntimeContract(name=name, version=version, metadata=metadata or {}, validate=validate)
    _registry().register(contract)
    return contract


def register_runtime_capabilities() -> List[RuntimeContract]:
    results = []
    try:
        results.append(_safe_register_capability("lifecycle", "0.1.0"))
    except Exception as exc:
        logger.debug("lifecycle registration failed: %s", exc)

    try:
        results.append(_safe_register_capability("events", "0.1.0"))
    except Exception as exc:
        logger.debug("events registration failed: %s", exc)

    try:
        _kb4_validate = lambda: True
        _safe_register_capability("kb4", "0.1.0", validate=_kb4_validate)
        results.append(RuntimeContract(name="kb4", version="0.1.0", validate=_kb4_validate))
    except Exception as exc:
        logger.debug("kb4 registration skipped: %s", exc)

    try:
        _safe_register_capability("moie", "0.1.0")
        results.append(RuntimeContract(name="moie", version="0.1.0"))
    except Exception as exc:
        logger.debug("moie registration skipped: %s", exc)

    try:
        _safe_register_capability("ouroboros", "0.1.0")
        results.append(RuntimeContract(name="ouroboros", version="0.1.0"))
    except Exception as exc:
        logger.debug("ouroboros registration skipped: %s", exc)

    try:
        _safe_register_capability("merkle", "0.1.0")
        results.append(RuntimeContract(name="merkle", version="0.1.0"))
    except Exception as exc:
        logger.debug("merkle registration skipped: %s", exc)

    try:
        _safe_register_capability("resources", "0.1.0")
        results.append(RuntimeContract(name="resources", version="0.1.0"))
    except Exception as exc:
        logger.debug("resources registration skipped: %s", exc)

    try:
        _safe_register_capability("circuit_breaker", "0.1.0")
        results.append(RuntimeContract(name="circuit_breaker", version="0.1.0"))
    except Exception as exc:
        logger.debug("circuit_breaker registration skipped: %s", exc)

    return results
