from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class NotificationRequest(BaseModel):
    source: str
    priority: Priority = Priority.medium
    template: str
    template_data: Dict[str, Any] = {}
    channels: Optional[List[str]] = None
    require_ack: bool = False
    expires_in_seconds: int = 3600


class NotificationResponse(BaseModel):
    id: str
    status: str
    channel: str
    detail: Optional[str] = None


class NotificationRecord(BaseModel):
    id: str
    request: Dict[str, Any]
    status: str
    channel: Optional[str] = None
    rendered: Optional[str] = None
    detail: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class AckRequest(BaseModel):
    ack_id: str
    response: str


class UserPreferences(BaseModel):
    channels: Dict[str, List[Priority]]
    quiet_hours_start: Optional[str] = None
    quiet_hours_end: Optional[str] = None
    rate_limit_per_minute: int = 10

