from __future__ import annotations

import threading
from typing import Any

from fastapi import APIRouter

from msb_v2.v3.crew_state import AgentStatus, Crew, CrewSupervisor, Agent

router = APIRouter()
_supervisor = CrewSupervisor()
_lock = threading.Lock()


@router.post("/v3/crew")
def create_crew(name: str = "", state: dict[str, Any] | None = None) -> dict[str, Any]:
    with _lock:
        crew = _supervisor.create_crew(name=name, state=state)
    return {"crew_id": crew.crew_id, "name": crew.name}


@router.get("/v3/crew/{crew_id}")
def get_crew(crew_id: str) -> dict[str, Any]:
    crew = _supervisor.get_crew(crew_id)
    if crew is None:
        return {"error": "not_found"}
    return crew.summary()


@router.post("/v3/crew/{crew_id}/agent")
def add_agent(crew_id: str, name: str = "", role: str = "") -> dict[str, Any]:
    crew = _supervisor.get_crew(crew_id)
    if crew is None:
        return {"error": "crew_not_found"}
    agent = Agent(name=name, role=role, status=AgentStatus.IDLE)
    with _lock:
        crew.add_agent(agent)
    return agent.summary()


@router.post("/v3/crew/{crew_id}/agent/{agent_id}/route")
def route_agent_message(crew_id: str, agent_id: str, message: str = "", to: str = "") -> dict[str, Any]:
    result = _supervisor.route(crew_id=crew_id, from_agent=agent_id, to_agent=to, message=message)
    return result


@router.get("/v3/crew")
def list_crews() -> dict[str, Any]:
    return _supervisor.summary()
