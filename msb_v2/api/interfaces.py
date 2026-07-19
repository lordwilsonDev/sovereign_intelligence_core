from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from interfaces.discovery import default_discovery
from interfaces.registry import InterfaceRegistry

router = APIRouter(tags=["interfaces"])
registry: InterfaceRegistry = default_discovery.registry


@router.get("/interfaces/registry")
def interfaces_registry() -> Dict[str, Any]:
    default_discovery.refresh()
    return registry.snapshot()


@router.post("/interfaces/refresh")
def interfaces_refresh() -> Dict[str, Any]:
    return default_discovery.refresh()
