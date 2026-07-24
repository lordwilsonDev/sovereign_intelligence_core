"""Proposal Engine — generates refactoring plans from Ouroboros scan results."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class ProposalEngine:
    """Converts Ouroboros hotspots into concrete refactoring proposals."""

    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path(__file__).resolve().parent.parent.parent

    def generate(self, hotspot: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate a refactoring proposal for a single hotspot."""
        file_path = self.repo_path / hotspot.get("file", "")
        if not file_path.exists():
            return None

        original_content = file_path.read_text()
        func_name = hotspot.get("function", "")
        complexity = hotspot.get("complexity", 0)

        if complexity < 8:
            return None  # Not worth the risk

        lines = original_content.splitlines()
        func_start = None
        for i, line in enumerate(lines):
            if f"def {func_name}" in line:
                func_start = i
                break
        if func_start is None:
            return None

        func_body = lines[func_start:]
        mid = len(func_body) // 2
        if mid < 5:
            return None

        proposal_id = hashlib.sha256(
            f"{file_path}{func_name}{datetime.now(timezone.utc)}".encode()
        ).hexdigest()[:12]

        new_content_lines = lines[:func_start] + [
            f"def {func_name}_helper():",
            "    # Extracted logic",
        ] + ["    " + l for l in func_body[mid:]] + [""] + [
            f"def {func_name}():",
        ] + func_body[:mid] + [
            f"    return {func_name}_helper()",
        ]
        new_content = "\n".join(new_content_lines)

        return {
            "id": proposal_id,
            "file": str(file_path.relative_to(self.repo_path)),
            "function": func_name,
            "complexity_before": complexity,
            "technique": "extract_helper",
            "risk": "LOW" if complexity < 15 else "MEDIUM",
            "changes": [
                {
                    "file": str(file_path.relative_to(self.repo_path)),
                    "action": "replace",
                    "content": new_content,
                }
            ],
        }

    def summarize(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Return a concise human-readable summary of a proposal."""
        return {
            "id": proposal.get("id"),
            "file": proposal.get("file"),
            "function": proposal.get("function"),
            "complexity_before": proposal.get("complexity_before"),
            "technique": proposal.get("technique"),
            "risk": proposal.get("risk"),
            "changes": len(proposal.get("changes", [])),
        }
