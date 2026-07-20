"""Orchestrator adapter for the Orca worktree agent runtime.

Wraps `git worktree` so MSB can create agent sessions as disposable Git
worktrees without depending on the Node/Electron Orca UI. Browser snapshot
relies on the bundled Orca CLI when explicitly enabled; otherwise returns 501.
"""
from __future__ import annotations

import dataclasses
import json
import os
import re
import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from msb_v2.v3.contracts import HarnessContract, register as _register_contract

router = APIRouter(prefix="/orchestrate/orca", tags=["orca"])

_GIT_TIMEOUT_SECONDS = int(os.environ.get("ORCA_GIT_TIMEOUT_SECONDS", "30"))
_ORCA_BIN = os.environ.get("ORCA_BIN", "")


class WorktreeCreateRequest(BaseModel):
    repo: str = Field(..., description="Target repo path or a Git URL")
    agent: str = Field("default", description="Agent label for this session")
    prompt: Optional[str] = Field(None, description="Optional initial prompt")
    branch: Optional[str] = Field(None, description="Optional branch name; auto-generated if omitted")


class WorktreeCreateResponse(BaseModel):
    ok: bool
    worktree_id: str
    worktree_root: str
    session_id: str
    agent: str
    branch: str
    repo: str
    message: str


class WorktreeStatusResponse(BaseModel):
    ok: bool
    worktree_id: str
    agent: str
    status: str
    branch: Optional[str] = None
    repo: Optional[str] = None
    last_output: Optional[str] = None


class SnapshotResponse(BaseModel):
    ok: bool
    html: str
    url: str
    title: Optional[str] = None
    relay: Optional[str] = None


def _git(*args: str, cwd: Optional[str] = None) -> subprocess.CompletedProcess:
    command = [shutil.which("git") or "git", *args]
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        timeout=_GIT_TIMEOUT_SECONDS,
    )


def _ensure_repo(repo: str) -> str:
    path = Path(repo).expanduser().resolve()
    if not path.is_dir() or not (path / ".git").exists():
        raise HTTPException(status_code=400, detail=f"target repo is not a local Git repository: {path}")
    return str(path)


def _worktree_root_for_repo(repo_path: str, session_id: str) -> str:
    base = Path(repo_path)
    return str(base.parent / f"{base.name}-worktrees" / session_id)


def _cli_json(command: List[str]) -> Dict[str, Any]:
    if not _ORCA_BIN:
        raise HTTPException(status_code=500, detail="ORCA_BIN is not configured; cannot invoke Orca CLI")
    cmd = [_ORCA_BIN, *command, "--json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=_GIT_TIMEOUT_SECONDS)
        clipped = (result.stdout or "").strip()
        if not clipped:
            return {"ok": True}
        try:
            return json.loads(clipped)
        except json.JSONDecodeError:
            return {"ok": True, "raw": clipped}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=f"Orca CLI missing: {exc}") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip()
        raise HTTPException(status_code=502, detail=detail or f"Orca failed with code {exc.returncode}") from exc
    except subprocess.TimeoutExpired as exc:
        raise HTTPException(status_code=502, detail=f"Orca CLI timed out after {_GIT_TIMEOUT_SECONDS}s") from exc


def _normalize_url(value: Optional[str]) -> Optional[str]:
    if not value:
        return value
    value = value.strip()
    if value.lower().startswith("http://") or value.lower().startswith("https://"):
        return value
    return f"https://{value}" if "." in value else value


_BROWSER_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def _snapshot_placeholder(relay: Optional[str]) -> str:
    if relay:
        return f"<!doctype html><html><head><meta charset='utf-8'><title>Orca browser relay</title></head><body><p>Browser snapshot is relayed by <code>{relay}</code>.</p></body></html>"
    return "<!doctype html><html><head><meta charset='utf-8'><title>Orca browser</title></head><body><p>Browser snapshot requires ORCA_BIN.</p></body></html>"


@router.get("/status", response_model=Dict[str, str])
def orca_status() -> Dict[str, Any]:
    git_ok = bool(shutil.which("git"))
    orca_root = Path(__file__).resolve().parent.parent.parent / "vendor" / "orca"
    return {
        "adapter": "git-worktree-python",
        "mode": "native" if git_ok else "fallback",
        "git_available": str(git_ok).lower(),
        "orca_root": str(orca_root),
        "orca_bin_configured": str(bool(_ORCA_BIN)).lower(),
        "git_timeout": str(_GIT_TIMEOUT_SECONDS),
        "interpreter": "python",
        "version": "0.0.0-dev",
    }


