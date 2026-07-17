from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


class Proposal:
    def __init__(self, proposal_id: str, change_type: str, patch: Dict[str, Any]) -> None:
        self.proposal_id = proposal_id
        self.change_type = change_type
        self.patch = patch
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.approved = False


class Oracle:
    def __init__(self, repo: Path = Path("."), proposals_dir: Path = Path("proposals"), config_path: Path = Path("config.yaml")) -> None:
        self.repo = repo
        self.proposals_dir = Path(proposals_dir)
        self.config_path = Path(config_path)
        self.proposals_dir.mkdir(parents=True, exist_ok=True)

    def propose(self, change_type: str, patch: Dict[str, Any]) -> Proposal:
        proposal_id = f"{change_type}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        proposal = Proposal(proposal_id=proposal_id, change_type=change_type, patch=patch)
        path = self.proposals_dir / f"{proposal_id}.json"
        path.write_text(json.dumps({"proposal_id": proposal.proposal_id, "change_type": proposal.change_type, "patch": proposal.patch, "created_at": proposal.created_at, "approved": proposal.approved}, indent=2))
        return proposal

    def approve(self, proposal_id: str, commit: bool = True) -> Dict[str, Any]:
        target = self.proposals_dir / f"{proposal_id}.json"
        if not target.exists():
            return {"status": "error", "message": f"proposal not found: {proposal_id}"}
        data = json.loads(target.read_text())
        data["approved"] = True
        target.write_text(json.dumps(data, indent=2))
        applied = self._apply_patch(data.get("patch", {}))
        if commit:
            self._git_commit(f"chore(aura): apply proposal {proposal_id}")
        return {"status": "ok", "proposal_id": proposal_id, "applied": applied}

    def _apply_patch(self, patch: Dict[str, Any]) -> Dict[str, Any]:
        if not patch:
            return {}
        config_path = self.config_path
        if config_path.exists():
            current = config_path.read_text()
            updated = current
            for key, value in patch.items():
                marker = f"{key}:"
                if marker in updated:
                    updated = updated.replace(marker, f"{key}: {json.dumps(value) if not isinstance(value, str) else value}\n")
            config_path.write_text(updated)
            return {"patch_items": list(patch.keys())}
        return {"note": "config.yaml not found; patch staged"}

    def _git_commit(self, message: str) -> None:
        commands = [
            ["git", "add", "."],
            ["git", "commit", "-m", message],
            ["git", "push"],
        ]
        for cmd in commands:
            try:
                __import__("subprocess").run(cmd, cwd=str(self.repo), stdout=__import__("subprocess").DEVNULL, stderr=__import__("subprocess").DEVNULL)
            except Exception:
                pass
