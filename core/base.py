from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional


class RoleType(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    CRITIC = "critic"
    EXECUTOR = "executor"


class RoleCardinality(str, Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"


class RoleDefinition:
    def __init__(self, role_type: str, name: str, system_prompt: str, cardinality: str = "single", allowed_tools: Optional[List[str]] = None):
        self.role_type = role_type
        self.name = name
        self.system_prompt = system_prompt
        self.cardinality = cardinality
        self.allowed_tools = allowed_tools or []


class AgentInstanceConfig:
    def __init__(self, role: RoleDefinition, instance_id: str, context: Optional[Dict[str, Any]] = None):
        self.role = role
        self.instance_id = instance_id
        self.context = context or {}


class BaseArchitecture:
    def __init__(self, name: str, roles: Optional[List[RoleDefinition]] = None):
        self.name = name
        self.roles = roles or []

    def register_instance(self, config: AgentInstanceConfig) -> None:
        self.roles.append(config.role)
