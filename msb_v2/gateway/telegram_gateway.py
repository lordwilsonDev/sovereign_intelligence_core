from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import random
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse

from cognitive_compiler.sovereign_autonomy_core import (
    PhysicalSovereigntyAssertion,
    QuarantineInversionAgent,
    SanitizedContextSummary,
)
from msb_v2.agent.sovereign_agent_runtime import AgentProfile, LoveGateway, SovereignAgentRuntime
from msb_v2.v3.contracts import HarnessContract, register as _register_contract

logger = logging.getLogger(__name__)

router = APIRouter()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
NODE_KEY: str = os.getenv("SAR_NODE_KEY", "insecure-dev-key")
EXPECTED_GATEWAY_HASH: str = os.getenv("SAR_GATEWAY_HASH", "").strip()

# ---------------------------------------------------------------------------
# Hardware-rooted invariant stub
# ---------------------------------------------------------------------------
def _current_module_sha256() -> str:
    try:
        path = os.path.realpath(__file__)
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except Exception:
        return ""


def _verify_module_integrity() -> None:
    expected = EXPECTED_GATEWAY_HASH
    if not expected:
        logger.warning("I_NSSI hash not configured; gateway integrity check skipped")
        return
    actual = _current_module_sha256()
    if actual != expected:
        raise RuntimeError(
            "I_NSSI Hardware Veto: gateway bytecode hash mismatch. Node refusing to start."
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _signed_audit_token(event: Dict[str, Any]) -> str:
    payload = dict(event)
    payload.setdefault("iat", int(time.time()))
    raw = json.dumps(payload, sort_keys=True, default=str)
    sig = hmac.new(NODE_KEY.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{raw}.{sig}"


_SAFETY_CRITICAL_PREFIXES = ("/tool", "/execute", "/send", "/transfer", "/publish")


def _is_safety_critical(action: Optional[str]) -> bool:
    if action is None:
        return False
    return action.startswith(_SAFETY_CRITICAL_PREFIXES)


def _classify_action(text: str) -> Optional[str]:
    text = (text or "").strip()
    if not text:
        return None
    if text.startswith("/"):
        return text
    lowered = text.lower()
    if lowered.startswith("send "):
        return "/send"
    if lowered.startswith("transfer "):
        return "/transfer"
    if lowered.startswith("publish "):
        return "/publish"
    return None


# ---------------------------------------------------------------------------
# Core gateway
# ---------------------------------------------------------------------------
class SovereignGatewayBase:
    def __init__(self) -> None:
        _verify_module_integrity()
        self.quarantine = QuarantineInversionAgent()
        self.psa = PhysicalSovereigntyAssertion()
        self.love_gateway = LoveGateway()

    def love_gate(self, message: str) -> SanitizedContextSummary:
        return self.quarantine.apply(source_label="telegram_gateway", payload={"content": message})

    def generate_audit_receipt(self, event: Dict[str, Any]) -> str:
        jitter_ns = random.randint(0, 50_000_000)
        event = dict(event)
        event["jitter_ns"] = jitter_ns
        event["node_key"] = hashlib.sha256(NODE_KEY.encode("utf-8")).hexdigest()[:16]
        return _signed_audit_token(event)


_gateway = SovereignGatewayBase()
_profile = AgentProfile(
    profile_id="telegram:default",
    display_name="Telegram Sovereign Gateway",
    memory_partition="telegram/default",
    tool_allowlist=["reply"],
)
_runtime = SovereignAgentRuntime(profile=_profile, love_gateway=_gateway.love_gateway)


# ---------------------------------------------------------------------------
# Background audit poster
# ---------------------------------------------------------------------------
def _post_audit_record(event: Dict[str, Any], token: str) -> None:
    record = {
        "event": event,
        "token": token,
        "gateway_hash": _current_module_sha256(),
        "posted_at": _now_iso(),
    }
    logger.info("SAC audit record: %s", json.dumps(record, default=str))


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@router.post("/gateway/telegram/webhook")
def telegram_webhook(payload: Dict[str, Any], background_tasks: BackgroundTasks) -> JSONResponse:
    update = payload if isinstance(payload, dict) else {}
    message_text = ""
    msg = ((update or {}).get("message") or {})
    if msg:
        message_text = str((msg.get("text") or "")).strip()

    action = _classify_action(message_text)
    if not message_text:
        return JSONResponse({"ok": True, "receipt_id": None, "status": "noop_200"})

    summary = _gateway.love_gate(message_text)
    risk_level = (
        summary.epistemic_risk.value
        if hasattr(summary.epistemic_risk, "value")
        else str(summary.epistemic_risk)
    )

    if risk_level == "high" and _is_safety_critical(action):
        receipt = {
            "id": str(int(time.time() * 1000)),
            "received_at": _now_iso(),
            "verdict": "veto",
            "epistemic_risk": risk_level,
            "action": action,
            "reason": "I_NSSI veto",
        }
        token = _gateway.generate_audit_receipt(receipt)
        receipt["token"] = token
        background_tasks.add_task(_post_audit_record, receipt, token)
        logger.warning("I_NSSI veto applied: action=%s", action)
        return JSONResponse({"ok": True, "receipt_id": receipt["id"], "status": "veto"})

    accepted = _runtime.submit({"type": "msg", "content": message_text, "action": action})

    receipt = {
        "id": str(int(time.time() * 1000)),
        "received_at": _now_iso(),
        "verdict": "accepted",
        "epistemic_risk": risk_level,
        "action": action,
        "accepted": bool(accepted.get("accepted")),
    }
    token = _gateway.generate_audit_receipt(receipt)
    receipt["token"] = token
    background_tasks.add_task(_post_audit_record, receipt, token)
    return JSONResponse({"ok": True, "receipt_id": receipt["id"], "status": "accepted"})


# HCL contracts
_register_contract(HarnessContract(route="/gateway/telegram/webhook", method="post", allow_anonymous=True))
