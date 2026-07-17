from __future__ import annotations

import urllib.request
import urllib.error


_BASE = "http://127.0.0.1:8766"


def _post(path: str, payload: dict) -> dict:
    data = __import__("json").dumps(payload).encode()
    req = urllib.request.Request(f"{_BASE}{path}", data=data, headers={"content-type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return __import__("json").loads(resp.read())


def _get(path: str) -> dict:
    with urllib.request.urlopen(f"{_BASE}{path}", timeout=30) as resp:
        return __import__("json").loads(resp.read())


def test_evolution_live_flow() -> None:
    body = _post("/evolution/scan", {})
    assert "hotspots" in body
    assert "duplication" in body

    propose = _post("/evolution/propose", {
        "proposal_id": "ev-live-1",
        "title": "tighten probe scope",
        "affected_modules": ["msb_v2/evolution/scanner.py"],
        "rationale": "reduce speculative fan-out",
    })
    assert propose["proposal_id"] == "ev-live-1"

    sim_dry = _post("/evolution/simulate", {"proposal_id": "ev-live-1", "dry_run": True})
    assert sim_dry["passed"] is True
    assert sim_dry["failure_reason"] is None

    sim_hard = _post("/evolution/simulate", {"proposal_id": "ev-live-1"})
    assert "passed" in sim_hard
    assert "failure_reason" in sim_hard

    proposals = _get("/evolution/proposals")
    assert any(p["proposal_id"] == "ev-live-1" for p in proposals["proposals"])
