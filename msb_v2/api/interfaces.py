from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends

from interfaces.discovery import default_discovery
from interfaces.registry import InterfaceRegistry

from msb_v2.api.middleware import require_bearer_token

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter(tags=["interfaces"])
registry: InterfaceRegistry = default_discovery.registry


@router.get("/interfaces/registry")
def interfaces_registry() -> Dict[str, Any]:
    default_discovery.refresh()
    return registry.snapshot()


@router.post("/interfaces/refresh", dependencies=[Depends(require_bearer_token)])
def interfaces_refresh() -> Dict[str, Any]:
    return default_discovery.refresh()
# HCL contract registration
_register_contract(HarnessContract(route="/interfaces/refresh", method="post", allow_anonymous=False))
