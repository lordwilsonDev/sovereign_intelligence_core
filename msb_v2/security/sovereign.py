from __future__ import annotations

from dataclasses import dataclass, field

from msb_v2.engine.execution_policy import CapabilityBoundary


@dataclass(frozen=True)
class SovereignProfile:
    capability: CapabilityBoundary = field(default_factory=lambda: CapabilityBoundary(allow_exec=False, max_dangerous_per_min=2))
    airgap: bool = True
    telemetry_opt_out: bool = True
    identity_role: str = "default"
    pubkey_hex: str = ""


_DEFAULT = SovereignProfile()


def get_sovereign_profile() -> SovereignProfile:
    return _DEFAULT