@router.post("/worktree/create", response_model=WorktreeCreateResponse)
def orca_worktree_create(payload: WorktreeCreateRequest) -> WorktreeCreateResponse:
    repo_path = _ensure_repo(payload.repo)
    branch = payload.branch or f"msb/{payload.agent}/{uuid.uuid4().hex[:8]}"
    session_id = f"{Path(repo_path).name}-{payload.agent}-{uuid.uuid4().hex[:6]}"
    worktree_root = _worktree_root_for_repo(repo_path, session_id)
    Path(worktree_root).mkdir(parents=True, exist_ok=False)

    add_cmd = _git(
        "worktree",
        "add",
        "-b",
        branch,
        str(worktree_root),
        "HEAD",
        cwd=repo_path,
    )
    if add_cmd.returncode != 0:
        detail = add_cmd.stderr.strip() or f"git worktree add failed with code {add_cmd.returncode}"
        raise HTTPException(status_code=502, detail=detail)

    try:
        _git("config", "user.name", "MSB Orca Adapter", cwd=repo_path)
    except Exception:
        pass

    return WorktreeCreateResponse(
        ok=True,
        worktree_id=Path(worktree_root).name,
        worktree_root=worktree_root,
        session_id=session_id,
        agent=payload.agent,
        branch=branch,
        repo=repo_path,
        message=f"created worktree {session_id} from HEAD on {branch}",
    )


@router.get("/worktree/{session_id}", response_model=WorktreeStatusResponse)
def orca_worktree_status(session_id: str, repo: str = Query(..., description="Repo path for this worktree")) -> WorktreeStatusResponse:
    repo_path = _ensure_repo(repo)
    list_cmd = _git("worktree", "list", cwd=repo_path)
    if list_cmd.returncode != 0:
        raise HTTPException(status_code=502, detail=list_cmd.stderr.strip())

    expected_root = _worktree_root_for_repo(repo_path, session_id).rstrip("/")
    listed = [line.strip() for line in list_cmd.stdout.splitlines() if line.strip()]
    found = any(line == expected_root or line.rstrip("/").endswith(f"/{Path(expected_root).name}") for line in listed)

    if not found and not Path(expected_root).exists():
        return WorktreeStatusResponse(ok=False, worktree_id=session_id, agent="unknown", status="missing")

    status_cmd = _git("status", "--short", "--branch", cwd=expected_root)
    branch_line = ""
    if status_cmd.returncode == 0:
        for line in status_cmd.stdout.splitlines():
            line = line.strip()
            if line.startswith("## "):
                branch_line = line[3:]
                break

    return WorktreeStatusResponse(
        ok=True,
        worktree_id=session_id,
        agent="default",
        status="ready",
        branch=branch_line or None,
        repo=repo_path,
        last_output=branch_line or f"{Path(expected_root).name}",
    )


@router.get("/browser/snapshot", response_model=SnapshotResponse)
def orca_browser_snapshot(agent: Optional[str] = Query(None, description="Optional screen context")) -> SnapshotResponse:
    if not _ORCA_BIN:
        return SnapshotResponse(ok=False, html=_snapshot_placeholder(None), url="", relay=None)

    raw = _cli_json(["browser", "snapshot", "--agent", agent or "default"])
    html = str(raw.get("html") or "")
    url = str(raw.get("url") or "")
    title = str(raw.get("title") or "")
    relay = str(raw.get("relay") or _ORCA_BIN)

    if not html:
        html = _snapshot_placeholder(relay)

    normalized = _normalize_url(url) if url else ""
    if title:
        title = _BROWSER_TITLE_RE.sub(lambda m: m.group(1), title)
        title = " ".join(title.split())
    return SnapshotResponse(ok=True, html=html, url=normalized, title=title or None, relay=relay)


_register_contract(HarnessContract(route="/orchestrate/orca/status", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/worktree/create", method="post", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/worktree/{session_id}", method="get", allow_anonymous=True, max_body_bytes=65536))
_register_contract(HarnessContract(route="/orchestrate/orca/browser/snapshot", method="get", allow_anonymous=True, max_body_bytes=65536))
