"""Mesh Task Contract API — submit and retrieve reasoning tasks across nodes."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
import time

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
def get_task(task_id: str):
    """Retrieve the status and result of a submitted task."""
    task = _task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(task_id=task_id, status=task["status"], result=task.get("result"))
