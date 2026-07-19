#!/usr/bin/env python3
"""
SHARED COGNITIVE STATE (SCS) v1.0
Structured memory object passed between hybrid harness executions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import time


@dataclass
class HarnessRecord:
    harness: str
    output: Dict[str, Any]
    key_findings: List[str] = field(default_factory=list)
    unresolved_tensions: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


@dataclass
class MoIEPanelState:
    critic_active_theses: List[str] = field(default_factory=list)
    scout_active_hypotheses: List[str] = field(default_factory=list)
    synthesizer_integrations: List[str] = field(default_factory=list)
    open_disputes: List[str] = field(default_factory=list)
    confidence_levels: Dict[str, float] = field(default_factory=dict)


@dataclass
class SharedCognitiveState:
    problem_statement: str
    routing_decision: Dict[str, Any] = field(default_factory=dict)
    harness_history: List[HarnessRecord] = field(default_factory=list)
    moie_state: MoIEPanelState = field(default_factory=MoIEPanelState)
    synthesis_artifacts: Dict[str, Any] = field(default_factory=dict)
    open_assumptions: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    sac: Dict[str, Any] = field(default_factory=dict)

    def add_harness_output(self, harness: str, output: Dict[str, Any]) -> None:
        findings = self._extract_findings(output)
        tensions = self._extract_tensions(output)
        self.harness_history.append(HarnessRecord(
            harness=harness,
            output=output,
            key_findings=findings,
            unresolved_tensions=tensions
        ))

    def update_moie(self, critic: List[str], scout: List[str], synthesizer: List[str], disputes: List[str]) -> None:
        self.moie_state.critic_active_theses = critic
        self.moie_state.scout_active_hypotheses = scout
        self.moie_state.synthesizer_integrations = synthesizer
        self.moie_state.open_disputes = disputes

    def to_prompt_context(self) -> str:
        lines = [f"Problem: {self.problem_statement}", ""]
        if self.routing_decision:
            lines.append(f"Routing: {self.routing_decision.get('primary')} -> {self.routing_decision.get('secondary', 'none')}")
        if self.harness_history:
            lines.append("Prior reasoning:")
            for rec in self.harness_history[-3:]:
                lines.append(f"- {rec.harness}: {rec.key_findings[0] if rec.key_findings else 'output recorded'}")
        if self.open_assumptions:
            lines.append("Open assumptions: " + "; ".join(self.open_assumptions[-5:]))
        return "\n".join(lines)

    def _extract_findings(self, output: Dict[str, Any]) -> List[str]:
        candidates = []
        for key in ["next_actions", "immediate_next_action", "plan", "hypotheses"]:
            val = output.get(key)
            if isinstance(val, list):
                candidates.extend([str(v) for v in val[:3]])
            elif isinstance(val, str):
                candidates.append(val)
        return candidates[:5] or ["No explicit findings"]

    def _extract_tensions(self, output: Dict[str, Any]) -> List[str]:
        risks = output.get("risks", [])
        if isinstance(risks, list):
            return [r.get("description", str(r)) for r in risks[:5] if isinstance(r, dict)]
        return []
