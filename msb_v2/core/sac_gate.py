"""Shared SAC readiness / status gate for all harnesses."""

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
