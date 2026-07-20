from __future__ import annotations

import logging
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from msb_v2.api.middleware import hcl_contract_middleware, require_bearer_token
from msb_v2.v3.contracts import HarnessContract, register as _register_contract
from msb_v2.engine.orchestrator import Task, orchestrate

from cognitive_compiler.sovereign_autonomy_core import SovereignAutonomyCore
from cognitive_compiler.sac_self_audit import SacSelfAuditor, get_auditor, set_app_factory
from msb_v2.transport.compression import compress_content

_register_contract(HarnessContract(route="/orchestrate", method="post", allow_anonymous=False, max_body_bytes=65536))
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
_register_contract(HarnessContract(route="/chat", method="post", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/runtime/start", method="post", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/runtime/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/runtime/stop", method="post", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/worktree/create", method="post", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/browser/snapshot", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/gateway/telegram/webhook", method="post", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/metrics", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/memory/add", method="post", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/memory/search", method="post", allow_anonymous=True, max_body_bytes=65536))

_ROUTER_REGISTRY: List[Tuple[Any, str]] = []


class OrchestrateRequest(BaseModel):
    tasks: list[Task]


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
    from msb_v2.api.demo import router as demo_router
    from msb_v2.api.counterfactual import router as counterfactual_router
    from msb_v2.api.reasoning_drift import router as reasoning_drift_router
    from msb_v2.api.observability import router as observability_router
    from msb_v2.api.observability_console import router as observability_console_router
    from observability.multica_dashboard import router as multica_dashboard_router
    from msb_v2.gateway.telegram_gateway import router as telegram_gateway_router
    from msb_v2.orca.router import router as orca_router
    from msb_v2.control.control_router import router as control_router
    from msb_v2.api.web_ui_router import router as web_ui_router
    from msb_v2.api.calibration import router as calibration_router
    from msb_v2.api.adk_bridge import router as adk_router
    from msb_v2.api.alert_hooks import router as alert_hooks_router
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
    from msb_v2.api.auth import router as auth_router
    from msb_v2.api.policy import router as policy_router
    from msb_v2.api.scheduler import router as scheduler_router
    from msb_v2.api.knowledge import router as knowledge_router
    from msb_v2.api.security import router as security_router
    from msb_v2.api.model_router import router as model_router
    from msb_v2.api.recovery import router as recovery_router
    from msb_v2.api.fine_tune import router as fine_tune_router
    from msb_v2.api.interfaces import router as interfaces_router
    from msb_v2.api.transport import router as transport_router
    from msb_v2.api import v3 as v3_router
    from msb_v2.api import v3_inversion as v3_inversion_router
    from msb_v2.api import v3_deliberation as v3_deliberation_router
    from msb_v2.api import v3_knowledge as v3_knowledge_router
    from msb_v2.api import v3_twin as v3_twin_router
    from msb_v2.api import v3_tools as v3_tools_router
    from msb_v2.api import v3_tasks as v3_tasks_router
    from msb_v2.api import v3_crew as v3_crew_router
    from msb_v2.api.health import router as health_router

    _register(health_router, "")
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
    _register(runtime_router, "")
    _register(verification_router, "")
    _register(evolution_router, "")
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
    _register(auth_router, "")
    _register(policy_router, "")
    _register(model_router, "")
    _register(recovery_router, "")
    _register(scheduler_router, "")
    _register(knowledge_router, "")
    _register(security_router, "")
    _register(fine_tune_router, "")
    _register(interfaces_router, "")
    _register(transport_router, "")
    _register(v3_router.router, "")
    _register(v3_inversion_router.router, "")
    _register(v3_deliberation_router.router, "")
    _register(v3_knowledge_router.router, "")
    _register(v3_twin_router.router, "")
    _register(v3_tools_router.router, "")
    _register(v3_tasks_router.router, "")
    _register(v3_crew_router.router, "")


def create_app() -> FastAPI:
    app = FastAPI(title="MSB v2.0")
    app.middleware("http")(hcl_contract_middleware)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
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
        return {"status": "ok"}

    @app.get("/runtime/ping")
    def runtime_ping() -> dict:
        return {"status": "ok", "module": "runtime"}

    @app.post("/orchestrate")
    def orchestrate_endpoint(payload: OrchestrateRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> list:
        return [{"id": t.id, "status": t.status} for t in orchestrate(payload.tasks)]

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

    if dupes:
        print(f"[router-dup] skipped {dupes} duplicate effective route registrations; validate router prefixes")

    if len(unique_routes) != len(_ROUTER_REGISTRY):
        print(f"[router-check] mounted {len(unique_routes)} unique routers from {len(_ROUTER_REGISTRY)} entries")

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
        from fastapi.responses import Response as FastAPIResponse

        @app.get("/metrics")
        def prometheus_metrics() -> FastAPIResponse:
            data = generate_latest(REGISTRY)
            return FastAPIResponse(content=data, media_type="text/plain; version=0.0.4")
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

        if dupes:
            print(f"[router-dup] skipped {dupes} duplicate effective route registrations; validate router prefixes")

        if len(unique_routes) != len(_ROUTER_REGISTRY):
            print(f"[router-check] mounted {len(unique_routes)} unique routers from {len(_ROUTER_REGISTRY)} entries")

        for router, prefix in unique_routes:
            globals()['app'].include_router(router, prefix=prefix)
    finally:
        _app_factory_lock = False
