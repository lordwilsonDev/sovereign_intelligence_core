from __future__ import annotations

import threading
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token

from msb_v2.v3.crew_state import AgentStatus, Crew, CrewSupervisor, Agent

router = APIRouter()
_supervisor = CrewSupervisor()
_lock = threading.Lock()


class CreateCrewRequest(BaseModel):
    name: str = ""
    state: Optional[dict[str, Any]] = None


class AddAgentRequest(BaseModel):
    name: str = ""
    role: str = ""


class RouteMessageRequest(BaseModel):
    to: str = ""
    message: str = ""


@router.post("/v3/crew")
def create_crew(payload: CreateCrewRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> dict[str, Any]:
    with _lock:
        crew = _supervisor.create_crew(name=payload.name or "unnamed", state=payload.state)
    return {"crew_id": crew.crew_id, "name": crew.name}


@router.get("/v3/crew/{crew_id}")
def get_crew(crew_id: str) -> dict[str, Any]:
    crew = _supervisor.get_crew(crew_id)
    if crew is None:
        return {"error": "not_found"}
    return crew.summary()


@router.post("/v3/crew/{crew_id}/agent")
def add_agent(crew_id: str, payload: AddAgentRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> dict[str, Any]:
    crew = _supervisor.get_crew(crew_id)
    if crew is None:
        return {"error": "crew_not_found"}
    agent = Agent(name=payload.name or "unnamed", role=payload.role, status=AgentStatus.IDLE)
    with _lock:
        crew.add_agent(agent)
    return agent.summary()


@router.post("/v3/crew/{crew_id}/agent/{agent_id}/route")
def route_agent_message(crew_id: str, agent_id: str, payload: RouteMessageRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> dict[str, Any]:
    result = _supervisor.route(crew_id=crew_id, from_agent=agent_id, to_agent=payload.to, message=payload.message)
    return result


@router.get("/v3/crew")
def list_crews() -> dict[str, Any]:
    return _supervisor.summary()
