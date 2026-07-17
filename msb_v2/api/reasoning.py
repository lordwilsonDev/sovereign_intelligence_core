from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field

from msb_v2.reasoning.store import ReasoningStore, SEED
from msb_v2.reasoning.types import (
    ReasoningStatus,
    ReasoningStep,
    ReasoningTrace,
)

router = APIRouter(tags=["reasoning"])
store = ReasoningStore(SEED)


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


def _trace_out(trace: ReasoningTrace) -> TraceOut:
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
    )


@router.get("/traces", response_model=list[TraceOut])
def list_traces(status: ReasoningStatus | None = None) -> list[TraceOut]:
    return [_trace_out(t) for t in store.list_traces(status)]


@router.get("/traces/{trace_id}", response_model=TraceOut)
def get_trace(trace_id: str) -> TraceOut:
    try:
        return _trace_out(store.get_trace(trace_id))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/traces", response_model=TraceOut)
def create_trace(body: TraceCreate) -> TraceOut:
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
        return _trace_out(store.add_trace(trace))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.patch("/traces/{trace_id}/status", response_model=TraceOut)
def patch_status(trace_id: str, body: SetStatusBody) -> TraceOut:
    try:
        return _trace_out(store.set_status(trace_id, body.status))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/traces/{trace_id}/decision", response_model=TraceOut)
def backfill_decision(trace_id: str, decision_id: str = Body(...)) -> TraceOut:
    try:
        return _trace_out(store.backfill_decision(trace_id, decision_id))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/refs/{ref_id}")
def refs_for(ref_id: str) -> list[dict[str, object]]:
    return [r.__dict__ for r in store.refs_for(ref_id)]
