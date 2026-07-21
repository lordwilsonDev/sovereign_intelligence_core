from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.auto_healing import AutoHealingPolicyEngine
from msb_v2.audit.business_metrics import BusinessMetrics
from msb_v2.audit.events import EventType, Status
from msb_v2.audit.storage import AuditStore


router = APIRouter()


def _engine() -> AuditEngine:
    return AuditEngine(store=AuditStore())


@router.get("/recent")
def recent_audit_events(limit: int = 100, engine: AuditEngine = Depends(_engine)) -> list[dict[str, Any]]:
    return engine.events(limit=limit)


@router.get("/summary")
def audit_summary(limit: int = 100, engine: AuditEngine = Depends(_engine)) -> dict[str, Any]:
    engine.events(limit=limit)
    from msb_v2.audit.business_metrics import BusinessMetrics
    return BusinessMetrics(audit=engine).snapshot()


@router.get("/policies")
def audit_policies(engine: AuditEngine = Depends(_engine)) -> dict[str, Any]:
    actions = AutoHealingPolicyEngine(audit=engine).evaluate()
    return {"actions": actions, "count": len(actions)}


@router.get("/policies/falsification")
def audit_policies_falsification(engine: AuditEngine = Depends(_engine)) -> dict[str, Any]:
    events = engine.events()
    policy_events: list[dict[str, Any]] = []
    for event in events:
        event_type = event.get("event_type")
        if event_type not in {EventType.SELF_CORRECTION.value, EventType.SELF_CORRECTION_BLOCKED.value}:
            continue
        metadata = event.get("metadata") or {}
        policy = metadata.get("policy")
        if not policy:
            continue
        policy_events.append(
            {
                "policy": policy,
                "detected_rate": metadata.get("detected_rate"),
                "sample_count": metadata.get("sample_count"),
                "blocked": event_type == EventType.SELF_CORRECTION_BLOCKED.value,
                "suggestion": metadata.get("suggestion"),
                "quarantine": metadata.get("quarantine", {}),
                "action_feedback": "pending",
            }
        )
    return {"records": policy_events, "count": len(policy_events), "falsified_count": 0}


@router.get("/verify")
def audit_verify(store: AuditStore = Depends(_engine)) -> dict[str, Any]:
    from msb_v2.audit.sovereign.merkle import AuditMerkleChain
    from msb_v2.audit.sovereign.store import SovereignAuditStore
    sovereign = SovereignAuditStore()
    return {"verified": sovereign.merkle.verify_chain(), "log": str(sovereign.merkle.log_path)}


@router.get("/sovereignty")
def audit_sovereignty(
    engine: AuditEngine = Depends(_engine),
) -> dict[str, Any]:
    from msb_v2.audit.sovereign.metrics import compute_audit_sovereignty_score
    from msb_v2.audit.sovereign.store import SovereignAuditStore
    sovereign = SovereignAuditStore()
    merkle_ok = sovereign.merkle.verify_chain()
    snapshot = BusinessMetrics(audit=engine).snapshot()
    immutable_record = snapshot.get("immutable_record", {})
    root_hash = immutable_record.get("root_hash")
    total_blocks = immutable_record.get("total_blocks", 0)
    actions = AutoHealingPolicyEngine(audit=engine).evaluate()
    blocked = sum(1 for a in actions if a.get("status") == "blocked")
    score = compute_audit_sovereignty_score(
        merkle_ok=merkle_ok,
        fts=0.0,
        assumption_debt=0,
        veto_active=blocked == 0,
    )
    return {
        "merkle_ok": merkle_ok,
        "root_hash": root_hash,
        "total_blocks": total_blocks,
        "blocked_actions": blocked,
        "audit_sovereignty_score": score,
    }
