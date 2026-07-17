from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    DLQ = "DLQ"


class Priority(int, Enum):
    CRITICAL = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class EventPhase(str, Enum):
    PERCEIVE = "PERCEIVE"
    ORIENT = "ORIENT"
    DECIDE = "DECIDE"
    ACT = "ACT"
    REFLECT = "REFLECT"


class Task(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    goal: str
    client_id: str = "default"
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    created_at: float = Field(default_factory=time.time)
    retry_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = Field(default_factory=time.time)
    session_id: str
    phase: EventPhase
    actor: str = "AURA"
    tool_name: Optional[str] = None
    latency_ms: Optional[float] = None
    status: str = "SUCCESS"
    payload: Dict[str, Any] = Field(default_factory=dict)


class State(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    current_goal: Optional[str] = None
    task_id: Optional[str] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    step: int = 0
