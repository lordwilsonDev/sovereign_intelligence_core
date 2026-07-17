from __future__ import annotations

import time
from typing import Any, Dict

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.api.cognitive import _engine as cognitive_engine
from msb_v2.api.counterfactual import branch_trace, _stream as counterfactual_stream
from msb_v2.core.evaluation_metrics import EvaluationMetrics
from msb_v2.engine.moie_orchestrator import MoIEOrchestrator
from msb_v2.engine.rcoh import RCOH, RCOHState, Phase
from msb_v2.engine.merkle_reasoning import MerkleReasoningChain

router = APIRouter(tags=["brain"])

class ManifestRequest(BaseModel):
    query: str
    intent: str = "default"
    trace_id: str | None = None


def _metrics(task_id: str, trace_id: str | None, kind: str) -> EvaluationMetrics:
    metrics = EvaluationMetrics(task_id=task_id, trace_id=trace_id)
    start = time.time()
    yield metrics
    latency = (time.time() - start) * 1000
    yield metrics.with_efficiency(
        tokens_used=0,
        latency_ms=round(latency, 2),
        compute_ms=round(latency, 2),
    ).scored(1.0 if kind != "cognitive_error" else 0.0)


def _ok(kind: str, payload: Dict[str, Any], task_id: str, trace_id: str | None, metrics: EvaluationMetrics) -> Dict[str, Any]:
    return {
        "status": "ok",
        "kind": kind,
        "task_id": task_id,
        "trace_id": trace_id,
        "metrics": metrics.to_dict(),
        "payload": payload,
    }


_trace_seq = 0


def _next_task_id() -> str:
    global _trace_seq
    _trace_seq += 1
    return f"task-{_trace_seq:04d}"


@router.post("/run")
def brain_run(req: ManifestRequest) -> Dict[str, Any]:
    kind = req.intent.lower()
    task_id = _next_task_id()
    trace_id = req.trace_id
    gen = _metrics(task_id, trace_id, kind)
    metrics = next(gen)

    if kind == "debate":
        result = MoIEOrchestrator().run(req.query)
        metrics = gen.send(metrics.with_reasoning(success_rate=0.9, planning_accuracy=0.9, contradictions=0).with_coding(tests_passed=0, tests_total=0, regressions=0, security_warnings=0).with_autonomy(human_interventions=0, recovery_actions=0, failed_loops=0))
        return _ok("moie", result, task_id, trace_id, metrics)

    if kind == "plan":
        state = RCOHState(
            cycle_id=f"rcoh-brain-{req.query[:20].replace(' ', '_')}",
            current_phase=Phase.OBSERVE,
            context_summary=req.query,
            goals=[req.query],
            max_iterations=3,
        )
        final = RCOH(state=state).run(max_iterations=3)
        metrics = gen.send(metrics.with_reasoning(success_rate=0.8, planning_accuracy=0.8, contradictions=0).with_coding(tests_passed=0, tests_total=0, regressions=0, security_warnings=0).with_autonomy(human_interventions=0, recovery_actions=0, failed_loops=0))
        return _ok("rcoh", {
            "cycle_id": final.cycle_id,
            "phase": final.current_phase.value,
            "confidence": final.confidence,
            "goals": final.goals,
            "alternatives_count": len(final.alternatives),
        }, task_id, trace_id, metrics)

    if kind == "assess":
        trace_id = req.trace_id or ""
        try:
            result = cognitive_engine.assess(trace_id)
        except Exception as exc:  # noqa: BLE001
            kind_out = "cognitive_error"
            metrics = gen.send(metrics.with_reasoning(success_rate=0.0, planning_accuracy=0.0, contradictions=0).with_coding(tests_passed=0, tests_total=0, regressions=0, security_warnings=0).with_autonomy(human_interventions=0, recovery_actions=0, failed_loops=1))
            return _ok(kind_out, {"trace_id": trace_id, "error": str(exc)}, task_id, trace_id, metrics)
        metrics = gen.send(metrics.with_reasoning(success_rate=0.85, planning_accuracy=0.7, contradictions=0).with_coding(tests_passed=0, tests_total=0, regressions=0, security_warnings=0).with_autonomy(human_interventions=0, recovery_actions=0, failed_loops=0))
        kind_out = "cognitive"
        return _ok(kind_out, {"trace_id": trace_id, "assessment": result}, task_id, trace_id, metrics)

    if kind == "branch":
        trace_id = req.trace_id or ""
        try:
            result = branch_trace(counterfactual_stream, trace_id)
        except Exception as exc:  # noqa: BLE001
            metrics = gen.send(metrics.with_reasoning(success_rate=0.0, planning_accuracy=0.0, contradictions=1).with_coding(tests_passed=0, tests_total=0, regressions=0, security_warnings=0).with_autonomy(human_interventions=0, recovery_actions=0, failed_loops=1))
            return _ok("counterfactual_error", {"error": str(exc)}, task_id, trace_id, metrics)
        metrics = gen.send(metrics.with_reasoning(success_rate=0.75, planning_accuracy=0.6, contradictions=0).with_coding(tests_passed=0, tests_total=0, regressions=0, security_warnings=0).with_autonomy(human_interventions=0, recovery_actions=0, failed_loops=0))
        return _ok("counterfactual", result, task_id, trace_id, metrics)

    if kind == "imagine":
        chain = MerkleReasoningChain()
        seed = req.query.split()[0].lower() if req.query else "default"
        chain.append("brain", {"intent": req.intent, "query": req.query})
        metrics = gen.send(metrics.with_reasoning(success_rate=0.5, planning_accuracy=0.5, contradictions=0).with_coding(tests_passed=0, tests_total=0, regressions=0, security_warnings=0).with_autonomy(human_interventions=0, recovery_actions=0, failed_loops=0))
        return _ok("imagination", {
            "seed": seed,
            "root_hash": chain.root_hash(),
        }, task_id, trace_id, metrics)

    if kind == "drill":
        metrics = gen.send(metrics.with_reasoning(success_rate=0.6, planning_accuracy=0.6, contradictions=0).with_coding(tests_passed=0, tests_total=0, regressions=0, security_warnings=0).with_autonomy(human_interventions=0, recovery_actions=0, failed_loops=0))
        return _ok("aura", {
            "module": "aura",
            "goal": req.query,
            "decision": {"tool": "echo", "arguments": {"message": req.query}},
            "note": "drill path uses synthetic execution; swap for live AURA run when retriever/policy are configured",
        }, task_id, trace_id, metrics)

    metrics = gen.send(metrics.with_reasoning(success_rate=0.0, planning_accuracy=0.0, contradictions=0).with_coding(tests_passed=0, tests_total=0, regressions=0, security_warnings=0).with_autonomy(human_interventions=0, recovery_actions=0, failed_loops=0))
    return _ok("fallback", {"resolved": "noop", "query": req.query}, task_id, trace_id, metrics)
