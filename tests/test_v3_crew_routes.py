from __future__ import annotations

import threading

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.v3_crew import _supervisor

client = TestClient(create_app())


def test_crew_route_returns_200_and_creates_crew() -> None:
    response = client.post("/v3/crew", json={"name": "alpha", "state": {"role": "research"}})
    assert response.status_code == 200, response.json()
    body = response.json()
    assert body.get("crew_id")
    assert body.get("name") == "alpha"


def test_crew_route_rejects_empty_name() -> None:
    response = client.post("/v3/crew", json={"name": "", "state": {}})
    assert response.status_code == 200
    body = response.json()
    assert body.get("name") == "unnamed"


def test_crew_list_after_creation() -> None:
    client.post("/v3/crew", json={"name": "list-test"})
    response = client.get("/v3/crew")
    assert response.status_code == 200
    body = response.json()
    crew_names = [c.get("name") for c in body.get("crews", [])]
    assert "list-test" in crew_names


def test_v3_crew_agent_workflow() -> None:
    crew_response = client.post("/v3/crew", json={"name": "agent-test"})
    assert crew_response.status_code == 200
    crew_id = crew_response.json()["crew_id"]

    agent_response = client.post(f"/v3/crew/{crew_id}/agent", json={"name": "bot1", "role": "assistant"})
    assert agent_response.status_code == 200
    agent_body = agent_response.json()
    assert agent_body.get("name") == "bot1"

    route_response = client.post(
        f"/v3/crew/{crew_id}/agent/bot1/route",
        json={"to": "bot1", "message": "ping"},
    )
    assert route_response.status_code == 200
