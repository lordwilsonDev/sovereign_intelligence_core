from __future__ import annotations

from msb_v2.v3.constraints import ConstraintEngine
from msb_v2.v3.inversion_registry import get_registry as _get_inversion_registry
from msb_v2.v3.memory_router import MemoryRouter
from msb_v2.v3.registry import get_registry as _get_capability_registry


class BootstrapV3:
    def __init__(self) -> None:
        self.capabilities = _get_capability_registry()
        self.memory_router = MemoryRouter()
        self.constraint_engine = ConstraintEngine()
        self.inversion_registry = _get_inversion_registry()

    def summary(self) -> dict:
        return {
            "capabilities": self.capabilities.summary(),
            "memory": self.memory_router.summary(),
            "constraints": self.constraint_engine.summary(),
            "inversion": self.inversion_registry.summary(),
        }


_bootstrap: BootstrapV3 | None = None


def bootstrap_v3() -> BootstrapV3:
    global _bootstrap
    if _bootstrap is None:
        _bootstrap = BootstrapV3()
    return _bootstrap
