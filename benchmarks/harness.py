from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class BenchmarkCase:
    name: str
    prompt: str
    expected_keys: List[str] = field(default_factory=list)
    max_tokens: int = 256
    temperature: float = 0.0


@dataclass
class BenchmarkResult:
    model: str
    case: str
    latency_ms: float
    tokens_used: int
    text: str
    passed: bool
    missing_keys: List[str] = field(default_factory=list)


class BenchmarkHarness:
    def __init__(self, cases: List[BenchmarkCase], provider: str = "ollama") -> None:
        self.cases = cases
        self.provider = provider
        self.results: List[BenchmarkResult] = []

    def run_model(self, model: str) -> List[BenchmarkResult]:
        results: List[BenchmarkResult] = []
        for case in self.cases:
            start = time.perf_counter()
            try:
                if self.provider == "ollama":
                    payload = {
                        "model": model,
                        "prompt": case.prompt,
                        "stream": False,
                        "options": {"num_predict": case.max_tokens, "temperature": case.temperature, "num_ctx": 4096, "top_k": 32, "top_p": 0.9},
                    }
                    import urllib.request
                    req = urllib.request.Request(
                        "http://127.0.0.1:11434/api/generate",
                        data=__import__("json").dumps(payload).encode(),
                        headers={"content-type": "application/json"},
                        method="POST",
                    )
                    with urllib.request.urlopen(req, timeout=120) as resp:
                        data = __import__("json").loads(resp.read().decode())
                    text = str(data.get("response", ""))
                    tokens = int(data.get("eval_count", 0))
                else:
                    raise ValueError("unsupported provider")
            except Exception as exc:
                text = ""
                tokens = 0
                latency_ms = (time.perf_counter() - start) * 1000.0
                results.append(BenchmarkResult(model=model, case=case.name, latency_ms=latency_ms, tokens_used=0, text="", passed=False, missing_keys=[str(exc)]))
                continue
            latency_ms = (time.perf_counter() - start) * 1000.0
            missing = []
            if case.expected_keys:
                lower = text.lower()
                for key in case.expected_keys:
                    if key.lower() not in lower:
                        missing.append(key)
            passed = len(missing) == 0
            results.append(BenchmarkResult(model=model, case=case.name, latency_ms=latency_ms, tokens_used=tokens, text=text, passed=passed, missing_keys=missing))
        self.results.extend(results)
        return results

    def summary(self) -> Dict[str, Any]:
        if not self.results:
            return {"models": [], "cases": []}
        by_model: Dict[str, List[BenchmarkResult]] = {}
        for r in self.results:
            by_model.setdefault(r.model, []).append(r)
        models = []
        for model, rows in by_model.items():
            passed = sum(1 for r in rows if r.passed)
            avg_latency = sum(r.latency_ms for r in rows) / len(rows)
            avg_tokens = sum(r.tokens_used for r in rows) / len(rows)
            models.append({"model": model, "passed": passed, "cases": len(rows), "avg_latency_ms": round(avg_latency, 2), "avg_tokens": round(avg_tokens, 2)})
        return {"models": models, "cases": [c.name for c in self.cases]}
