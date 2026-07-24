"""Shadow Buffer — sandboxed refactoring with golden-test verification."""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional


class ShadowBuffer:
    """Applies a proposed change in a sandbox, runs tests, and returns results."""

    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path(__file__).resolve().parent.parent.parent

    def test_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Apply the proposal in a temporary copy and run the test suite."""
        proposal_id = proposal.get("id", "unknown")
        temp_dir = Path(tempfile.mkdtemp(prefix="msb-shadow-"))
        try:
            # Copy the repository into the sandbox
            shutil.copytree(
                self.repo_path,
                temp_dir / "repo",
                symlinks=True,
                ignore_dangling_symlinks=True,
                ignore=shutil.ignore_patterns(
                    ".git", "__pycache__", ".venv", "snapshots", "msb-backups"
                ),
            )

            # Apply the proposed changes (overwrite files)
            for change in proposal.get("changes", []):
                target_file = temp_dir / "repo" / change["file"]
                target_file.parent.mkdir(parents=True, exist_ok=True)
                if change.get("action") == "replace":
                    target_file.write_text(change["content"])

            # Run the test suite
            result = subprocess.run(
                ["make", "test"],
                cwd=str(temp_dir / "repo"),
                capture_output=True,
                text=True,
                timeout=300,
            )
            passed = "FAILED" not in result.stdout and result.returncode == 0

            return {
                "proposal_id": proposal_id,
                "passed": passed,
                "output": result.stdout[-1000:],
                "error": result.stderr[-500:],
            }
        except Exception as e:
            return {"proposal_id": proposal_id, "passed": False, "error": str(e)}
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
