"""Sovereign AGI Harness — perpetual cognition loop."""
import time
from datetime import datetime, timezone

import requests

from msb_v2.observer_log.thought_emitter import emit_thought


class AGIHarness:
    """Orchestrates the full sovereign cognition cycle continuously."""

    def __init__(self, base_url="http://127.0.0.1:8766"):
        self.base_url = base_url.rstrip("/")
        self.running = False

    def cycle(self) -> dict:
        emit_thought("agi-harness", "Starting cognition cycle")
        cycle_id = datetime.now(timezone.utc).isoformat()
        observations = self._observe()
        inversions = [self._reason(obs) for obs in observations]
        actions = self._act(inversions)
        self._learn(actions)
        emit_thought("agi-harness", f"Cognition cycle {cycle_id} complete")
        return {"cycle_id": cycle_id, "observations": len(observations), "actions": len(actions)}

    def _observe(self):
        inputs = []
        try:
            resp = requests.get(f"{self.base_url}/mesh/discovery/peers", timeout=3)
            if resp.ok:
                data = resp.json()
                if data.get("peers"):
                    inputs.append({"source": "mesh", "data": data["peers"]})
        except Exception:
            pass
        try:
            resp = requests.get(f"{self.base_url}/truth-beat/pulse", timeout=3)
            if resp.ok:
                inputs.append({"source": "truth-beat", "data": resp.json()})
        except Exception:
            pass
        try:
            resp = requests.get(f"{self.base_url}/axiom-library/random", timeout=3)
            if resp.ok:
                data = resp.json()
                if "error" not in data:
                    inputs.append({"source": "axiom-library", "data": data})
        except Exception:
            pass
        try:
            resp = requests.get(f"{self.base_url}/observer-log/recent?limit=5", timeout=3)
            if resp.ok:
                thoughts = resp.json().get("thoughts", [])
                critical = [t for t in thoughts if t.get("priority") in ("high", "critical")]
                if critical:
                    inputs.append({"source": "observer-log", "data": critical})
        except Exception:
            pass
        return inputs

    def _reason(self, obs):
        try:
            resp = requests.post(
                f"{self.base_url}/kernel/run",
                json={"intent": f"Apply Axiom Inversion Logic and Mixture of Inversion Experts to the following observation: {obs.get('data', obs)}"},
                timeout=15,
            )
            if resp.ok:
                return {"source": obs["source"], "result": resp.json()}
        except Exception:
            pass
        return {"source": obs["source"], "result": "reasoning failed"}

    def _act(self, inversions):
        actions = []
        for inv in inversions:
            if inv.get("source") == "axiom-library":
                try:
                    resp = requests.post(
                        f"{self.base_url}/research/assistant/run",
                        json={"phase": "full", "topic": f"Counterfactual exploration of axiom: {inv.get('result', '')}"},
                        timeout=15,
                    )
                    if resp.ok:
                        actions.append({"action": "research_mission", "status": resp.json().get("status")})
                except Exception:
                    pass
        return actions

    def _learn(self, actions):
        try:
            requests.post(f"{self.base_url}/memory/consolidate", json={"kind": "agi-cycle"}, timeout=5)
        except Exception:
            pass
        try:
            requests.post(f"{self.base_url}/evolution/scan", json={"target": "full"}, timeout=10)
        except Exception:
            pass
        try:
            requests.post(f"{self.base_url}/autonomous-evolution/run", timeout=10)
        except Exception:
            pass
        try:
            requests.post(f"{self.base_url}/snapshot/capture", timeout=10)
        except Exception:
            pass

    def run_forever(self, interval_seconds: int = 300):
        self.running = True
        emit_thought("agi-harness", "AGI Harness started perpetual cognition loop")
        while self.running:
            try:
                self.cycle()
            except Exception as e:
                emit_thought("agi-harness", f"Cognition cycle error: {e}", "high")
            time.sleep(interval_seconds)
