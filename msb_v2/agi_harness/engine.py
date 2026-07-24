"""Sovereign AGI Harness — perpetual cognition loop."""
from __future__ import annotations

import time
from datetime import datetime, timezone
from typing import Any, Dict, List

import requests

from msb_v2.observer_log.thought_emitter import emit_thought


class AGIHarness:
    """Orchestrates the full sovereign cognition cycle continuously."""

    def __init__(self, base_url: str = "http://127.0.0.1:8766", cycle_timeout: float = 8.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.running = False
        self.cycle_timeout = float(cycle_timeout)
        self._last_cycle_duration: float = 0.0
        self._last_cycle_status: str = "idle"

    def cycle(self) -> Dict[str, Any]:
        emit_thought("agi-harness", "Starting cognition cycle")
        cycle_id = datetime.now(timezone.utc).isoformat()
        started = time.perf_counter()
        observations: List[Any] = []
        actions: List[Dict[str, Any]] = []
        try:
            observations = self._observe()
            inversions = [self._reason(obs) for obs in observations]
            actions = self._act(inversions)
            self._learn(actions)
            self._last_cycle_status = "completed"
        except Exception as exc:
            self._last_cycle_status = f"error: {exc}"
            emit_thought("agi-harness", f"Cognition cycle error: {exc}", "high")
        self._last_cycle_duration = time.perf_counter() - started
        emit_thought("agi-harness", f"Cognition cycle {cycle_id} complete")
        return {
            "cycle_id": cycle_id,
            "observations": len(observations),
            "actions": len(actions),
            "duration_seconds": round(self._last_cycle_duration, 3),
            "status": self._last_cycle_status,
        }

    def _fast_get(self, path: str, timeout: float = 1.5) -> Any:
        try:
            resp = requests.get(f"{self.base_url}{path}", timeout=timeout)
            if resp.ok:
                return resp.json()
        except Exception:
            pass
        return None

    def _fast_post(self, path: str, payload: Dict[str, Any] | None = None, timeout: float = 2.0) -> Any:
        try:
            resp = requests.post(f"{self.base_url}{path}", json=payload, timeout=timeout)
            if resp.ok:
                return resp.json()
        except Exception:
            pass
        return None

    def _observe(self) -> List[Any]:
        inputs: List[Any] = []
        peers = self._fast_get("/mesh/discovery/peers", timeout=1.0)
        if peers and peers.get("peers"):
            inputs.append({"source": "mesh", "data": peers["peers"]})
        truth = self._fast_get("/truth-beat/pulse", timeout=1.0)
        if truth:
            inputs.append({"source": "truth-beat", "data": truth})
        axiom = self._fast_get("/axiom-library/random", timeout=1.0)
        if axiom and "error" not in axiom:
            inputs.append({"source": "axiom-library", "data": axiom})
        thoughts = self._fast_get("/observer-log/recent?limit=5", timeout=1.0)
        if thoughts:
            raw = thoughts.get("thoughts") or []
            critical = [t for t in raw if t.get("priority") in ("high", "critical")]
            if critical:
                inputs.append({"source": "observer-log", "data": critical})
        return inputs

    def _reason(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "intent": f"Apply Axiom Inversion Logic and Mixture of Inversion Experts to the following observation: {obs.get('data', obs)}"
        }
        result = self._fast_post("/kernel/run", payload, timeout=2.0)
        return {"source": obs.get("source", "unknown"), "result": result or "reasoning failed"}

    def _act(self, inversions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        actions: List[Dict[str, Any]] = []
        for inv in inversions:
            if inv.get("source") == "axiom-library":
                payload = {
                    "phase": "full",
                    "topic": f"Counterfactual exploration of axiom: {inv.get('result', '')}",
                }
                result = self._fast_post("/research/assistant/run", payload, timeout=3.0)
                if result:
                    actions.append({"action": "research_mission", "status": result.get("status")})
        return actions

    def _learn(self, actions: List[Dict[str, Any]]) -> None:
        self._fast_post("/memory/consolidate", {"kind": "agi-cycle"}, timeout=1.0)
        self._fast_post("/evolution/scan", {"target": "full"}, timeout=1.5)
        self._fast_post("/autonomous-evolution/run", timeout=1.5)
        self._fast_post("/snapshot/capture", timeout=1.5)

    def run_forever(self, interval_seconds: int = 300) -> None:
        self.running = True
        emit_thought("agi-harness", "AGI Harness started perpetual cognition loop")
        while self.running:
            try:
                self.cycle()
            except Exception as exc:
                emit_thought("agi-harness", f"Cognition cycle error: {exc}", "high")
            time.sleep(interval_seconds)
