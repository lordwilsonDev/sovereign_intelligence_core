from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.aura.validator import ValidatorCascade

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter(tags=["aura"])
_cascade = ValidatorCascade()


@router.post("/validate")
def aura_validate(payload: dict[str, Any]) -> JSONResponse:
    task = payload.get("task")
    context = payload.get("context", {})
    if task is None:
        return JSONResponse({"ok": False, "errors": ["task is required"]}, status_code=422)
    cascade_result = _cascade.validate(str(task), context)
    return JSONResponse({"ok": cascade_result.get("valid", False), "results": cascade_result.get("results", [])})
# HCL contract registration
_register_contract(HarnessContract(route="/aura/validate", method="post", allow_anonymous=False))
