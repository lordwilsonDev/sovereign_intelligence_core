from __future__ import annotations

from typing import Any, Dict, List, Sequence

from msb_v2.engine.rcoh_persistence import RCOHPersistence
from msb_v2.engine.observability import span


class Crystallizer:
    """Turn validated judgment into immediate/near-term/sustained steps."""

    def __init__(self, persistence: RCOHPersistence | None = None) -> None:
        self._persistence = persistence

    @span("crystallizer.crystallize")
    def crystallize(self, judgment: Dict[str, Any]) -> Dict[str, Any]:
        validated = judgment.get("validated", [])
        potential = judgment.get("breakthrough_potential", "low")
        consensus = judgment.get("consensus_statement", "")
        artifact: Dict[str, Any] = {
            "immediate_steps": self._immediate(validated, potential),
            "near_term_steps": self._near_term(validated, potential),
            "sustained_steps": self._sustained(validated, potential),
            "deepening_question": self._deepening(consensus),
        }
        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{judgment['query'][:50]}/crystallization", artifact)
        return artifact

    @staticmethod
    def _immediate(validated: Sequence[str], potential: str) -> List[str]:
        if not validated:
            return ["Run one falsification experiment on top-ranked claim."]
        return [
            f"Lock claim {validated[0]} and draft one-page operational definition.",
            "Schedule a 24-hour review with the smallest possible stakeholder group.",
        ]

    @staticmethod
    def _near_term(validated: Sequence[str], potential: str) -> List[str]:
        return [
            f"Build a minimal artifact for {len(validated)} validated claim(s): a checklist, template, or detector.",
            "Collect 3 real adverse cases to confirm the inversion survives contact with reality.",
        ]

    @staticmethod
    def _sustained(validated: Sequence[str], potential: str) -> List[str]:
        return [
            "Schedule periodic re-reviews as conditions change.",
            "Document exceptions and edge cases in a local ledger.",
        ]

    @staticmethod
    def _deepening(consensus: str) -> str:
        if not consensus:
            return "What is the simplest observable that would falsify the top unvalidated claim?"
        return "What boundary condition would reverse this consensus in one specific system?"
