"""Autonomous Evolution Orchestrator — closes the metabolic loop."""
from __future__ import annotations

from typing import Any, Dict

import requests

from msb_v2.evolution.proposal_engine import ProposalEngine
from msb_v2.evolution.shadow_buffer import ShadowBuffer
from msb_v2.observer_log.thought_emitter import emit_thought


class AutonomousEvolution:
    """Proposes, tests, and applies refactorings automatically, with human veto for risky changes."""

    def __init__(self):
        self.proposal_engine = ProposalEngine()
        self.shadow_buffer = ShadowBuffer()

    def run_cycle(self) -> dict:
        """Run one full autonomous evolution cycle."""
        emit_thought("autonomous-evolution", "Starting metabolic cycle")

        # 1. Fetch the top hotspot from the scan
        try:
            scan = requests.post(
                "http://127.0.0.1:8766/evolution/scan",
                json={"target": "full"},
                timeout=10,
            ).json()
            hotspots = scan.get("hotspots", [])
        except Exception:
            return {"status": "scan_failed"}

        if not hotspots:
            emit_thought("autonomous-evolution", "No hotspots found — organism is clean")
            return {"status": "no_hotspots"}

        top = hotspots[0]
        emit_thought(
            "autonomous-evolution",
            f"Top hotspot: {top.get('file')}::{top.get('function')} complexity {top.get('complexity')}",
        )

        # 2. Generate a proposal
        proposal = self.proposal_engine.generate(top)
        if not proposal:
            return {"status": "no_proposal"}

        emit_thought(
            "autonomous-evolution",
            f"Generated proposal {proposal['id']} risk={proposal['risk']}",
        )

        # 3. Test in the shadow buffer
        result = self.shadow_buffer.test_proposal(proposal)

        if result["passed"]:
            emit_thought("autonomous-evolution", f"Proposal {proposal['id']} passed shadow tests")

            summary = self.proposal_engine.summarize(proposal)
            if proposal["risk"] == "LOW":
                # Apply automatically
                self._apply(proposal)
                return {"status": "applied", "proposal": summary}
            else:
                # Request human veto
                emit_thought(
                    "autonomous-evolution",
                    f"Proposal {proposal['id']} needs human approval",
                    "high",
                )
                return {"status": "awaiting_approval", "proposal": summary}
        else:
            emit_thought("autonomous-evolution", f"Proposal {proposal['id']} failed shadow tests", "high")
            return {"status": "shadow_failed", "proposal_id": proposal["id"], "shadow": result}

    def _apply(self, proposal: dict):
        """Apply the proposal to the live codebase."""
        for change in proposal["changes"]:
            target = Path(__file__).resolve().parent.parent.parent / change["file"]
            target.write_text(change["content"])
        emit_thought("autonomous-evolution", f"Applied proposal {proposal['id']}")
