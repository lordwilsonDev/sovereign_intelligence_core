from __future__ import annotations

import pytest

from msb_v2.v3.crew_state import AgentStatus, Agent, Crew, CrewSupervisor


def test_create_crew_and_agent() -> None:
    sup = CrewSupervisor()
    crew = sup.create_crew(name="alpha")
    agent = Agent(name="wow", role="planner")
    crew.add_agent(agent)
    assert agent.parent_id == crew.crew_id
    assert agent.status == AgentStatus.IDLE
    assert agent.name == "wow"


def test_update_agent_status() -> None:
    sup = CrewSupervisor()
    crew = sup.create_crew()
    agent = Agent(name="x")
    crew.add_agent(agent)
    updated = sup.update_agent(crew.crew_id, agent.agent_id, status=AgentStatus.SUCCESS, result="ok")
    assert updated is not None
    assert updated.status == AgentStatus.SUCCESS
    assert updated.result == "ok"


def test_route_message() -> None:
    sup = CrewSupervisor()
    crew = sup.create_crew()
    a1 = Agent(name="sender")
    a2 = Agent(name="receiver")
    crew.add_agent(a1)
    crew.add_agent(a2)
    result = sup.route(crew.crew_id, a1.agent_id, a2.agent_id, message="hello")
    assert result["routed"] is True
    assert result["to"] == a2.agent_id
    assert a1.result == "hello"
    assert a1.status == AgentStatus.SUCCESS


def test_supervisor_summary() -> None:
    sup = CrewSupervisor()
    sup.create_crew(name="one")
    sup.create_crew(name="two")
    summary = sup.summary()
    assert summary["crew_count"] == 2
