from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class ServingDeployment:
    model_id: str
    port: int
    process: Optional[threading.Thread] = None
    status: str = "running"


class DeployEngine:
    def __init__(self) -> None:
        self._deployments: Dict[str, ServingDeployment] = {}

    def deploy(self, model_id: str, port: int, base_url: str = "http://127.0.0.1:11434") -> Dict[str, Any]:
        if not base_url:
            return {"status": "error", "error": "base_url required"}
        # Build minimal local FastAPI wrapper after module-level guard.
        try:
            import fastapi  # noqa: F401
            from fastapi import FastAPI
            import uvicorn
        except Exception as exc:
            return {"status": "error", "error": f"fastapi/uvicorn unavailable: {exc}"}
        app = FastAPI()

        @app.get("/health")
        def health():
            return {"status": "ok", "model": model_id, "port": port}

        @app.post("/generate")
        def generate(payload: Dict[str, Any]):
            prompt = payload.get("prompt", "")
            max_tokens = int(payload.get("max_tokens", 128))
            temperature = float(payload.get("temperature", 0.2))
            try:
                engine = InferenceEngine(base_url=base_url)
                result = engine.generate(model_id=model_id, prompt=prompt, max_tokens=max_tokens, temperature=temperature)
                return {"text": result.text, "backend": result.backend, "model": result.model}
            except Exception as exc:
                return {"status": "error", "error": str(exc)}

        task = {"app": app, "model_id": model_id, "port": port}
        th = threading.Thread(target=self._serve, args=(app, port), daemon=True)
        th.start()
        self._deployments[f"{model_id}:{port}"] = ServingDeployment(model_id=model_id, port=port, process=th)
        return {"status": "started", "model_id": model_id, "port": port, "endpoint": f"http://127.0.0.1:{port}/generate"}

    @staticmethod
    def _serve(app: Any, port: int) -> None:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")

    def stop(self, model_id: str, port: int) -> Dict[str, Any]:
        key = f"{model_id}:{port}"
        dep = self._deployments.pop(key, None)
        if dep is None:
            return {"status": "not_found"}
        return {"status": "stopped", "model_id": model_id, "port": port}

    def list_deployments(self) -> Dict[str, Dict[str, Any]]:
        out: Dict[str, Dict[str, Any]] = {}
        for key, dep in self._deployments.items():
            out[key] = {"model_id": dep.model_id, "port": dep.port, "status": dep.status}
        return out
