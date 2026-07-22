from __future__ import annotations

import logging
import uuid
from typing import Any, Dict, Optional

from cognitive_compiler.sovereign_autonomy_core import QuarantineInversionAgent

logger = logging.getLogger(__name__)


class EchoDecision:
    def __init__(self) -> None:
        self.decision_id: str = uuid.uuid4().hex[:8]
        self.should_echo: bool = False
        self.reasons: list[str] = []
        self.severity: str = "normal"
        self.echo_message: str = ""
        self.alternatives: list[dict] = []
        self.vetoed: bool = False
        self.raw: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "should_echo": self.should_echo,
            "reasons": self.reasons,
            "severity": self.severity,
            "echo_message": self.echo_message,
            "alternatives": self.alternatives,
            "vetoed": self.vetoed,
            "raw": self.raw,
        }


class SovereignEcho:
    # Echo thresholds
    BLAST_RADIUS_THRESHOLD = 0.5
    FATIGUE_THRESHOLD = 0.6
    FRUSTRATION_THRESHOLD = 0.7
    SPECIFICITY_THRESHOLD = 0.4

    def __init__(self) -> None:
        self.total_commands = 0
        self.echoes_triggered = 0
        self.history: list[dict] = []

    @property
    def echo_rate(self) -> float:
        if self.total_commands == 0:
            return 0.0
        return self.echoes_triggered / self.total_commands

    def _assess_blast_radius(self, blast_analysis, decision):
        if not blast_analysis:
            return
        score = blast_analysis.get("score", 0)
        if score > self.BLAST_RADIUS_THRESHOLD:
            decision.should_echo = True
            affected = blast_analysis.get("affected", 0)
            total = blast_analysis.get("total", 0)
            decision.reasons.append(f"Blast radius: {affected}/{total} workloads affected")
            if blast_analysis.get("stateful_at_risk", 0) > 0:
                decision.severity = "critical"
                decision.reasons.append(f"{blast_analysis['stateful_at_risk']} stateful services at risk")

    def _assess_destructive_quantifier(self, intent, decision):
        if intent.get("is_destructive") and intent.get("has_universal_quantifier"):
            decision.should_echo = True
            decision.reasons.append("Destructive action with universal scope")
            decision.severity = max(
                decision.severity,
                "elevated",
                key=lambda x: ["normal", "elevated", "critical"].index(x),
            )

    def _assess_irreversible_critical(self, intent, decision):
        if intent.get("is_reversible") is False and intent.get("target_criticality", 0) > 0.7:
            decision.should_echo = True
            decision.reasons.append("Irreversible action on critical target")
            decision.severity = "critical"

    def _assess_low_specificity(self, intent, decision):
        specificity = intent.get("specificity")
        if specificity is not None and specificity < self.SPECIFICITY_THRESHOLD:
            decision.should_echo = True
            decision.reasons.append(f"Low specificity ({specificity:.0%}) — command may be vague")

    def _assess_cognitive_state(self, cognitive_state, decision):
        if not cognitive_state:
            return
        fatigue = float(cognitive_state.get("fatigue", 0))
        frustration = float(cognitive_state.get("frustration", 0))
        if fatigue > self.FATIGUE_THRESHOLD:
            decision.should_echo = True
            decision.reasons.append(f"Operator fatigue detected ({fatigue:.0%})")
        if frustration > self.FRUSTRATION_THRESHOLD:
            decision.should_echo = True
            decision.reasons.append(f"Operator frustration detected ({frustration:.0%})")

    def _assess_temporal_risk(self, temporal_context, decision):
        if not temporal_context:
            return
        mult = temporal_context.get("risk_multiplier", 1.0)
        if mult > 1.5:
            decision.should_echo = True
            decision.reasons.append(f"Elevated temporal risk (x{mult})")

    def _finalize_decision(self, intent, blast_analysis, cognitive_state, decision):
        if decision.should_echo:
            decision.echo_message = _generate_echo(intent, blast_analysis, cognitive_state)
            decision.alternatives = _suggest_alternatives(intent, blast_analysis)
            self.echoes_triggered += 1
        self.history.append({
            "command": intent.get("raw_text", str(intent)),
            "echoed": decision.should_echo,
            "severity": decision.severity,
            "reasons": decision.reasons,
            "timestamp": _utcnow(),
        })
        return decision

    def evaluate(self, intent, blast_analysis=None, cognitive_state=None, temporal_context=None):
        self.total_commands += 1
        decision = EchoDecision()
        decision.raw = {
            "intent": intent,
            "blast_analysis": blast_analysis,
            "cognitive_state": cognitive_state,
            "temporal_context": temporal_context,
        }

        action = intent.get("action")
        if action == "query":
            self.history.append({
                "command": intent.get("raw_text", str(intent)),
                "echoed": False,
                "severity": "normal",
                "reasons": [],
                "timestamp": _utcnow(),
            })
            return decision

        self._assess_blast_radius(blast_analysis, decision)
        self._assess_destructive_quantifier(intent, decision)
        self._assess_irreversible_critical(intent, decision)
        self._assess_low_specificity(intent, decision)
        self._assess_cognitive_state(cognitive_state, decision)
        self._assess_temporal_risk(temporal_context, decision)
        return self._finalize_decision(intent, blast_analysis, cognitive_state, decision)

    def summary(self) -> Dict[str, Any]:
        return {
            "total_commands": self.total_commands,
            "echoes_triggered": self.echoes_triggered,
            "echo_rate": round(self.echo_rate, 4),
        }


