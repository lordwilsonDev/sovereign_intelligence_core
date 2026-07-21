from __future__ import annotations

from typing import Any, Dict

from msb_v2.v3.contracts import HarnessContract


class ProviderContract(HarnessContract):
    def __init__(self) -> None:
        super().__init__(route="/provider/interface", method="get", allow_anonymous=True, max_body_bytes=65536)
        self.io = _ProviderIOContract()
        self.guarantees = [
            "provider_trusted",
            "veto_path",
            "coherence_score",
            "jitter_bounded",
        ]


class _ProviderIOContract:
    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "prompt": {"type": "string"},
            "messages": {"type": "array"},
        },
        "required": ["prompt"],
    }
    output_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "response": {"type": "string"},
            "metadata": {"type": "object"},
        },
        "required": ["response"],
    }


ProviderIOContract = _ProviderIOContract
