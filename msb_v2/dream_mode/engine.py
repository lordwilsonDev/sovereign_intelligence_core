"""Dream Mode — periodic speculative synthesis and self-simulation."""
from __future__ import annotations

import hashlib
import json
import random
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DreamScenario:
    scenario_id: str
    prompt: str
    branches: List[Dict[str, Any]]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    outcome: Optional[Dict[str, Any]] = None


class DreamMode:
    """Generates speculative scenarios, runs simulations, and stores dreams."""

    def __init__(self, dreams_path: Optional[Path] = None):
        self.dreams_path = dreams_path or Path(__file__).resolve().parent.parent.parent / "runtime" / "dreams.jsonl"
        self.dreams_path.parent.mkdir(parents=True, exist_ok=True)
        self.prompts = [
            "What would the organism do if external inference APIs failed?",
            "How would the mesh recover if half the peers went offline?",
            "What fact is the system avoiding that could destabilize current assumptions?",
            "If the SAC limit were breached, what would the recovery path look like?",
            "What unseen dependency could break the current metabolic loop?",
        ]

    def generate_scenario(self) -> DreamScenario:
        scenario_id = hashlib.sha256(f"{time.time()}".encode()).hexdigest()[:12]
        prompt = random.choice(self.prompts)
        branches = []
        for i in range(3):
            branches.append({
                "id": f"branch-{i+1}",
                "hypothesis": f"{prompt} Scenario {i+1}: {'maintain' if i == 0 else 'adapt'} with {'low' if i < 2 else 'high'} risk.",
                "risk": "LOW" if i < 2 else "MEDIUM",
            })
        return DreamScenario(scenario_id=scenario_id, prompt=prompt, branches=branches)

    def simulate(self, scenario: DreamScenario) -> Dict[str, Any]:
        """Run a lightweight simulation and record outcome."""
        outcome = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "survival_score": random.randint(70, 99),
            "instability_triggers": random.randint(0, 2),
            "recommended_action": random.choice(["maintain", "monitor", "adapt", "quarantine"]),
        }
        scenario.outcome = outcome
        self._store(scenario)
        return self._to_dict(scenario)

    def run_dream_cycle(self) -> Dict[str, Any]:
        """Generate and simulate a single dream scenario."""
        scenario = self.generate_scenario()
        return self.simulate(scenario)

    def _store(self, scenario: DreamScenario) -> None:
        with open(self.dreams_path, "a") as f:
            f.write(json.dumps(self._to_dict(scenario)) + "\n")

    def _to_dict(self, scenario: DreamScenario) -> Dict[str, Any]:
        return {
            "scenario_id": scenario.scenario_id,
            "prompt": scenario.prompt,
            "branches": scenario.branches,
            "created_at": scenario.created_at,
            "outcome": scenario.outcome,
        }

    def recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        if not self.dreams_path.exists():
            return []
        lines = self.dreams_path.read_text().strip().splitlines()[-limit:]
        return [json.loads(line) for line in lines if line.strip()]
