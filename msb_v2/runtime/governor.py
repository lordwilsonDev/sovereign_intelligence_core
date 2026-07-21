from __future__ import annotations

import logging
from typing import List

from msb_v2.runtime.contracts import RuntimeContract, registry as _registry

logger = logging.getLogger(__name__)


def _safe_register_capability(name: str, version: str = "0.0.0") -> RuntimeContract:
    contract = RuntimeContract(name=name, version=version)
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
        from msb_v2.kernel.kb4 import KB4Kernel
        _safe_register_capability("kb4", "0.1.0")
        results.append(RuntimeContract(name="kb4", version="0.1.0"))
    except Exception as exc:
        logger.debug("kb4 registration skipped: %s", exc)

    try:
        from msb_v2.engine.moie_orchestrator import MoIEOrchestrator
        _safe_register_capability("moie", "0.1.0")
        results.append(RuntimeContract(name="moie", version="0.1.0"))
    except Exception as exc:
        logger.debug("moie registration skipped: %s", exc)

    try:
        from msb_v2.evolution.scanner import OuroborosScanner
        _safe_register_capability("ouroboros", "0.1.0")
        results.append(RuntimeContract(name="ouroboros", version="0.1.0"))
    except Exception as exc:
        logger.debug("ouroboros registration skipped: %s", exc)

    try:
        from msb_v2.audit.sovereign.merkle import AuditMerkleChain
        _safe_register_capability("merkle", "0.1.0")
        results.append(RuntimeContract(name="merkle", version="0.1.0"))
    except Exception as exc:
        logger.debug("merkle registration skipped: %s", exc)

    return results
