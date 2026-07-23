"""Mesh Task Contract API — submit, execute, and retrieve reasoning tasks across nodes."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
import time

from msb_v2.mesh.executor import MeshTaskExecutor
from msb_v2.mesh.identity import NodeIdentity

router = APIRouter(tags=["mesh-tasks"])

# In-memory task store (will be replaced with persistent mesh ledger)
_task_store: Dict[str, Dict[str, Any]] = {}


class TaskSubmission(BaseModel):
    intent: str
    context: Optional[Dict[str, Any]] = {}
    requesting_node_id: str
    requesting_node_signature: str


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None


_identity = NodeIdentity(node_id=__import__("socket").gethostname(), public_key=b"\x00" * 32, display_name=__import__("socket").gethostname())


@router.post("/submit", response_model=TaskResponse)
def submit_task(submission: TaskSubmission):
    """Submit a reasoning task to the mesh. Returns immediately with a task_id."""
    task_id = str(uuid.uuid4())[:12]
    _task_store[task_id] = {
        "intent": submission.intent,
        "context": submission.context,
        "requesting_node_id": submission.requesting_node_id,
        "status": "queued",
        "submitted_at": time.time(),
    }
    return TaskResponse(task_id=task_id, status="queued")


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, execute: bool = Query(False)):
    """Retrieve the status and result of a submitted task. Set execute=true to run it now."""
    task = _task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if execute and task.get("status") == "queued":
        executor = MeshTaskExecutor(_identity, _task_store)
        task = executor.execute(task_id)

    return TaskResponse(task_id=task_id, status=task["status"], result=task.get("result"))
