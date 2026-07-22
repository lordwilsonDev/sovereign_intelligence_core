from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends

from msb_v2.echo.harness import EchoHarness

router = APIRouter()
_harness = EchoHarness()


@router.post("/evaluate")
def evaluate(payload: Dict[str, Any]) -> Dict[str, Any]:
    return _harness.evaluate(payload)


@router.get("/history")
def history(limit: int = 50) -> Dict[str, Any]:
    return {"items": _harness.history(limit=limit)}


@router.get("/status")
def status() -> Dict[str, Any]:
    return _harness.status()
