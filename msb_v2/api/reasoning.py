from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel, Field

from msb_v2.api.middleware import require_bearer_token

from msb_v2.reasoning.store import ReasoningStore, SEED
from msb_v2.reasoning.types import (
    ReasoningStatus,
    ReasoningStep,
    ReasoningTrace,
)
from msb_v2.verification.capability_registry import CapabilityRegistry
from msb_v2.verification.evidence import EvidenceEngine

router = APIRouter(tags=["reasoning"])
store = ReasoningStore(SEED)
_registry = CapabilityRegistry()
_evidence_engine = EvidenceEngine(registry=_registry, memory_client=None)


def seed_store(traces: list[ReasoningTrace]) -> None:
    for t in traces:
        store.add_trace(t)


class StepModel(BaseModel):
    step_index: int
    claim: str
    evidence_refs: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    metadata: dict[str, object] = Field(default_factory=dict)


class TraceCreate(BaseModel):
    trace_id: str | None = None
    title: str
    status: ReasoningStatus
    steps: list[StepModel]
    decision_id: str | None = None
    memory_ids: list[str] = Field(default_factory=list)
    conclusion: str = ""
    metadata: dict[str, object] = Field(default_factory=dict)


class SetStatusBody(BaseModel):
    status: ReasoningStatus


class TraceOut(BaseModel):
    trace_id: str
    title: str
    status: ReasoningStatus
    steps: list[StepModel]
    decision_id: str | None
    memory_ids: list[str]
    conclusion: str
    created_at: str
    updated_at: str
    metadata: dict[str, object]
    evidence_report: dict[str, object] | None = None


def _trace_out(trace: ReasoningTrace, evidence_report: dict[str, object] | None = None) -> TraceOut:
    return TraceOut(
        trace_id=trace.trace_id,
        title=trace.title,
        status=trace.status,
        steps=[
            StepModel(
                step_index=s.step_index,
                claim=s.claim,
                evidence_refs=list(s.evidence_refs),
                assumptions=list(s.assumptions),
                confidence=s.confidence,
                metadata=s.metadata,
            )
            for s in trace.steps
        ],
        decision_id=trace.decision_id,
        memory_ids=list(trace.memory_ids),
        conclusion=trace.conclusion,
        created_at=trace.created_at,
        updated_at=trace.updated_at,
        metadata=trace.metadata,
        evidence_report=evidence_report,
    )


def _build_evidence_report(trace: ReasoningTrace) -> dict[str, object] | None:
    try:
        report = _evidence_engine.evaluate(
            query=trace.title,
            answer=trace.conclusion or " ".join(s.claim for s in trace.steps),
            trace={
                "confidence": float(trace.steps[-1].confidence) if trace.steps else 0.0,
                "steps": [s.claim for s in trace.steps],
                "tool_calls": trace.metadata.get("tool_calls", []),
                "provenance": trace.metadata.get("provenance", []),
            },
        )
        return {
            "hash": report.compute_hash(),
            "confidence": report.confidence,
            "consistency": report.consistency,
            "novelty": report.novelty,
            "verification_score": report.verification_score,
            "falsification_score": report.falsification_score,
            "uncertainty": report.uncertainty,
            "trace_depth": report.trace_depth,
            "memory_support": report.memory_support,
            "tool_support": report.tool_support,
            "provenance": report.provenance,
        }
    except Exception:
        return None


@router.get("/traces", response_model=list[TraceOut])
def list_traces(
    status: ReasoningStatus | None = None,
    offset: int = 0,
    limit: int = 20,
    q: str | None = None,
) -> list[TraceOut]:
    if q:
        traces = store.search_traces(q, limit=max(1, limit))
    else:
        traces = store.list_trace_page(offset=max(0, offset), limit=max(1, limit), status=status)
    return [_trace_out(t) for t in traces]


@router.get("/traces/{trace_id}", response_model=TraceOut)
def get_trace(trace_id: str) -> TraceOut:
    try:
        trace = store.get_trace(trace_id)
        return _trace_out(trace, _build_evidence_report(trace))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/traces", response_model=TraceOut)
def create_trace(body: TraceCreate, auth: Dict[str, Any] = Depends(require_bearer_token)) -> TraceOut:
    trace_id = body.trace_id or store.next_trace_id()
    trace = ReasoningTrace(
        trace_id=trace_id,
        title=body.title,
        status=body.status,
        steps=tuple(
            ReasoningStep(
                step_index=s.step_index,
                claim=s.claim,
                evidence_refs=tuple(s.evidence_refs),
                assumptions=tuple(s.assumptions),
                confidence=s.confidence,
                metadata=s.metadata,
            )
            for s in body.steps
        ),
        decision_id=body.decision_id or None,
        memory_ids=tuple(body.memory_ids),
        conclusion=body.conclusion,
        metadata=body.metadata,
    )
    try:
        saved = store.add_trace(trace)
        return _trace_out(saved, _build_evidence_report(saved))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.patch("/traces/{trace_id}/status", response_model=TraceOut)
def patch_status(trace_id: str, body: SetStatusBody, auth: Dict[str, Any] = Depends(require_bearer_token)) -> TraceOut:
    try:
        trace = store.set_status(trace_id, body.status)
        return _trace_out(trace, _build_evidence_report(trace))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/traces/{trace_id}/decision", response_model=TraceOut)
def backfill_decision(trace_id: str, decision_id: str = Body(...)) -> TraceOut:
    try:
        trace = store.backfill_decision(trace_id, decision_id)
        return _trace_out(trace, _build_evidence_report(trace))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/refs/{ref_id}")
def refs_for(ref_id: str) -> list[dict[str, object]]:
    return [r.__dict__ for r in store.refs_for(ref_id)]
