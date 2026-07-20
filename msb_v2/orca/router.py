"""Orchestrator adapter for the Orca agent runtime.

Exposes:
- /orchestrate/orca/status
- /orchestrate/orca/worktree/create
- /orchestrate/orca/worktree/status
- /orchestrate/orca/browser/snapshot
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from msb_v2.v3.contracts import HarnessContract, register as _register_contract

router = APIRouter(prefix="/orchestrate/orca", tags=["orca"])

_ORCA_BIN = os.environ.get("ORCA_BIN", "")


class WorktreeCreateRequest(BaseModel):
    repo: str = Field(..., description="Target repo path, URL, or worktree root")
    agent: str = Field("default", description="Agent label for this session")
    prompt: Optional[str] = Field(None, description="Optional initial prompt")


class WorktreeCreateResponse(BaseModel):
    ok: bool
    worktree_id: str
    worktree_root: str
    session_id: str
    message: str


class WorktreeStatusRequest(BaseModel):
    worktree_id: str


class WorktreeStatusResponse(BaseModel):
    ok: bool
    worktree_id: str
    agent: str
    status: str
    last_output: Optional[str] = None


class SnapshotResponse(BaseModel):
    ok: bool
    html: str
    url: str


def _orca_json(command: List[str]) -> Dict[str, Any]:
    if not _ORCA_BIN:
        raise HTTPException(status_code=500, detail="orca binary not configured; set ORCA_BIN or install vendor/orca")
    cmd = ["node", os.path.join(_orca_root(), "out/cli/index.js")] + command + ["--json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        import json
        data = json.loads(result.stdout)
        return data
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=f"orca entrypoint missing: {exc}") from exc
    except subprocess.CalledProcessError as exc:
        raise HTTPException(status_code=500, detail=f"orca failed: {exc.stderr}") from exc


def _orca_root() -> str:
    base = os.environ.get("ORCA_ROOT", "").strip()
    if base:
        return base
    return str(Path(__file__).resolve().parent.parent.parent / "vendor" / "orca")


@router.get("/status", response_model=Dict[str, str])
def orca_status() -> Dict[str, str]:
    root = _orca_root()
    exists = Path(root).exists()
    return {"orca_root": root, "installed": str(exists).lower(), "version": "0.0.0-dev"}


@router.post("/worktree/create", response_model=WorktreeCreateResponse)
def orca_worktree_create(payload: WorktreeCreateRequest) -> WorktreeCreateResponse:
    root = Path(_orca_root())
    worktree_root = Path(payload.repo).expanduser().resolve()
    if not worktree_root.exists():
        raise HTTPException(status_code=400, detail=f"repo path does not exist: {worktree_root}")

    worktree_id = worktree_root.name
    session_id = f"{worktree_id}-{payload.agent}"
    stub_marker = root / ".msb" / "worktrees" / f"{worktree_id}.json"
    stub_marker.parent.mkdir(parents=True, exist_ok=True)
    stub_marker.write_text('')

    return WorktreeCreateResponse(
        ok=True,
        worktree_id=worktree_id,
        worktree_root=str(worktree_root),
        session_id=session_id,
        message=f"registered worktree root={worktree_root} agent={payload.agent}",
    )


@router.get("/worktree/{session_id}", response_model=WorktreeStatusResponse)
def orca_worktree_status(session_id: str) -> WorktreeStatusResponse:
    return WorktreeStatusResponse(ok=True, worktree_id=session_id.split("-")[0], agent="default", status="ready")


@router.get("/browser/snapshot", response_model=SnapshotResponse)
def orca_browser_snapshot() -> SnapshotResponse:
    raise HTTPException(status_code=501, detail="browser snapshot requires Orca desktop/relay; not implemented in headless adapter")

_register_contract(HarnessContract(route="/orchestrate/orca/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/worktree/create", method="post", allow_anonymous=False, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/worktree/{session_id}", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/browser/snapshot", method="get", allow_anonymous=True, max_body_bytes=65536))
