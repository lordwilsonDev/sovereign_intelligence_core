from __future__ import annotations

from typing import Any, Dict


class ProviderIOContract:
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


class ProviderContract:
    def __init__(self) -> None:
        self.io = ProviderIOContract()
        self.guarantees = [
            "provider_trusted",
            "veto_path",
            "coherence_score",
            "jitter_bounded",
        ]
