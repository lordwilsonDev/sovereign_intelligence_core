from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict

from msb_v2.core.evolution_memory import EvolutionMemory
from msb_v2.core.falsification_mirror import FalsificationMirror
from msb_v2.capabilities.runner import run_all

logger = logging.getLogger(__name__)


class GlobalScheduler:
    """Evaluates one proposed change against capability baseline and Evolution Memory."""

    CAP_DIR = Path(__file__).resolve().parent.parent / "capabilities" / "tests"

    def __init__(
        self,
        memory: EvolutionMemory,
        *,
        cap_dir: Path | None = None,
        mirror: FalsificationMirror | None = None,
    ) -> None:
        self.memory = memory
        self.cap_dir = cap_dir or self.CAP_DIR
        self.mirror = mirror or FalsificationMirror(memory)

    def execute_cycle(
        self,
        proposal: Dict[str, Any],
        *,
        mode: str = "simulate",
    ) -> Dict[str, Any]:
        outcomes = {
            "mode": mode,
            "proposal_id": proposal.get("proposal_id"),
            "module": proposal.get("module", ""),
        }

        capability_results = run_all(self.cap_dir)
        outcomes["capability_results"] = capability_results

        mirror_outcome = self.mirror.evaluate_batch(capability_results)
        outcomes["mirror"] = mirror_outcome
        outcomes["reality_coherence_rate"] = mirror_outcome.get("coherence_rate")
        outcomes["falsified_categories"] = [c["category"] for c in mirror_outcome.get("falsified", [])]

        if proposal.get("update_baseline"):
            from msb_v2.capabilities.runner import update_baseline
            update_baseline(capability_results, self.memory)
            outcomes["baseline_updated"] = True

        failed = len(mirror_outcome.get("falsified", [])) > 0
        record_result = "rejected" if failed else "accepted"
        outcomes["decision"] = record_result
        outcomes["accepted"] = not failed

        proposal_id = self.memory.record_proposal(
            proposal=proposal,
            result=record_result,
            reason="FALSIFIED categories: " + ", ".join(outcomes["falsified_categories"]) if failed else "COHERENT",
            lesson="Phase 4 scheduler gating",
            metrics_before=outcomes.get("metrics_before", {}),
            metrics_after=outcomes.get("metrics_after", {}),
        )
        outcomes["recorded_proposal_id"] = proposal_id
        return outcomes
