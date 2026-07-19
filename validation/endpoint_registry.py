from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EndpointProbe:
    path: str
    method: str = "GET"
    body: Optional[Dict[str, Any]] = None
    expect_status: int = 200
    expect_keys: List[str] = field(default_factory=list)
    timeout_s: float = 5.0


endpoint_registry = [
    EndpointProbe("/health", "GET", expect_keys=["status"]),
    EndpointProbe("/v3/health", "GET", expect_keys=["status"]),
    EndpointProbe("/meta/health", "GET", expect_keys=["status", "module"]),
    EndpointProbe("/desktop/health", "GET", expect_keys=["status", "module"]),
    EndpointProbe("/career/health", "GET", expect_keys=["ok"], expect_status=200),
    EndpointProbe("/memory/health", "GET", expect_keys=["verified_facts"]),
    EndpointProbe("/verification/benchmarks", "GET", expect_keys=[]),
    EndpointProbe("/evolution/proposals", "GET", expect_keys=[]),
    EndpointProbe("/agent/queue", "POST", body={"query":"ping","goal":"health"}, expect_keys=[]),
    EndpointProbe("/verification/evaluate", "POST", body={"query":"ping","answer":"ok"}, expect_keys=[]),
]
