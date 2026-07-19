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


@router.post("/evolution/scan")
def evolution_scan(auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    return JSONResponse(_scanner.scan())


@router.post("/evolution/propose")
def evolution_propose(payload: EvolutionProposalRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    proposal = EvolutionProposal(
        proposal_id=payload.proposal_id,
        title=payload.title,
        affected_modules=payload.affected_modules,
        rationale=payload.rationale,
        risk=payload.risk,
    )
    _memory.record(proposal)
    return JSONResponse({
        "proposal_id": proposal.proposal_id,
        "status": proposal.status,
        "risk": proposal.risk,
    })


@router.post("/evolution/simulate")
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


@router.get("/evolution/proposals")
def evolution_proposals(auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    return JSONResponse({"proposals": _memory.all()})


@router.get("/evolution/proposal/{proposal_id}")
def evolution_proposal(proposal_id: str, auth: Dict[str, Any] = Depends(require_bearer_token)) -> JSONResponse:
    proposal = _memory.get(proposal_id)
    if not proposal:
        return JSONResponse({"detail": "not found"}, status_code=404)
    history = _memory.history(proposal_id)
    return JSONResponse({"proposal": proposal, "history": history})
# HCL contract registration
_register_contract(HarnessContract(route="/evolution/scan", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/evolution/propose", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/evolution/simulate", method="post", allow_anonymous=False))