def _utcnow() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat()


def _generate_echo(intent: Dict[str, Any], blast_analysis: Optional[Dict[str, Any]], cognitive_state: Optional[Dict[str, Any]]) -> str:
    raw = intent.get("raw_text", "your command")
    parts = [f"I heard: \"{raw}\""]
    if blast_analysis:
        affected = blast_analysis.get("affected", 0)
        stateful = blast_analysis.get("stateful_at_risk", 0)
        client = blast_analysis.get("client_facing_at_risk", 0)
        impact = f"That would affect {affected} workload{'s' if affected != 1 else ''}"
        if stateful > 0:
            impact += f", including {stateful} database{'s' if stateful != 1 else ''}"
        if client > 0:
            impact += f" and {client} client-facing service{'s' if client != 1 else ''}"
        parts.append(impact + ".")
        details = blast_analysis.get("details", [])
        critical = [d.get("name") for d in details if d.get("critical") or d.get("stateful")]
        if critical:
            named = ", ".join(critical[:4])
            if len(critical) > 4:
                named += f", and {len(critical) - 4} more"
            parts.append(f"At risk: {named}.")
    if cognitive_state and float(cognitive_state.get("fatigue", 0)) > 0.6:
        parts.append("(I also notice your voice pattern suggests fatigue.)")
    return " ".join(parts)


def _suggest_alternatives(intent: Dict[str, Any], blast_analysis: Optional[Dict[str, Any]]) -> list[dict]:
    alts: list[dict] = []
    if blast_analysis:
        details = blast_analysis.get("details", [])
        non_critical = [d for d in details if not d.get("critical") and not d.get("stateful")]
        if non_critical:
            names = ", ".join(d.get("name", "") for d in non_critical[:3])
            alts.append({"description": f"Shut down only non-critical: {names}", "affected": len(non_critical), "safe": True})
        if not intent.get("targets"):
            gpus = [d for d in details if d.get("type") == "gpu"]
            if gpus:
                alts.append({"description": f"Target only GPU instances ({len(gpus)} jobs)", "affected": len(gpus), "safe": True})
        for provider in {d.get("provider") for d in details if d.get("provider")}:
            count = sum(1 for d in details if d.get("provider") == provider)
            alts.append({"description": f"Limit to {provider} only ({count} workloads)", "affected": count, "safe": False})
    return alts[:3]


class EchoHarness:
    def __init__(self) -> None:
        self._engine = SovereignEcho()
        self._quarantine = QuarantineInversionAgent()

    def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        intent = payload.get("intent") or {}
        payload.setdefault("text", intent.get("raw_text", ""))
        summary = self._quarantine.apply(source_label="echo_harness", payload=payload)
        decision = self._engine.evaluate(
            intent=intent,
            blast_analysis=payload.get("blast_analysis"),
            cognitive_state=payload.get("cognitive_state"),
            temporal_context=payload.get("temporal_context"),
        )
        decision.raw["quarantine_risk"] = str(summary.epistemic_risk).lower()
        if str(summary.epistemic_risk).lower() == "high":
            decision.vetoed = True
            decision.should_echo = False
            decision.severity = "critical"
            decision.reasons = ["blocked by sovereign immune system"]
            decision.echo_message = "This command is blocked by the Sovereign Immune System."
            decision.alternatives = []
        return decision.to_dict()

    def history(self, limit: int = 50) -> list[dict]:
        return self._engine.history[-max(0, limit):]

    def status(self) -> Dict[str, Any]:
        return {"status": "ok", **self._engine.summary()}
