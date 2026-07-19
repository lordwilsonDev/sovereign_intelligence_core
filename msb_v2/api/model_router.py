from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends
from models.registry import default_registry
from models.router import ModelRouter

from msb_v2.api.middleware import require_bearer_token

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter(tags=["models"])
model_router = ModelRouter()


@router.get("/model/status")
def model_status() -> Dict[str, Any]:
    return {
        "models": [
            {
                "name": name,
                "provider": model.provider,
                "enabled": model.enabled,
                "fallback": model.fallback,
                "max_tokens": model.max_tokens,
                "cost_per_1k": model.capabilities.cost_per_1k_tokens,
                "capabilities": model.capabilities.__dict__,
            }
            for name, model in default_registry.models.items()
        ],
        "available_count": len(default_registry.available("reasoning")),
    }


@router.post("/model/route")
def model_route(body: Dict[str, Any], auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    task = str(body.get("task", ""))
    context = body or {}
    result = model_router.route(task, context)
    return {
        "task": task,
        "context": context,
        "result": result,
        "ts": "2026-07-19",
    }
# HCL contract registration
_register_contract(HarnessContract(route="/model/route", method="post", allow_anonymous=False))
