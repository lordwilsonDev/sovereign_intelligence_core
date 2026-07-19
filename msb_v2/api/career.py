from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from cognitive_compiler.career_harness_v1 import CareerHarness

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter()


class EvaluateRequest(BaseModel):
    company: str
    role: str
    jd_text: str
    score: float | None = None
    career_project_root: str | None = None


@router.get("/career/health")
def career_health(career_project_root: str | None = None):
    h = CareerHarness(project_root=career_project_root)
    plan = h.plan("health")
    return {"ok": h.ready, "event": "health", "missing": plan.get("missing", [])}


@router.post("/career/evaluate")
def career_evaluate(body: EvaluateRequest):
    h = CareerHarness(project_root=body.career_project_root)
    result = h.evaluate_jd_text(body.company, body.role, body.jd_text, body.score)
    out = dict(result.payload or {"error": result.error or "evaluation failed"})
    out["event"] = result.event
    out["ok"] = result.ok
    return out
# HCL contract registration
_register_contract(HarnessContract(route="/career/evaluate", method="post", allow_anonymous=False))
