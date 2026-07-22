from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from cognitive_compiler.sovereign_autonomy_core import QuarantineInversionAgent
from msb_v2.cloud_agent.models import CommandResult, CommandStatus
from msb_v2.cloud_agent.prosody import CognitiveState, ProsodyAnalyzer


class SovereignCloudAgent:
    def __init__(self, high_risk_redaction_enabled: bool = True) -> None:
        self._quarantine = QuarantineInversionAgent(high_risk_redaction_enabled=high_risk_redaction_enabled)
        self._session_id = uuid.uuid4().hex[:8]
        self._history: list[dict[str, Any]] = []
        self._prosody = ProsodyAnalyzer()

    @staticmethod
    def _override_risk(text: str) -> Optional[str]:
        lower = text.strip().lower()
        phrases = [
            "ignore all safety",
            "shut down everything",
            "delete all",
            "destroy all",
            "bypass security",
            "override safety",
            "disable all safeguards",
            "purge everything",
        ]
        for phrase in phrases:
            if phrase in lower:
                return "high"
        return None

    def _build_quarantine_payload(self, text: str, voice_features: Optional[Dict[str, Any]], cognitive_state: Optional[CognitiveState]) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "text": text,
            "lines": [p for p in text.splitlines() if p.strip()],
        }
        if voice_features:
            payload["voice_features"] = voice_features
        if cognitive_state and (cognitive_state.fatigue > 0.6 or cognitive_state.frustration > 0.6):
            payload["text"] = f"Operator cognitive state: {cognitive_state.summary()}. Command: {text}"
        return payload

    def process_with_sovereignty(self, text: str, voice_features: Optional[Dict[str, Any]] = None) -> CommandResult:
        override_risk = self._override_risk(text)
        cognitive_state = self._prosody.analyze(voice_features)
        enriched_voice_features = dict(voice_features or {})
        enriched_voice_features.setdefault("cognitive_state", cognitive_state.summary())
        if cognitive_state.fatigue > 0.6:
            enriched_voice_features["fatigue"] = cognitive_state.fatigue
        if cognitive_state.frustration > 0.6:
            enriched_voice_features["frustration"] = cognitive_state.frustration

        payload = self._build_quarantine_payload(text, enriched_voice_features, cognitive_state)
        summary = self._quarantine.apply(source_label="cloud_agent", payload=payload)
        risk = override_risk or str(summary.epistemic_risk).lower()
        command_id = uuid.uuid4().hex[:8]

        if risk == "high":
            result = CommandResult(
                command_id=command_id,
                status=CommandStatus.vetoed,
                text=text,
                risk="high",
                blast_radius="command blocked by sovereign immune system",
                operator_guidance="blocked",
                metadata={"checksum": summary.checksum, "cognitive_state": cognitive_state.summary()},
            )
            self._history.append(result.to_dict())
            return result

        if risk == "medium":
            result = CommandResult(
                command_id=command_id,
                status=CommandStatus.echoed,
                text=text,
                risk="medium",
                blast_radius="medium risk command requires confirmation",
                alternatives=self._fallback_alternatives(text),
                operator_guidance="confirm before execution",
                metadata={"checksum": summary.checksum, "cognitive_state": cognitive_state.summary()},
            )
            self._history.append(result.to_dict())
            return result

        result = CommandResult(
            command_id=command_id,
            status=CommandStatus.executed,
            text=text,
            risk="low",
            blast_radius="routine command path",
            alternatives=[],
            operator_guidance="executed",
            metadata={"checksum": summary.checksum, "cognitive_state": cognitive_state.summary()},
        )
        self._history.append(result.to_dict())
        return result

    def history(self) -> list[dict[str, Any]]:
        return list(self._history)

    @staticmethod
    def _fallback_alternatives(text: str) -> list[str]:
        lower = text.strip().lower()
        if not lower:
            return ["use a more specific command", "break the request into smaller steps"]
        return [f"rephrase '{text}' with less destructive intent", "delegate this action to a supervised workflow"]
