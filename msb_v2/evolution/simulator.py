from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
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
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z")


class EvolutionSimulator:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root

    def simulate(self, proposal: EvolutionProposal, pytest_targets: Optional[List[str]] = None) -> SimulationResult:
        if getattr(proposal, "dry_run", False):
            return SimulationResult(
                proposal_id=proposal.proposal_id,
                passed=True,
                regression_tests=0,
                capability_parity=True,
                failure_reason=None,
            )
        if not pytest_targets:
            return SimulationResult(
                proposal_id=proposal.proposal_id,
                passed=False,
                regression_tests=0,
                capability_parity=False,
                failure_reason="missing targets",
            )
        results = {
            "test": self._run_pytest(proposal, pytest_targets),
            "lint": self._run_lint(proposal, pytest_targets),
            "type": self._run_type(proposal, pytest_targets),
        }
        passed = all(v.get("ok", False) for v in results.values())
        failure_reason = None if passed else next((k for k, v in results.items() if not v.get("ok", False)), "unknown")
        return SimulationResult(
            proposal_id=proposal.proposal_id,
            passed=passed,
            regression_tests=results.get("test", {}).get("tests", 0),
            capability_parity=results.get("test", {}).get("ok", False),
            failure_reason=failure_reason,
        )

    def _run_pytest(self, proposal: EvolutionProposal, targets: List[str]) -> Dict[str, Any]:
        cmd = ["pytest", "-q"] + targets
        return self._run(cmd, proposal, label="regression")

    def _run_lint(self, proposal: EvolutionProposal, targets: List[str]) -> Dict[str, Any]:
        cmd = ["python3", "-m", "ruff", "check"] + targets
        return self._run(cmd, proposal, label="ruff")

    def _run_type(self, proposal: EvolutionProposal, targets: List[str]) -> Dict[str, Any]:
        cmd = ["python3", "-m", "mypy"] + targets
        return self._run(cmd, proposal, label="mypy")

    def _run(self, cmd: List[str], proposal: EvolutionProposal, label: str) -> Dict[str, Any]:
        try:
            proc = subprocess.run(cmd, cwd=self.repo_root, capture_output=True, text=True, timeout=120)
            ok = proc.returncode == 0
            return {"ok": ok, "mode": label, "label": label, "returncode": proc.returncode, "stdout": proc.stdout[-2000:], "stderr": proc.stderr[-2000:]}
        except Exception as exc:
            return {"ok": False, "mode": label, "label": label, "error": str(exc)}
