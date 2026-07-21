from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from msb_v2.api.middleware import require_bearer_token
from msb_v2.audit.audit_engine import AuditEngine
from msb_v2.audit.auto_healing import AutoHealingPolicyEngine
from msb_v2.audit.business_metrics import BusinessMetrics
from msb_v2.audit.sovereign.metrics import compute_audit_sovereignty_score
from msb_v2.audit.sovereign.merkle import AuditMerkleChain
from msb_v2.audit.sovereign.store import SovereignAuditStore
from msb_v2.audit.storage import AuditStore

router = APIRouter()


def _engine() -> AuditEngine:
    return AuditEngine(store=AuditStore())


def _sovereign_store() -> SovereignAuditStore:
    return SovereignAuditStore()


@router.get("/recent")
def recent_audit_events(limit: int = 100, engine: AuditEngine = Depends(_engine)) -> list[dict[str, Any]]:
    return engine.events(limit=limit)


@router.get("/summary")
def audit_summary(limit: int = 100, engine: AuditEngine = Depends(_engine)) -> dict[str, Any]:
    engine.events(limit=limit)
    return BusinessMetrics(audit=engine).snapshot()


@router.get("/policies")
def audit_policies(engine: AuditEngine = Depends(_engine)) -> dict[str, Any]:
    actions = AutoHealingPolicyEngine(audit=engine).evaluate()
    return {"actions": actions, "count": len(actions)}


@router.get("/policies/falsification")
def audit_policies_falsification(engine: AuditEngine = Depends(_engine)) -> dict[str, Any]:
    policy = AutoHealingPolicyEngine(audit=engine)
    return policy.falsification_snapshot()


@router.get("/verify")
def audit_verify(store: SovereignAuditStore = Depends(_sovereign_store)) -> dict[str, Any]:
    return {"verified": store.merkle.verify_chain(), "log": str(store.merkle.log_path)}


@router.get("/sovereignty")
def audit_sovereignty(
    engine: AuditEngine = Depends(_engine),
    store: SovereignAuditStore = Depends(_sovereign_store),
) -> dict[str, Any]:
    merkle_ok = store.merkle.verify_chain()
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
