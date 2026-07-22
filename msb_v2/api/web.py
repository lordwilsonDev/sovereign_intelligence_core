from __future__ import annotations

import logging
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from msb_v2.api.middleware import hcl_contract_middleware, require_bearer_token
from msb_v2.v3.contracts import HarnessContract, register as _register_contract
from msb_v2.engine.orchestrator import Task, orchestrate

from cognitive_compiler.sovereign_autonomy_core import SovereignAutonomyCore
from cognitive_compiler.sac_self_audit import SacSelfAuditor, get_auditor, set_app_factory
from msb_v2.provider.contract import ProviderContract
from msb_v2.transport.compression import compress_content

_register_contract(HarnessContract(route="/orchestrate", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(ProviderContract())
_register_contract(HarnessContract(route="/audit/recent", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/audit/summary", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/audit/policies", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/audit/policies/falsification", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/audit/report/html", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/audit/report/pdf", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/audit/verify", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/audit/sovereignty", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/health", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/runtime/ping", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/sac/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/sac/self-audit", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/metrics", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/studio/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/sovereign/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/environment/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/demo/query", method="post", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/chat", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/runtime/start", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/runtime/status", method="get", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/runtime/stop", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/status", method="get", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/worktree/create", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/browser/snapshot", method="get", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/gateway/telegram/webhook", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/continuity/resume-prompt", method="get", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/metrics", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/memory/add", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/memory/search", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/deepseek/provider/status", method="get", allow_anonymous=False, max_body_bytes=65536))

_ROUTER_REGISTRY: List[Tuple[Any, str]] = []
_HEALTH_MANAGER: Any = None
_RUNTIME_REGISTRY: Any = None
_POLICY_ENGINE: Any = None


class OrchestrateRequest(BaseModel):
    tasks: list[Task]
    intent: str | None = None
    metadata: dict[str, object] | None = None


def _register(router: Any, prefix: str) -> None:
    _ROUTER_REGISTRY.append((router, prefix))


def _load_routers() -> None:
    from msb_v2.api.cognitive import router as cognitive_router
    from msb_v2.api.imagination import router as imagination_router
    from msb_v2.api.moie import router as moie_router
    from msb_v2.api.aura import router as aura_router
    from msb_v2.api.aura_validate import router as aura_validate_router
    from msb_v2.api.rcoh import router as rcoh_router
    from msb_v2.api.deepseek import router as deepseek_router
    from msb_v2.api.eve import router as eve_router
    from msb_v2.api.eve_schedules import router as eve_schedules_router
    from msb_v2.api.cognitive_verification import router as cognitive_verification_router
    from msb_v2.api.rag import router as rag_router
    from msb_v2.api.moie_slug import router as moie_slug_router
    from msb_v2.api.torsion import router as torsion_router
    from msb_v2.api.memory import router as memory_router
    from msb_v2.api.memory_hierarchy import router as memory_hierarchy_router
    from msb_v2.api.values import router as values_router
    from msb_v2.api.reasoning import router as reasoning_router
    from msb_v2.api.reasoning_integrity import router as reasoning_integrity_router
    from msb_v2.api.consciousness import router as consciousness_router
    from msb_v2.api.demo import router as demo_router
    from msb_v2.api.counterfactual import router as counterfactual_router
    from msb_v2.api.reasoning_drift import router as reasoning_drift_router
    from msb_v2.api.observability import router as observability_router
    from msb_v2.api.observability_console import router as observability_console_router
    from msb_v2.observability.multica_dashboard import router as multica_dashboard_router
    from msb_v2.gateway.telegram_gateway import router as telegram_gateway_router
    from msb_v2.orca.router import router as orca_router
    from msb_v2.control.control_router import router as control_router
    from msb_v2.api.web_ui_router import router as web_ui_router
    from msb_v2.api.calibration import router as calibration_router
    from msb_v2.api.adk_bridge import router as adk_router
    from msb_v2.api.alert_hooks import router as alert_hooks_router
    from msb_v2.api.hooks import router as hooks_router
    from msb_v2.api.audit import router as audit_router
    from msb_v2.api.audit_report import router as audit_report_router
    from msb_v2.api.runtime import router as runtime_router
    from msb_v2.api.verification import router as verification_router
    from msb_v2.api.evolution import router as evolution_router
    from msb_v2.api.agent import router as agent_router
    from msb_v2.api.visualizer import router as visualizer_router
    from msb_v2.api.studio import router as studio_router
    from msb_v2.api.environment import router as environment_router
    from msb_v2.api.brain import router as brain_router
    from msb_v2.api.integrations import router as integrations_router
    from msb_v2.api.meta import router as meta_router
    from msb_v2.api.desktop import router as desktop_router
    from msb_v2.api.career import router as career_router
    from msb_v2.api.system import router as system_router
    from msb_v2.api.local_ai import router as local_ai_router
    from msb_v2.api.policy import router as policy_router
    from msb_v2.api.scheduler import router as scheduler_router
    from msb_v2.api.knowledge import router as knowledge_router
    from msb_v2.api.security import router as security_router
    from msb_v2.api.model_router import router as model_router
    from msb_v2.api.recovery import router as recovery_router
    from msb_v2.api.fine_tune import router as fine_tune_router
    from msb_v2.api.interfaces import router as interfaces_router
    from msb_v2.api.transport import router as transport_router
    from msb_v2.api.star import router as star_router
    from msb_v2.api.scth import router as scth_router
    from msb_v2.api.sn import router as sn_router
    from msb_v2.v3.policy import register_dispatch_contracts as _register_dispatch_contracts
    from msb_v2.api import v3 as v3_router
    _register(star_router, "/star")
    _register(scth_router, "/scth")
    _register(sn_router, "/sn")
    _register_dispatch_contracts()

    from msb_v2.api.governor import router as governor_router
    _register(governor_router, "/governor")
    from msb_v2.api import v3_inversion as v3_inversion_router
    from msb_v2.api import v3_deliberation as v3_deliberation_router
    from msb_v2.api import v3_knowledge as v3_knowledge_router
    from msb_v2.api import v3_twin as v3_twin_router
    from msb_v2.api import v3_tools as v3_tools_router
    from msb_v2.api import v3_tasks as v3_tasks_router
    from msb_v2.api import v3_crew as v3_crew_router
    from msb_v2.api.health import router as health_router
    from msb_v2.api.continuity import router as continuity_router
    from msb_v2.api.pipeline import router as pipeline_router
    from msb_v3.validation.api.router import router as validation_router
    from msb_v3.validation.api.ail import router as validation_ail_router
    from msb_v3.validation.api.propulsion import router as validation_propulsion_router

    from msb_v2.kernel import metrics as _kb4_metrics
    from msb_v2.pipeline import metrics as _pipeline_metrics

    _register(health_router, "")
    _register(continuity_router, "/continuity")
    _register(pipeline_router, "/pipeline")
    _register(validation_router, "/validation")
    _register(validation_ail_router, "/validation")
    _register(validation_propulsion_router, "/validation")
    _register(cognitive_router, "/cognitive")
    _register(imagination_router, "/imagination")
    _register(moie_router, "/moie")
    _register(moie_slug_router, "/moie/slug")
    _register(aura_router, "/aura")
    _register(aura_validate_router, "/aura")
    _register(rcoh_router, "/rcoh")
    _register(deepseek_router, "/deepseek")
    _register(eve_router, "/eve")
    _register(eve_schedules_router, "/eve")
    _register(rag_router, "/rag")
    _register(torsion_router, "/monitor/torsion")
    _register(memory_router, "/memory")
    _register(memory_hierarchy_router, "/memory")
    _register(values_router, "/values")
    _register(reasoning_router, "/reasoning")
    _register(reasoning_integrity_router, "/reasoning/integrity")
    _register(consciousness_router, "/consciousness")
    _register(demo_router, "/demo")
    _register(counterfactual_router, "/reasoning/counterfactual")
    _register(reasoning_drift_router, "/reasoning/drift")
    _register(observability_router, "/observability")
    _register(observability_console_router, "/observability")
    _register(multica_dashboard_router, "")
    _register(telegram_gateway_router, "")
    _register(control_router, "")
    _register(web_ui_router, "")
    _register(orca_router, "")
    _register(calibration_router, "/reasoning/calibration")
    _register(adk_router, "/adk")
    _register(alert_hooks_router, "/alerts")
    _register(hooks_router, "")
    _register(audit_router, "/audit")
    _register(audit_report_router, "/audit")
    _register(runtime_router, "")
    _register(verification_router, "")
    _register(evolution_router, "/evolution")
    _register(agent_router, "")
    _register(visualizer_router, "/visualizer")
    _register(studio_router, "")
    _register(environment_router, "")
    _register(brain_router, "/brain")
    _register(integrations_router, "")
    _register(meta_router, "")
    _register(desktop_router, "")
    _register(career_router, "")
    _register(system_router, "")
    _register(policy_router, "")
    _register(model_router, "")
    _register(recovery_router, "")
    _register(scheduler_router, "")
    _register(knowledge_router, "")
    _register(security_router, "")
    _register(fine_tune_router, "")
    _register(interfaces_router, "")
    _register(transport_router, "")
    _register(local_ai_router, "")
    from msb_v2.api import v3 as v3_router
    _register(v3_router.router, "")
    _register(v3_inversion_router.router, "")
    _register(v3_deliberation_router.router, "")
    _register(v3_knowledge_router.router, "")
    _register(v3_twin_router.router, "")
    _register(v3_tools_router.router, "")
    _register(v3_tasks_router.router, "")
    _register(v3_crew_router.router, "")
    from msb_v2.api.scth import router as scth_router
    _register(scth_router, "/scth")
    from msb_v2.api.cloud_agent import router as cloud_agent_router
    _register(cloud_agent_router, "/cloud-agent")
    from msb_v2.api.echo import router as echo_router
    _register(echo_router, "/echo")
    from msb_v2.api.systems_health import router as systems_health_router
    _register(systems_health_router, "/systems-health")
    from msb_v2.api.soh import router as soh_router
    _register(soh_router, "/soh")
    from msb_v2.api.sshh import router as sshh_router
    _register(sshh_router, "/sshh")
    from msb_v2.api.optimize import router as optimize_router
    _register(optimize_router, "/optimize")
    from msb_v2.api.schh import router as schh_router
    _register(schh_router, "/schh")
    try:
        from msb_v2.api.sn import router as sn_router
        _register(sn_router, "/sn")
    except Exception:
        pass
    try:
        from msb_v2.v3.policy import register_dispatch_contracts as _register_dispatch_contracts
        _register_dispatch_contracts()
    except Exception:
        pass
    try:
        from msb_v2.api import cloud_agent_contracts
    except Exception:
        pass


def create_app() -> FastAPI:
    app = FastAPI(title="MSB v2.0")
    app.middleware("http")(hcl_contract_middleware)

    _attach_runtime()

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        status_code = getattr(exc, 'status_code', None)
        if isinstance(status_code, int) and 400 <= status_code < 600:
            raise
        correlation_id = str(uuid.uuid4())
        logging.getLogger("msb_v2.api.errors").error("Unhandled exception %s: %s", correlation_id, exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "correlation_id": correlation_id,
                "detail": str(exc),
            },
        )

    @app.get("/health")
    def health() -> dict:
        return {
            "status": "ok",
            "runtime": {
                "state": _HEALTH_MANAGER.state.value if _HEALTH_MANAGER is not None else "unknown",
                "uptime_seconds": _HEALTH_MANAGER.uptime if _HEALTH_MANAGER is not None else 0.0,
            },
            "contracts": {
                "registered": len(_RUNTIME_REGISTRY.all()) if _RUNTIME_REGISTRY is not None else 0,
                "names": [c.name for c in (_RUNTIME_REGISTRY.all() or [])],
            },
        }

    @app.get("/runtime/capabilities")
    def runtime_capabilities() -> dict:
        if _RUNTIME_REGISTRY is None:
            return {"registry_state": "unattached", "capabilities": []}
        entries = []
        for contract in _RUNTIME_REGISTRY.all():
            entries.append(contract.capability_interface())
        return {"registry_state": "attached", "capabilities": entries}

    @app.get("/runtime/policies")
    def runtime_policies() -> dict:
        if _POLICY_ENGINE is None:
            return {"registry_state": "unattached", "policies": []}
        entries = []
        for rule in _POLICY_ENGINE._rules.values():
            entries.append({
                "rule_id": rule.rule_id,
                "name": rule.name,
                "category": rule.category,
                "enforcement": rule.enforcement.value,
                "owner": rule.owner,
                "rationale": rule.rationale,
            })
        return {"registry_state": "attached", "policies": entries}

    @app.post("/runtime/policies/evaluate")
    def runtime_policies_evaluate(payload: dict) -> dict:
        if _POLICY_ENGINE is None:
            return {"registry_state": "unattached", "results": []}
        context = payload if isinstance(payload, dict) else {}
        return {"registry_state": "attached", "results": _POLICY_ENGINE.evaluate(context)}

    @app.post("/runtime/mutation/request")
    def runtime_mutation_request(payload: dict) -> dict:
        intent = str(payload.get("intent", "")).strip()
        actor = str(payload.get("actor", "")).strip()
        if not intent or not actor:
            return {"status": "error", "detail": "intent and actor are required"}
        from msb_v2.runtime.mutation_guard import guard as _mutation_guard
        return _mutation_guard().request(
            intent=intent,
            actor=actor,
            payload=payload if isinstance(payload, dict) else {},
            signature=payload.get("signature"),
        )

    @app.get("/runtime/governance/state")
    def runtime_governance_state() -> dict:
        from msb_v2.runtime.state import governance_state as _governance_state
        return _governance_state()

    @app.get("/runtime/ping")
    def runtime_ping() -> dict:
        return {"status": "ok", "module": "runtime"}

    @app.post("/orchestrate")
    def orchestrate_endpoint(payload: OrchestrateRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> list:
        intent = payload.intent or payload.metadata.get("intent") if isinstance(payload.metadata, dict) else None
        if intent == "orca_worktree":
            repo = ((payload.metadata or {}).get("repo") if isinstance(payload.metadata, dict) else None) or "/Users/lordwilson/msb-v2"
            agent = ((payload.metadata or {}).get("agent") if isinstance(payload.metadata, dict) else None) or "default"
            from msb_v2.orca.router import orca_worktree_create, WorktreeCreateRequest
            body = WorktreeCreateRequest(repo=str(repo), agent=str(agent))
            result = orca_worktree_create(body)
            return [{"id": result.session_id, "status": "orchestrated", "intent": intent, "worktree": result.model_dump()}]
        from msb_v2.audit.audit_engine import AuditEngine
        from msb_v2.audit.hooks import build_audit_hook
        engine = AuditEngine()
        audit_hook = build_audit_hook(engine, workflow="orchestrate", agent="api")
        from msb_v2.engine.orchestrator import orchestrate
        return [{"id": t.id, "status": t.status} for t in orchestrate(payload.tasks, hook=lambda event_name, task_id, payload, metadata: (audit_hook(event_name, task_id, payload, metadata), {})[1])]

    if not _ROUTER_REGISTRY:
        _load_routers()

    seen: Dict[str, Tuple[Any, str]] = {}
    unique_routes: List[Tuple[Any, str]] = []
    dupes = 0
    for router, prefix in _ROUTER_REGISTRY:
        for route in getattr(router, 'routes', []):
            if not hasattr(route, 'path'):
                continue
            path = prefix + route.path
            key = path + '|' + (','.join(sorted(method.upper() for method in getattr(route, 'methods', []) or [])))
            if key in seen:
                dupes += 1
                continue
            seen[key] = (router, prefix)
        if any(hasattr(r, 'path') for r in getattr(router, 'routes', [])):
            unique_routes.append((router, prefix))
        else:
            unique_routes.append((router, prefix))

    logging.getLogger(__name__).info("router registry started with %d entries, %d duplicates, %d mounted routers", len(_ROUTER_REGISTRY), dupes, len(unique_routes))

    for router, prefix in unique_routes:
        app.include_router(router, prefix=prefix)

    @app.get("/sac/status")
    def sac_status() -> dict:
        core = SovereignAutonomyCore()
        return SovereignAutonomyCore.to_dict(
            core.run_dispatch_gate(query="api-status", context={"high_stakes": False}, model_source="local")
        )

    @app.get("/sac/self-audit")
    def sac_self_audit() -> dict:
        report = get_auditor().run_audit()
        return {
            "mirage_detected": report.mirage_detected,
            "sas_confidence_weight": report.sas_confidence_weight,
            "adversarial_finding": report.adversarial_finding,
            "cma_verdict": report.cma_verdict,
            "cma_details": report.cma_details,
            "timestamp": report.timestamp,
        }

    try:
        from prometheus_client import generate_latest, REGISTRY

        @app.get("/metrics")
        def prometheus_metrics() -> Response:
            data = generate_latest(REGISTRY)
            return Response(
                content=data,
                media_type="text/plain; version=0.0.4; charset=utf-8",
            )
    except Exception:
        pass

    set_app_factory(create_app)

    try:
        import threading

        _sac_bg_logger = logging.getLogger("msb_v2.sac_self_audit.bg")

        def _background_audit_loop() -> None:
            _sac_bg_logger.info("SAC background audit loop starting")
            while True:
                try:
                    auditor = get_auditor()
                    report = auditor.run_audit()
                    result = {
                        "mirage_detected": report.mirage_detected,
                        "sas_confidence_weight": report.sas_confidence_weight,
                        "adversarial_finding": report.adversarial_finding,
                        "cma_verdict": report.cma_verdict,
                        "cma_details": report.cma_details,
                        "timestamp": report.timestamp,
                    }
                    if result.get("mirage_detected"):
                        _sac_bg_logger.warning("SAC self-audit detected a mirage. Confidence weight halved.")
                    else:
                        _sac_bg_logger.info("SAC self-audit clean.")
                except Exception as exc:
                    _sac_bg_logger.error("SAC self-audit failed: %s", exc)
                time.sleep(3600)

        if not getattr(create_app, "_sac_audit_started", False):
            t = threading.Thread(target=_background_audit_loop, daemon=True)
            t.start()
            create_app._sac_audit_started = True  # type: ignore[attr-defined]

        from msb_v2.audit.audit_engine import AuditEngine
        from msb_v2.audit.storage import AuditStore
        from msb_v2.audit.telemetry import AuditTelemetry

        _telem_engine = AuditEngine(store=AuditStore())
        _telemetry = AuditTelemetry(audit=_telem_engine)

        def _audit_telemetry_loop() -> None:
            while True:
                try:
                    _telemetry.maybe_resync()
                except Exception:
                    pass
                time.sleep(60.0)

        if not getattr(create_app, "_audit_telemetry_started", False):
            threading.Thread(target=_audit_telemetry_loop, daemon=True).start()
            create_app._audit_telemetry_started = True  # type: ignore[attr-defined]

        from msb_v2.audit.auto_healing import AutoHealingPolicyEngine
        from msb_v2.audit.audit_engine import AuditEngine
        from msb_v2.audit.storage import AuditStore
        from msb_v2.audit.telemetry import _update_policy_metrics, update_sovereign_metrics
        from msb_v2.audit.sovereign.metrics import compute_audit_sovereignty_score
        from msb_v2.audit.sovereign.store import SovereignAuditStore

        _policy_engine = AutoHealingPolicyEngine(audit=AuditEngine(store=AuditStore()))

        def _policy_engine_loop() -> None:
            while True:
                try:
                    actions = _policy_engine.evaluate()
                    _update_policy_metrics(actions)
                    engine = _policy_engine._audit
                    falsification = engine.falsification_snapshot()
                    fts = 0.0
                    if falsification.get("count", 0) > 0:
                        fts = falsification.get("falsified_count", 0) / falsification["count"]
                    assumption_debt = engine.assumption_debt_count()
                    try:
                        merkle_ok = SovereignAuditStore().merkle.verify_chain()
                    except Exception:
                        merkle_ok = False
                    score = compute_audit_sovereignty_score(
                        merkle_ok=merkle_ok,
                        fts=fts,
                        assumption_debt=assumption_debt,
                        veto_active=any(a.get("status") == "blocked" for a in actions),
                    )
                    update_sovereign_metrics(
                        fts=fts,
                        assumption_debt=assumption_debt,
                        audit_sovereignty_score=score,
                    )
                except Exception:
                    pass
                time.sleep(1800)

        if not getattr(create_app, "_policy_engine_started", False):
            threading.Thread(target=_policy_engine_loop, daemon=True).start()
            create_app._policy_engine_started = True  # type: ignore[attr-defined]
    except Exception:
        pass
    return app


_app_factory_lock = False


def ensure_factory_registry() -> None:
    global _app_factory_lock
    if _app_factory_lock:
        return
    _app_factory_lock = True
    try:
        if not _ROUTER_REGISTRY:
            _load_routers()

        seen: Dict[str, Tuple[Any, str]] = {}
        unique_routes: List[Tuple[Any, str]] = []
        dupes = 0
        for router, prefix in _ROUTER_REGISTRY:
            for route in getattr(router, 'routes', []):
                if not hasattr(route, 'path'):
                    continue
                path = prefix + route.path
                key = path + '|' + (','.join(sorted(method.upper() for method in getattr(route, 'methods', []) or [])))
                if key in seen:
                    dupes += 1
                    continue
                seen[key] = (router, prefix)
            unique_routes.append((router, prefix))

        for router, prefix in unique_routes:
            globals()['app'].include_router(router, prefix=prefix)
    finally:
        _app_factory_lock = False


def _attach_runtime() -> None:
    global _HEALTH_MANAGER, _RUNTIME_REGISTRY, _POLICY_ENGINE
    try:
        from msb_v2.runtime.lifecycle import LifecycleManager
        from msb_v2.runtime.health import HealthManager
        from msb_v2.runtime.contracts import registry as _runtime_registry
        _RUNTIME_REGISTRY = _runtime_registry()
        _HEALTH_MANAGER = LifecycleManager()
        _HEALTH_MANAGER.initialize()
        HealthManager().record("ok", detail="from _attach_runtime")
        from msb_v2.runtime.governor import register_runtime_capabilities
        register_runtime_capabilities()
    except Exception:
        pass
    try:
        from msb_v2.runtime.policy import policy_engine, register_default_rules
        _POLICY_ENGINE = policy_engine()
        register_default_rules()
    except Exception:
        pass
