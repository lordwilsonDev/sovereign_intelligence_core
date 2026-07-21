from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Request
from pydantic import BaseModel

from msb_v2.governor.engine import GovernorEngine
from msb_v2.governor.orchestrator import WorkflowOrchestrator
from msb_v2.governor.policy_engine import PolicyEngine, PolicyRule

router = APIRouter()

_governor = GovernorEngine()
_policy_engine = PolicyEngine()
_orchestrator = WorkflowOrchestrator(_governor)
_governor._orchestrator = _orchestrator  # type: ignore[attr-defined]


class RegisterHarnessRequest(BaseModel):
    name: str
    url: str
    health_endpoint: str
    metadata: Dict[str, Any] | None = None


class WorkflowDefinitionRequest(BaseModel):
    name: str
    steps: list[Dict[str, Any]]


class WorkflowExecuteRequest(BaseModel):
    name: str


class PolicyRuleRequest(BaseModel):
    id: str
    name: str
    condition: str
    action: str
    enabled: bool = True


class PolicyEvaluateRequest(BaseModel):
    context: Dict[str, Any]


class PolicyRemoveRequest(BaseModel):
    policy_id: str


@router.get("/governor/status")
def governor_status() -> Dict[str, Any]:
    return {
        "status": "ok",
        "harness_count": len(_governor.harnesses()),
        "harnesses": _governor.health_snapshot(),
    }


@router.get("/governor/harnesses")
def list_harnesses() -> Dict[str, Any]:
    return {"harnesses": _governor.harnesses()}


@router.post("/governor/harnesses/register")
def register_harness(payload: RegisterHarnessRequest) -> Dict[str, Any]:
    return _governor.register_harness(payload.name, payload.url, payload.health_endpoint, payload.metadata)


@router.get("/governor/harnesses/{name}/health")
def harness_health(name: str) -> Dict[str, Any]:
    return _governor.check_harness(name)


@router.post("/governor/harnesses/{name}/enable")
def enable_harness(name: str) -> Dict[str, Any]:
    return _governor.enable_harness(name)


@router.post("/governor/harnesses/{name}/disable")
def disable_harness(name: str) -> Dict[str, Any]:
    return _governor.disable_harness(name)


@router.post("/governor/workflows/definitions")
def add_workflow_definition(payload: WorkflowDefinitionRequest) -> Dict[str, Any]:
    return _orchestrator.register_workflow(payload.model_dump())


@router.post("/governor/workflows/execute")
def execute_workflow(payload: WorkflowExecuteRequest) -> Dict[str, Any]:
    return _orchestrator.execute_workflow(payload.name)


@router.get("/governor/workflows/definitions")
def list_workflow_definitions() -> Dict[str, Any]:
    return {"workflows": list(_orchestrator.workflows().keys())}


@router.get("/governor/policies")
def list_policies() -> Dict[str, Any]:
    return {"policies": _policy_engine.rules()}


@router.post("/governor/policies/add")
def add_policy(payload: PolicyRuleRequest) -> Dict[str, Any]:
    return _policy_engine.add_rule(PolicyRule(id=payload.id, name=payload.name, condition=payload.condition, action=payload.action, enabled=payload.enabled))


@router.delete("/governor/policies/remove")
def remove_policy(payload: PolicyRemoveRequest) -> Dict[str, Any]:
    return _policy_engine.remove_rule(payload.policy_id)


@router.post("/governor/policies/evaluate")
def evaluate_policy(payload: PolicyEvaluateRequest) -> Dict[str, Any]:
    return _policy_engine.evaluate(payload.context)


@router.get("/governor/audit")
def governor_audit() -> Dict[str, Any]:
    return {"events": _governor.health_snapshot()[-10:]}
