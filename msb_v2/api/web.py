from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import hcl_contract_middleware, require_bearer_token

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

from msb_v2.engine.orchestrator import Task, orchestrate

from cognitive_compiler.sovereign_autonomy_core import SovereignAutonomyCore
from cognitive_compiler.sac_self_audit import SacSelfAuditor, get_auditor
from msb_v2.transport.compression import compress_content
from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract

_register_contract(HarnessContract(route="/orchestrate", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/health", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/runtime/ping", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/sac/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/sac/self-audit", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/metrics", method="get", allow_anonymous=True, max_body_bytes=65536))
class OrchestrateRequest(BaseModel):
    tasks: list[Task]


def create_app() -> FastAPI:
    app = FastAPI(title="MSB v2.0")
    app.middleware("http")(hcl_contract_middleware)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/runtime/ping")
    def runtime_ping() -> dict:
        return {"status": "ok", "module": "runtime"}

    @app.post("/orchestrate")
    def orchestrate_endpoint(payload: OrchestrateRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> list:
        return [{"id": t.id, "status": t.status} for t in orchestrate(payload.tasks)]

    app.include_router(cognitive_router, prefix="/cognitive")
    app.include_router(cognitive_verification_router, prefix="/cognitive")
    app.include_router(imagination_router, prefix="/imagination")
    app.include_router(moie_router, prefix="/moie")
    app.include_router(moie_slug_router, prefix="/moie/slug")
    app.include_router(aura_router, prefix="/aura")
    app.include_router(aura_validate_router, prefix="/aura")
    app.include_router(rcoh_router, prefix="/rcoh")
    app.include_router(deepseek_router, prefix="/deepseek")
    app.include_router(eve_router, prefix="/eve")
    app.include_router(eve_schedules_router, prefix="/eve")
    app.include_router(rag_router, prefix="/rag")
    app.include_router(torsion_router, prefix="/monitor/torsion")
    app.include_router(memory_router, prefix="/memory")
    app.include_router(memory_hierarchy_router, prefix="/memory")
    app.include_router(values_router, prefix="/values")
    app.include_router(reasoning_router, prefix="/reasoning")
    app.include_router(reasoning_integrity_router, prefix="/reasoning/integrity")
    app.include_router(demo_router, prefix="/demo")
    app.include_router(counterfactual_router, prefix="/reasoning/counterfactual")
    app.include_router(reasoning_drift_router, prefix="/reasoning/drift")
    app.include_router(observability_router, prefix="/observability")
    app.include_router(observability_console_router, prefix="/observability")
    app.include_router(calibration_router, prefix="/reasoning/calibration")
    app.include_router(adk_router, prefix="/adk")
    app.include_router(alert_hooks_router, prefix="/alerts")
    app.include_router(runtime_router, prefix="")
    app.include_router(verification_router, prefix="")
    app.include_router(evolution_router, prefix="")
    app.include_router(agent_router, prefix="")
    app.include_router(visualizer_router, prefix="/visualizer")
    app.include_router(studio_router, prefix="")
    app.include_router(environment_router, prefix="")
    app.include_router(brain_router, prefix="/brain")
    app.include_router(integrations_router, prefix="")
    app.include_router(meta_router, prefix="")
    app.include_router(desktop_router, prefix="")
    app.include_router(career_router, prefix="")
    app.include_router(system_router, prefix="")
    app.include_router(auth_router)
    app.include_router(policy_router)
    app.include_router(model_router)
    app.include_router(recovery_router)
    app.include_router(scheduler_router)
    app.include_router(knowledge_router)
    app.include_router(security_router)
    app.include_router(fine_tune_router)
    app.include_router(interfaces_router)
    app.include_router(transport_router)
    try:
        from msb_v2.transport.compression_middleware import ResponseCompressionMiddleware
        app.add_middleware(ResponseCompressionMiddleware, threshold=2000)
    except Exception:
        pass
    app.include_router(v3_router.router)
    app.include_router(v3_inversion_router.router)
    app.include_router(v3_deliberation_router.router)
    app.include_router(v3_knowledge_router.router)
    app.include_router(v3_twin_router.router)
    app.include_router(v3_tools_router.router)
    app.include_router(v3_tasks_router.router)
    app.include_router(v3_crew_router.router)
    @app.get("/sac/status")
    def sac_status() -> dict:
        core = SovereignAutonomyCore()
        return SovereignAutonomyCore.to_dict(
            core.run_dispatch_gate(query="api-status", context={"high_stakes": False}, model_source="local")
        )

    @app.get("/sac/self-audit")
    def sac_self_audit() -> dict:
        return get_auditor().run_audit()

    try:
        from prometheus_client import generate_latest, REGISTRY
        from fastapi.responses import Response as FastAPIResponse

        @app.get("/metrics")
        def prometheus_metrics() -> FastAPIResponse:
            data = generate_latest(REGISTRY)
            return FastAPIResponse(content=data, media_type="text/plain; version=0.0.4")
    except Exception:
        pass

    from cognitive_compiler.sac_self_audit import set_app_factory
    set_app_factory(create_app)

    try:
        import threading
        from cognitive_compiler.sac_self_audit import SacSelfAuditor
        _sac_bg_logger = logging.getLogger("msb_v2.sac_self_audit.bg")

        def _background_audit_loop() -> None:
            _sac_bg_logger.info("SAC background audit loop starting")
            while True:
                try:
                    auditor = get_auditor()
                    result = auditor.run_audit()
                    if result.get("mirage_detected"):
                        _sac_bg_logger.warning("SAC self-audit detected a mirage. Confidence weight halved.")
                    else:
                        _sac_bg_logger.info("SAC self-audit clean.")
                except Exception as exc:
                    _sac_bg_logger.error("SAC self-audit failed: %s", exc)
                time.sleep(3600)

        t = threading.Thread(target=_background_audit_loop, daemon=True)
        t.start()
    except Exception:
        pass
    return app
