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
