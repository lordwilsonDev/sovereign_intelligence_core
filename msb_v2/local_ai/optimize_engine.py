from __future__ import annotations

import hashlib
import os
import time
import urllib.request
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from .inference_engine import InferenceEngine


@dataclass(frozen=True)
class BenchmarkResult:
    model: str
    latency_ms: float
    tokens_per_sec: float
    backend: str
    device: str = "cpu/ollama"


class OptimizeEngine:
    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url or "http://127.0.0.1:11434"
        self.prompt = "Count from 1 to 10."

    def benchmark(self, model_id: str, iterations: int = 1) -> BenchmarkResult:
        engine = InferenceEngine(base_url=self.base_url)
        start = time.perf_counter()
        result = engine.generate(model_id=model_id, prompt=self.prompt, max_tokens=64, temperature=0.0)
        end = time.perf_counter()
        latency_ms = (end - start) * 1000
        tokens = max(len(result.text.split()), 1)
        tps = tokens / ((end - start) if (end - start) > 0 else 1e-6)
        output_path = self._audit_dir() / f"benchmark-{hashlib.sha256(model_id.encode()).hexdigest()}.json"
        output_path.write_text(json.dumps({
            "model": model_id,
            "latency_ms": latency_ms,
            "tokens_per_sec": tps,
            "text": result.text,
            "backend": result.backend,
        }, indent=2))
        return BenchmarkResult(model=model_id, latency_ms=latency_ms, tokens_per_sec=tps, backend="ollama")

    def optimize(self, model_id: str) -> Dict[str, Any]:
        bench = self.benchmark(model_id)
        suggestions = {"model": model_id, "backend": "ollama"}
        if bench.latency_ms > 2000:
            suggestions["hint"] = "Consider smaller model or reduced max_tokens for low-latency paths."
        else:
            suggestions["hint"] = "Current settings suitable for interactive use."
        return suggestions

    @staticmethod
    def _audit_dir() -> Path:
        return Path(os.environ.get("MSB_AUDIT_DIR") or "/tmp/msb-local-audit")
