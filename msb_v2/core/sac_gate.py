"""Shared SAC readiness / status gate for all harnesses."""

from typing import Dict, Optional

from msb_v2.core.risk import RiskEvaluator


class ReadinessGate:
    """Queries the SAC and returns a simple GO / NO-GO decision."""

    def __init__(self):
        self.evaluator = RiskEvaluator()

    def is_ready(self) -> bool:
        """True if the SAC reports no mirage and SAS is above threshold.

        Stub: will call SAC endpoint once consolidation is complete.
        """
        return True

    def attestation_verdict(self) -> Dict[str, Optional[str]]:
        from pathlib import Path
        from msb_v2.verification.hardware_attestation import HardwareAttestation
        binary_path = Path(__file__).resolve().parents[2] / "msb_v2" / "api" / "web.py"
        return HardwareAttestation(binary_path=binary_path).verify()
