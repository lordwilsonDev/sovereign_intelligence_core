from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.auto_healing import AutoHealingPolicyEngine
from msb_v2.audit.business_metrics import BusinessMetrics
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
    return engine.falsification_snapshot()


@router.post("/policies/falsification/advance")
def audit_policies_falsification_advance(payload: dict[str, Any] | None = None, engine: AuditEngine = Depends(_engine)) -> dict[str, Any]:
    policy = ((payload or {}).get("policy") or "").strip() if isinstance(payload, dict) else ""
    try:
        raw_actions = AutoHealingPolicyEngine(audit=engine).evaluate()
    except Exception:
        raw_actions = []
    actions: list[dict[str, Any]] = []
    for action in raw_actions:
        name = action.get("policy") if isinstance(action, dict) else None
        if isinstance(name, str) and policy in name:
            actions.append({"policy": name, "action": "advanced", "state": "advanced"})
    snapshot = engine.falsification_snapshot()
    records = snapshot.get("records", []) if isinstance(snapshot, dict) else []
    latest = records[-1:] if records else []
    return {
        "advanced": len(actions),
        "actions": actions,
        "records_updated": len(latest),
        "latest": latest,
        "count": len(records),
    }


@router.get("/verify")
def audit_verify(store: AuditStore = Depends(_engine)) -> dict[str, Any]:
    from msb_v2.audit.sovereign.merkle import AuditMerkleChain
    from msb_v2.audit.sovereign.store import SovereignAuditStore
    sovereign = SovereignAuditStore()
    valid = sovereign.merkle.verify_chain()
    falsification = store.falsification_snapshot() if hasattr(store, "falsification_snapshot") else {}
    fts = 0.0
    if isinstance(falsification, dict) and falsification.get("count", 0) > 0:
        fts = falsification.get("falsified_count", 0) / falsification["count"]
    return {
        "verified": valid,
        "chain_valid": valid,
        "chain_root_hash": getattr(sovereign.merkle, "root_hash", ""),
        "log": str(sovereign.merkle.log_path),
        "falsification_feedback": {
            "enabled": True,
            "fts": fts,
            "falsified_count": falsification.get("falsified_count", 0) if isinstance(falsification, dict) else 0,
            "latest_policy": ((falsification.get("records") or [{}])[-1].get("policy") if isinstance(falsification, dict) and falsification.get("records") else None),
        },
    }


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
    falsification = engine.falsification_snapshot()
    fts = 0.0
    if falsification.get("count", 0) > 0:
        fts = falsification.get("falsified_count", 0) / falsification["count"]
    assumption_debt = engine.assumption_debt_count()
    score = compute_audit_sovereignty_score(
        merkle_ok=merkle_ok,
        fts=fts,
        assumption_debt=assumption_debt,
        veto_active=bool(blocked),
    )
    return {
        "merkle_ok": merkle_ok,
        "root_hash": root_hash,
        "total_blocks": total_blocks,
        "blocked_actions": blocked,
        "falsified_count": falsification.get("falsified_count", 0),
        "fts": fts,
        "assumption_debt": assumption_debt,
        "audit_sovereignty_score": score,
        "falsification": {
            "count": falsification.get("count", 0),
            "falsified_count": falsification.get("falsified_count", 0),
            "fts": fts,
            "records": falsification.get("records", []),
        },
    }
