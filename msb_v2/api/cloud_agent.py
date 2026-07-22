from __future__ import annotations

import logging
import traceback
from typing import Any, Dict

from fastapi import APIRouter

from msb_v2.cloud_agent.models import CommandResult
from msb_v2.cloud_agent.prosody import VoiceprintStore
from msb_v2.cloud_agent.sovereign_agent import SovereignCloudAgent

router = APIRouter()
_agent = SovereignCloudAgent()
_store = VoiceprintStore()
_logger = logging.getLogger(__name__)


def _notify_snh(result: CommandResult) -> None:
    if result.status.value == "vetoed":
        template = "cloud_agent_vetoed"
        priority = "high"
    else:
        template = "cloud_agent_echoed"
        priority = "medium"
    data = {
        "source": "cloud-agent",
        "priority": priority,
        "template": template,
        "template_data": {
            "command_id": result.command_id,
            "text": result.text,
            "risk": result.risk,
            "blast_radius": result.blast_radius,
            "alternatives": result.alternatives,
        },
    }
    try:
        from msb_v2.sn.engine import NotificationEngine
        from msb_v2.sn.models import NotificationRequest
        engine = NotificationEngine()
        engine.notify(NotificationRequest(**data))
    except Exception as exc:  # pragma: no cover - defensive notify failure
        _logger.error("SN notify failed: `%s`\n%s", exc, traceback.format_exc())


def _audit_command_event(event: str, payload: dict) -> None:
    try:
        from msb_v2.audit.audit_engine import AuditEngine
        from msb_v2.audit.events import AuditEvent
        engine = AuditEngine()
        engine.record(AuditEvent(workflow="cloud_agent", event_type=event, status="succeeded", metadata=payload))
    except Exception as exc:  # pragma: no cover - defensive audit failure
        _logger.error("Audit event recording failed: `%s`\n%s", exc, traceback.format_exc())


@router.post("/command")
def command(request: Dict[str, Any]) -> Dict[str, Any]:
    text = str(request.get("text", "")).strip()
    voice_features = request.get("voice_features")
    result = _agent.process_with_sovereignty(text, voice_features=voice_features)
    payload: Dict[str, Any] = result.to_dict()
    if result.status.value in {"echoed", "vetoed"}:
        try:
            _notify_snh(result)
        except Exception as exc:
            _logger.error("Command notify failure: `%s`\n%s", exc, traceback.format_exc())
    _audit_command_event("CLOUD_AGENT_COMMAND", {"text": text, "result": payload})
    return payload


@router.post("/confirm")
def confirm(payload: Dict[str, Any]) -> Dict[str, Any]:
    command_id = str(payload.get("command_id", "")).strip()
    confirmation = str(payload.get("confirmation", "")).strip().lower()
    history = _agent.history()
    match = next((item for item in reversed(history) if item.get("command_id") == command_id), None)
    if not match:
        _audit_command_event("CLOUD_AGENT_CONFIRM", {"command_id": command_id, "status": "not_found"})
        return {"status": "not_found"}
    if confirmation != "yes":
        _audit_command_event("CLOUD_AGENT_CONFIRM", {"command_id": command_id, "status": "cancelled"})
        return {"status": "cancelled", "command_id": command_id}
    response = {"status": "confirmed", "command_id": command_id, "previous": match}
    _audit_command_event("CLOUD_AGENT_CONFIRM", {"command_id": command_id, "status": "confirmed"})
    return response


@router.get("/history")
def history(limit: int = 50) -> Dict[str, Any]:
    items = _agent.history()
    return {"items": items[-max(0, limit):], "count": len(items)}


@router.get("/status")
def status() -> Dict[str, Any]:
    history = _agent.history()
    return {"active": True, "history_count": len(history)}


@router.get("/voiceprint/baseline")
def voiceprint_baseline() -> Dict[str, Any]:
    return _store.baseline()


@router.post("/voiceprint/calibrate")
def voiceprint_calibrate(payload: Dict[str, Any]) -> Dict[str, Any]:
    samples = payload.get("samples") or []
    if not isinstance(samples, list):
        samples = []
    baseline = _store.update(samples)
    return {"status": "calibrated", "baseline": baseline}


@router.post("/voiceprint/reset")
def voiceprint_reset() -> Dict[str, Any]:
    baseline = _store.reset()
    return {"status": "reset", "baseline": baseline}
