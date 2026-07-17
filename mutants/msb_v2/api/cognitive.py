from __future__ import annotations


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from msb_v2.engine.merkle_reasoning import MerkleReasoningChain
from msb_v2.engine.causal_memory import CausalMemory
from msb_v2.security.guardrails import Guardrails

router = APIRouter()


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class NegotiateRequest(BaseModel):
    peers: list[str]


class CheckpointRequest(BaseModel):
    label: str


class RedTeamResult(BaseModel):
    allowed: bool
    findings: list[str]
    reason: str | None
    redactions: int


def _memory_chain() -> MerkleReasoningChain:
    return MerkleReasoningChain()


def _memory_causal() -> CausalMemory:
    return CausalMemory()


@router.get("/ping")
def cognitive_ping() -> dict:
    return {"status": "ok", "module": "cognitive", "invariant": "T=0"}


@router.post("/mesh/negotiate")
def mesh_negotiate(payload: NegotiateRequest) -> dict:
    peers = payload.peers or []
    adjacency = {peer: [p for p in peers if p != peer] for peer in peers}
    return {"status": "ok", "peers": peers, "adjacency": adjacency, "mesh": len(peers) > 1}


@router.post("/chronos/checkpoint")
def chronos_checkpoint(payload: CheckpointRequest) -> dict:
    from datetime import datetime, timezone

    chain = _memory_chain()
    chain.append(payload.label, {"ts": datetime.now(timezone.utc).isoformat()})
    return {"status": "ok", "label": payload.label, "root": chain.root_hash()}


@router.post("/provenance/build")
def provenance_build() -> dict:
    chain = _memory_chain()
    causal = _memory_causal()
    chain.append("provenance", {"links": causal.links})
    return {"status": "ok", "root": chain.root_hash(), "links": causal.links}


@router.post("/redteam/run")
def redteam_run() -> dict:
    guardrails = Guardrails()
    sample = "contact@example.com and 123-45-6789"
    result = guardrails.inspect(sample, relevance=0.3)
    return {
        "status": "ok",
        "allowed": result.allowed,
        "findings": list(result.findings),
        "reason": result.reason,
        "redactions": sample.count("@") + sample.count("-"),
    }


@router.post("/semantic/snapshot")
def semantic_snapshot() -> dict:
    try:
        from msb_v2.aura.toolbelt import Toolbelt
        toolbelt = Toolbelt()
        return {
            "status": "ok",
            "available_tools": toolbelt.available(),
            "skill_count": len(getattr(toolbelt, "_skills", [])),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
