from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from msb_v2.environment.sovereign_environment import SovereignEnvironment

router = APIRouter(tags=["environment"])

_environment = SovereignEnvironment()


@router.get("/sovereign/status")
def sovereign_status() -> JSONResponse:
    return JSONResponse(_environment.snapshot())


@router.get("/environment/status")
def environment_status() -> JSONResponse:
    return JSONResponse(_environment.snapshot())
