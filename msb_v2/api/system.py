from __future__ import annotations

import os
from typing import Any, Dict

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from validation.workflow_tests import run_workflow_tests
from runtime.state_machine import RuntimeStateMachine, READY, THINKING, EXECUTING, VERIFYING, COMPLETED, FAILED

router = APIRouter(tags=["system"])
state_machine = RuntimeStateMachine()


class ValidateRequest(BaseModel):
    base_url: str = "http://127.0.0.1:8766"


class RunSandboxRequest(BaseModel):
    task_id: str
    agent: str | None = None


@router.get("/system/health/full")
def system_health_full() -> Dict[str, Any]:
    base = os.getenv("MSB_BASE_URL", "http://127.0.0.1:8766")
    return {
        "base_url": base,
        "validator": run_workflow_tests(base),
    }


@router.post("/system/validate", dependencies=[Depends(require_bearer_token)])
def system_validate(body: ValidateRequest) -> Dict[str, Any]:
    return run_workflow_tests(body.base_url)


@router.get("/system/integrity")
def system_integrity() -> Dict[str, Any]:
    base = os.getenv("MSB_BASE_URL", "http://127.0.0.1:8766")
    validator = run_workflow_tests(base)
    score = validator.get("score", 0.0)
    return {
        "score": score,
        "grade": "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "F",
        "passed": len(validator.get("passed", [])),
        "failed": len(validator.get("failed", [])),
        "details": validator,
    }


@router.post("/sandbox/run", dependencies=[Depends(require_bearer_token)])
def sandbox_run(body: RunSandboxRequest) -> Dict[str, Any]:
    task = state_machine.create_task(body.task_id, agent=body.agent)
    try:
        task.transition(THINKING)
        task.transition(EXECUTING)
        task.transition(VERIFYING)
        task.transition(COMPLETED, outcome="ok")
    except Exception as exc:
        task.transition(FAILED, error=str(exc))
    return task.to_dict()
