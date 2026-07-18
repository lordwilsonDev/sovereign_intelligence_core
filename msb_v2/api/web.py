from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from msb_v2.api.cognitive import router as cognitive_router
from msb_v2.api.imagination import router as imagination_router
from msb_v2.api.moie import router as moie_router
from msb_v2.api.aura import router as aura_router
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
from msb_v2.api import v3 as v3_router
from msb_v2.api import v3_inversion as v3_inversion_router
from msb_v2.api import v3_deliberation as v3_deliberation_router
from msb_v2.api import v3_knowledge as v3_knowledge_router
from msb_v2.api import v3_twin as v3_twin_router
from msb_v2.api import v3_tools as v3_tools_router
from msb_v2.api import v3_tasks as v3_tasks_router
from msb_v2.api import v3_crew as v3_crew_router
from msb_v2.engine.orchestrator import Task, orchestrate


class OrchestrateRequest(BaseModel):
    tasks: list[Task]


def create_app() -> FastAPI:
    app = FastAPI(title="MSB v2.0")

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.get("/runtime/ping")
    def runtime_ping() -> dict:
        return {"status": "ok", "module": "runtime"}

    @app.post("/orchestrate")
    def orchestrate_endpoint(payload: OrchestrateRequest) -> list:
        return [{"id": t.id, "status": t.status} for t in orchestrate(payload.tasks)]

    app.include_router(cognitive_router, prefix="/cognitive")
    app.include_router(cognitive_verification_router, prefix="/cognitive")
    app.include_router(imagination_router, prefix="/imagination")
    app.include_router(moie_router, prefix="/moie")
    app.include_router(moie_slug_router, prefix="/moie/slug")
    app.include_router(aura_router, prefix="/aura")
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
    app.include_router(v3_router.router)
    app.include_router(v3_inversion_router.router)
    app.include_router(v3_deliberation_router.router)
    app.include_router(v3_knowledge_router.router)
    app.include_router(v3_twin_router.router)
    app.include_router(v3_tools_router.router)
    app.include_router(v3_tasks_router.router)
    app.include_router(v3_crew_router.router)
    return app
