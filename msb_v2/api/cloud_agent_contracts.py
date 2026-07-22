from __future__ import annotations

from typing import Any, Dict

from msb_v2.v3.contracts import HarnessContract, register as _register_contract
from msb_v2.api.cloud_agent import router as cloud_agent_router
from msb_v2.api.systems_health import router as systems_health_router

_register_contract(HarnessContract(route="/cloud-agent/command", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/cloud-agent/confirm", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/cloud-agent/history", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/cloud-agent/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/systems-health/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/systems-health/check", method="post", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/systems-health/history", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/systems-health/processes", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/systems-health/repair", method="post", allow_anonymous=False, max_body_bytes=65536))
