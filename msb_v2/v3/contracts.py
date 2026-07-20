"""
Harness Contract Language (HCL) — register-time contract registry for MSB routes.

This module is the single place to register and inspect contracts. It sets no
policy by itself; runtime enforcement is wired into `msb_v2.api.middleware`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class HarnessContract:
    route: str
    method: str
    body_type: Any = field(default_factory=lambda: dict)
    allow_anonymous: bool = True
    timeout_ms: int = 5000
    max_body_bytes: int = 512_000

    def validate(self, payload: Dict[str, Any]) -> Optional[str]:
        if self.body_type is dict or self.body_type is None:
            return None
        try:
            if hasattr(self.body_type, "model_validate"):
                self.body_type.model_validate(payload)
            elif hasattr(self.body_type, "parse_obj"):
                self.body_type.parse_obj(payload)
        except Exception as exc:
            return str(exc)
        return None


_CONTRACTS: Dict[tuple[str, str], HarnessContract] = {}
_CONTRACT_LIST: List[HarnessContract] = []


def register(contract: HarnessContract) -> None:
    normalized_route = contract.route.rstrip("/") or "/"
    _CONTRACTS[(normalized_route, contract.method.lower())] = contract
    if contract not in _CONTRACT_LIST:
        _CONTRACT_LIST.append(contract)


def lookup(route: str, method: str) -> Optional[HarnessContract]:
    normalized_route = route.rstrip("/") or "/"
    contract = _CONTRACTS.get((normalized_route, method.lower()))
    if contract is not None:
        return contract
    normalized_route = route.rstrip("/") or "/"
    return _CONTRACTS.get((normalized_route, "any"))


def all_contracts() -> List[HarnessContract]:
    return list(_CONTRACT_LIST)
