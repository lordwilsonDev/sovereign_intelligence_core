from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from msb_v2.evolution.proposal import EvolutionProposal


@dataclass(frozen=True)
class SimulationResult:
    proposal_id: str
    passed: bool
    regression_tests: int
    capability_parity: bool
    failure_reason: Optional[str]
    ts: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class EvolutionSimulator:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def simulate(self, proposal: EvolutionProposal, pytest_targets: Optional[List[str]] = None) -> SimulationResult:
        modes = ["test", "lint", "type"]
        results = {}
        for mode in modes:
            results[mode] = self._run_checks(proposal, mode, pytest_targets or [])
        passed = all(v.get("ok", False) for v in results.values())
        failure_reason = None
        if not passed:
            failure_reason = next((k for k, v in results.items() if not v.get("ok", False)), "unknown")
        return SimulationResult(
            proposal_id=proposal.proposal_id,
            passed=passed,
            regression_tests=results.get("test", {}).get("tests", 0),
            capability_parity=results.get("test", {}).get("ok", False),
            failure_reason=failure_reason,
        )

    def _run_checks(self, proposal: EvolutionProposal, mode: str, targets: List[str]) -> Dict[str, Any]:
        if mode == "test":
            cmd = ["pytest", "-q"] + targets
            label = "regression"
        elif mode == "lint":
            cmd = ["python3", "-m", "ruff", "check"] + targets
            label = "ruff"
        else:
            cmd = ["python3", "-m", "mypy"] + targets
            label = "mypy"
        try:
            proc = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True, timeout=120)
            ok = proc.returncode == 0
            return {"ok": ok, "mode": mode, "label": label, "returncode": proc.returncode, "stdout": proc.stdout[-2000:], "stderr": proc.stderr[-2000:]}
        except Exception as exc:
            return {"ok": False, "mode": mode, "label": label, "error": str(exc)}
