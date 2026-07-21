from fastapi import APIRouter, Request
from msb_v2.local_ai.model_manager import ModelManager
from msb_v2.local_ai.inference_engine import InferenceEngine
from msb_v2.local_ai.router import SLAHRouter
from typing import Any, Dict


router = APIRouter()
_slah = SLAHRouter()
_manager = ModelManager()


@router.post("/local-ai/intent")
def local_ai_intent(payload: Dict[str, Any], request: Request) -> Dict[str, Any]:
    return _slah.handle_intent(payload)


@router.get("/local-ai/models")
def local_ai_models() -> Dict[str, Any]:
    models = _manager.list_models()
    return {"models": [
        {
            "id": m.id,
            "source": m.source,
            "size_bytes": m.size_bytes,
            "modified_at": m.modified_at,
            "last_used_at": m.last_used_at,
            "license": m.license,
        }
        for m in models
    ]}


@router.post("/local-ai/infer")
def local_ai_infer(payload: Dict[str, Any], request: Request) -> Dict[str, Any]:
    model = payload.get("model") or "qwen2.5:0.5b"
    prompt = payload.get("prompt", "")
    result = InferenceEngine().generate(model_id=model, prompt=prompt)
    _manager.record_use(result.model)
    return {"text": result.text, "model": result.model, "backend": result.backend}


from msb_v2.local_ai.deploy_engine import DeployEngine

_deploy = DeployEngine()


@router.post("/local-ai/deploy")
def local_ai_deploy(payload: Dict[str, Any]) -> Dict[str, Any]:
    model_id = str(payload.get("model") or "").strip()
    port = int(payload.get("port") or 9100)
    base_url = str(payload.get("base_url") or "http://127.0.0.1:11434").rstrip("/")
    if not model_id:
        return {"status": "error", "error": "model is required"}
    return _deploy.deploy(model_id=model_id, port=port, base_url=base_url)


@router.get("/local-ai/deployments")
def local_ai_deployments() -> Dict[str, Any]:
    return {"deployments": _deploy.list_deployments()}


@router.post("/local-ai/deploy/stop")
def local_ai_deploy_stop(payload: Dict[str, Any]) -> Dict[str, Any]:
    model_id = str(payload.get("model") or "").strip()
    port = int(payload.get("port") or 9100)
    return _deploy.stop(model_id=model_id, port=port)


from msb_v2.local_ai.optimize_engine import OptimizeEngine

_optimize = OptimizeEngine()


@router.get("/local-ai/optimize")
def local_ai_optimize(query: str = "") -> Dict[str, Any]:
    model_id = str(query or "qwen2.5:0.5b").strip()
    try:
        return _optimize.optimize(model_id=model_id)
    except Exception as exc:
        return {"status": "error", "error": str(exc)}
