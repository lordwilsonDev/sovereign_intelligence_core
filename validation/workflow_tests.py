from __future__ import annotations

import time
from typing import Any, Dict, List

from validation.endpoint_registry import EndpointProbe, endpoint_registry
from validation.sovereign_validator import SovereignValidationResult


def _probe(base_url: str, probe: EndpointProbe, session: Any) -> Dict[str, Any]:
    url = base_url.rstrip("/") + probe.path
    start = time.time()
    try:
        if probe.method == "GET":
            resp = session.get(url, timeout=probe.timeout_s)
        else:
            resp = session.post(url, json=probe.body or {}, timeout=probe.timeout_s)
        latency_ms = round((time.time() - start) * 1000, 2)
        payload = {}
        try:
            payload = resp.json() or {}
        except Exception:
            payload = {"raw": resp.text}
        ok = resp.status_code == probe.expect_status and all(k in payload for k in probe.expect_keys)
        return {
            "path": probe.path,
            "method": probe.method,
            "status": resp.status_code,
            "latency_ms": latency_ms,
            "ok": ok,
            "missing": [k for k in probe.expect_keys if k not in payload],
        }
    except Exception as exc:
        return {
            "path": probe.path,
            "method": probe.method,
            "status": None,
            "latency_ms": round((time.time() - start) * 1000, 2),
            "ok": False,
            "error": str(exc),
        }


def run_workflow_tests(base_url: str = "http://127.0.0.1:8766") -> Dict[str, Any]:
    try:
        import requests as _requests
        session = _requests.Session()
    except Exception:
        return {"ok": False, "error": "requests not available", "results": []}

    result = SovereignValidationResult()
    for probe in endpoint_registry:
        outcome = _probe(base_url, probe, session)
        label = f"{probe.method} {probe.path}"
        if outcome.get("ok"):
            result.passed.append(label)
        else:
            result.failed.append(outcome)

    result.score = round(len(result.passed) / max(1, len(endpoint_registry)) * 100, 2)
    return result.to_dict()
