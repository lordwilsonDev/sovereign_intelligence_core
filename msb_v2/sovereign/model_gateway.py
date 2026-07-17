from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class ModelCapabilityEvent:
    module: str
    tool: str
    status: str
    detail: str = ""


class ModelGateway:
    """Compatibility shim for level33_sovereign model access."""

    def __init__(self, *, strict: bool = False) -> None:
        self.strict = strict
        self._available = False
        self._last_error = "model backend not configured"

    def configure(self, backend: str = "stub", **kwargs: Any) -> None:
        if backend == "ollama":
            self._available = False
            self._last_error = "ollama backend is disabled in this integration"
        else:
            self._available = True
            self._last_error = ""

    def available(self) -> bool:
        return self._available

    def last_error(self) -> str:
        return self._last_error

    def emit_capability_event(self, module: str, tool: str, status: str = "skipped", detail: str = "") -> ModelCapabilityEvent:
        return ModelCapabilityEvent(module=module, tool=tool, status=status, detail=detail)

    def query(self, prompt: str, system_prompt: Optional[str] = None, **_: Any) -> str:
        if not self._available:
            if self.strict:
                raise RuntimeError(f"Model backend unavailable: {self._last_error}")
            return ""
        return ""
