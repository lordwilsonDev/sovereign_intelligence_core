from __future__ import annotations

import copy
import uuid
from dataclasses import dataclass, field
from typing import Any


class AgentStatus(str):
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Agent:
    agent_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    name: str = ""
    role: str = ""
    status: str = AgentStatus.IDLE
    parent_id: str | None = None
    result: Any = None
    error: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "status": self.status,
            "parent_id": self.parent_id,
            "result": self.result,
            "error": self.error,
            "metrics": self.metrics,
        }


@dataclass
class Crew:
    crew_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    name: str = ""
    agents: list[Agent] = field(default_factory=list)
    state: dict[str, Any] = field(default_factory=dict)

    def add_agent(self, agent: Agent) -> None:
        agent.parent_id = self.crew_id
        self.agents.append(agent)

    def summary(self) -> dict[str, Any]:
        return {
            "crew_id": self.crew_id,
            "name": self.name,
            "agent_count": len(self.agents),
            "agents": [a.summary() for a in self.agents],
            "state": self.state,
        }


class CrewSupervisor:
    def __init__(self) -> None:
        self._crews: dict[str, Crew] = {}

    def create_crew(self, name: str = "", state: dict[str, Any] | None = None) -> Crew:
        crew = Crew(name=name, state=state or {})
        self._crews[crew.crew_id] = crew
        return crew

    def get_crew(self, crew_id: str) -> Crew | None:
        return self._crews.get(crew_id)

    def update_agent(self, crew_id: str, agent_id: str, **updates: Any) -> Agent | None:
        crew = self._crews.get(crew_id)
        if crew is None:
            return None
        for agent in crew.agents:
            if agent.agent_id == agent_id:
                for k, v in updates.items():
                    if hasattr(agent, k):
                        setattr(agent, k, v)
                return agent
        return None

    def route(self, crew_id: str, from_agent: str, to_agent: str, message: str = "") -> dict[str, Any]:
        crew = self._crews.get(crew_id)
        if crew is None:
            return {"error": "crew_not_found"}
        for agent in crew.agents:
            if agent.agent_id == from_agent:
                agent.result = message
                agent.status = AgentStatus.SUCCESS
                return {"routed": True, "from": from_agent, "to": to_agent, "message": message}
        return {"routed": False, "reason": "sender_not_found"}

    def summary(self) -> dict[str, Any]:
        return {
            "crew_count": len(self._crews),
            "crews": [c.summary() for c in self._crews.values()],
        }
