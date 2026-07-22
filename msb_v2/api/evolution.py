from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pathlib import Path
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token
from msb_v2.evolution.memory import EvolutionMemory
from msb_v2.evolution.proposal import EvolutionProposal
from msb_v2.evolution.scanner import OuroborosScanner
from msb_v2.evolution.simulator import EvolutionSimulator
import json as _json
import re as _re

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter(tags=["evolution"])
_REPO_ROOT = Path("/Users/lordwilson/msb-v2")
_scanner = OuroborosScanner(root=_REPO_ROOT)
_simulator = EvolutionSimulator(repo_root=_REPO_ROOT)
_memory = EvolutionMemory(path=_REPO_ROOT / "evolution_memory.db")


class EvolutionProposalRequest(BaseModel):
    proposal_id: str
    title: str
    affected_modules: List[str]
    rationale: str
    risk: str = "medium"


class SimulationRequest(BaseModel):
    proposal_id: str
    pytest_targets: List[str] = []
    dry_run: bool = False


class MemoryArtifact(BaseModel):
    event: str
    component: str
    technique: str
    complexity_before: int
    complexity_after: int
    vdr_improvement: bool
    golden_tests_passed: bool


@router.post("/scan")
def evolution_scan(auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    return JSONResponse(_scanner.scan())


@router.post("/propose")
def evolution_propose(payload: EvolutionProposalRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    proposal = _scanner.propose(
        proposal_id=payload.proposal_id,
        title=payload.title,
        affected_modules=payload.affected_modules,
        rationale=payload.rationale,
        risk=payload.risk,
        memory=_memory,
    )
    _memory.record(proposal, target=payload.affected_modules[0] if payload.affected_modules else "")
    return JSONResponse({
        "proposal_id": proposal.proposal_id,
        "status": proposal.status,
        "risk": proposal.risk,
        "failure_reason": proposal.failure_reason,
    })


@router.post("/simulate")
def evolution_simulate(payload: SimulationRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    proposal = _memory.get(payload.proposal_id) or EvolutionProposal(
        proposal_id=payload.proposal_id,
        title=payload.proposal_id,
        affected_modules=payload.pytest_targets,
        rationale="",
    )
    object.__setattr__(proposal, "dry_run", payload.dry_run)
    result = _simulator.simulate(proposal, payload.pytest_targets)
    proposal.status = "simulated" if result.passed else "failed"
    proposal.simulation = {"passed": result.passed, "failure_reason": result.failure_reason}
    _memory.record(proposal)
    return JSONResponse({
        "proposal_id": result.proposal_id,
        "passed": result.passed,
        "regression_tests": result.regression_tests,
        "capability_parity": result.capability_parity,
        "failure_reason": result.failure_reason,
    })


@router.get("/proposals")
def evolution_proposals(auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    return JSONResponse({"proposals": _memory.all()})


@router.get("/proposal/{proposal_id}")
def evolution_proposal(proposal_id: str, auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    proposal = _memory.get(proposal_id)
    if not proposal:
        return JSONResponse({"detail": "not found"}, status_code=404)
    history = _memory.history(proposal_id)
    return JSONResponse({"proposal": proposal, "history": history})


@router.post("/memory/record")
async def record_evolution(artifact: MemoryArtifact):
    proposal = EvolutionProposal(
        proposal_id=f"{artifact.component}:{artifact.technique}:{artifact.complexity_before}->{artifact.complexity_after}",
        title=artifact.event,
        affected_modules=[artifact.component],
        rationale=artifact.technique,
        risk="low" if artifact.vdr_improvement else "medium",
        status="success" if artifact.vdr_improvement else "failure",
        approval_status="accepted" if artifact.golden_tests_passed else "rejected",
    )
    object.__setattr__(proposal, "description", artifact.technique)
    object.__setattr__(proposal, "outcome", "success" if artifact.vdr_improvement else "failure")
    _memory.record(
        proposal,
        target=artifact.component,
        fingerprint=f"{artifact.complexity_before}->{artifact.complexity_after}",
    )
    return {"status": "RECORDED", "component": artifact.component}


@router.get("/memory/latest")
async def latest_memories():
    db_path = getattr(_memory, "path", None)
    if not db_path:
        return {"memories": []}
    import os
    if not os.path.exists(db_path):
        return {"memories": []}
    import sqlite3
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT * FROM proposals ORDER BY created_at DESC LIMIT 5").fetchall()
    if not rows:
        return {"memories": []}
    keys = [
        "proposal_id",
        "title",
        "affected_modules",
        "rationale",
        "risk",
        "status",
        "created_at",
        "simulation",
        "approval_status",
        "failure_reason",
        "rollback_ref",
        "fingerprint",
        "target",
    ]
    memories = []
    for row in rows:
        data = dict(zip(keys, row))
        for field in ("affected_modules", "simulation"):
            if data.get(field):
                try:
                    data[field] = _json.loads(data[field])
                except Exception:
                    pass
        memories.append(data)
    return {"memories": memories}


class EvolveRequest(BaseModel):
    mode: str = "autonomous"
    max_refactors: int = 1


@router.post("/evolve")
def evolution_evolve(payload: EvolveRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    latest = _memory.all()[-1] if hasattr(_memory, "all") and _memory.all() else {}
    scan = _scanner.scan()
    hotspots = scan.get("hotspots", []) if isinstance(scan, dict) else []
    applied = []
    audited = 0
    persists = 0
    for hotspot in hotspots[: max(1, payload.max_refactors)]:
        target = hotspot.get("file") or hotspot.get("path") or ""
        function = hotspot.get("function") or hotspot.get("name") or ""
        proposal_id = f"evolv:{_json.loads(_json.dumps(hotspot, default=str)).__hash__()}"
        if not target:
            continue
        proposal = EvolutionProposal(
            proposal_id=proposal_id,
            title=f"Auto refactor: {function} in {target}",
            affected_modules=[target],
            rationale="Evolver: apply prior successful technique via declarative inversion when conditional density is high.",
            risk="low",
            status="proposed",
            approval_status="pending",
        )
        _memory.record(proposal, target=target)
        audited += 1
        persisted = _json.dumps({
            "module": target,
            "function": function,
            "complexity": hotspot.get("complexity"),
            "technique": "declarative_inversion",
        }, default=str)
        result = {
            "proposal_id": proposal_id,
            "target": target,
            "function": function,
            "technique": "declarative_inversion",
            "decision": "eligible" if hotspot.get("complexity", 0) >= 10 else "deferred",
            "vdr_expected": True,
            "details": persisted,
        }
        applied.append(result)
        persists += 1
        if payload.mode != "autonomous":
            continue
        if payload.max_refactors <= 1:
            break
    return JSONResponse({
        "mode": payload.mode,
        "applied_count": len(applied),
        "audit_result": {"pending_audit": audited, "persisted": persists},
        "training_examples": applied[:3],
        "next_steps": [
            "simulate each proposal before apply",
            "run golden tests before committing",
            "rollback if capability_parity is not 1.0"
        ],
        "memory_summary": {
            "latest_target": latest.get("target"),
            "latest_fingerprint": latest.get("fingerprint"),
            "latest_status": latest.get("status"),
        },
    })


# HCL contract registration
_register_contract(HarnessContract(route="/evolve", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/scan", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/propose", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/simulate", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/proposals", method="get", allow_anonymous=False))
_register_contract(HarnessContract(route="/proposal/{proposal_id}", method="get", allow_anonymous=False))
_register_contract(HarnessContract(route="/memory/record", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/memory/latest", method="get", allow_anonymous=False))
