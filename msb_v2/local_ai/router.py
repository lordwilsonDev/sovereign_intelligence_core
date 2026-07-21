from __future__ import annotations

from typing import Any, Dict
import urllib.request
import urllib.error
import json

from .inference_engine import InferenceEngine


class SLAHRouter:
    def handle_intent(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        raw = (intent.get("intent") or "").lower().strip()
        model = intent.get("model") or "qwen2.5:0.5b"
        prompt = intent.get("prompt") or "State your capabilities in one sentence."
        if any(token in raw for token in ["infer", "run inference", "generate", "ask", "use model"]):
            try:
                result = InferenceEngine().generate(model_id=model, prompt=prompt)
                return {"action": "infer", "backend": result.backend, "model": result.model, "text": result.text}
            except urllib.error.URLError as exc:
                return {"action": "infer", "backend": "ollama", "status": "error", "error": str(exc)}
            except Exception as exc:
                return {"action": "infer", "backend": "ollama", "status": "error", "error": str(exc)}
        if any(token in raw for token in ["deploy", "benchmark", "optimize", "download", "start"]):
            action = raw.split("---")[0].strip() if "---" in raw else raw.strip()
            return {"action": "acknowledged", "status": "planned", "action": action}
        return {"action": "unknown", "status": "todo", "intent": raw}
