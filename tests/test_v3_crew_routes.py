from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_v3_crew_create_and_get() -> None:
    r = client.post("/v3/crew", params={"name": "alpha", "state": {"mode": "nautical"}})
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "alpha"
    crew_id = body["crew_id"]

    r = client.get(f"/v3/crew/{crew_id}")
    assert r.status_code == 200
    body = r.json()
    assert body["crew_id"] == crew_id
    assert body["name"] == "alpha"


def test_v3_crew_add_agent_and_route() -> None:
    r = client.post("/v3/crew", params={"name": "beta"})
    assert r.status_code == 200
    crew_id = r.json()["crew_id"]

    r = client.post(f"/v3/crew/{crew_id}/agent", params={"name": "wow", "role": "planner"})
    assert r.status_code == 200
    agent = r.json()
    agent_id = agent["agent_id"]
    assert agent["name"] == "wow"

    r = client.post(f"/v3/crew/{crew_id}/agent/{agent_id}/route", params={"message": "swarm", "to": "unknown"})
    assert r.status_code == 200
    body = r.json()
    assert body["routed"] is True or body.get("reason") == "sender_not_found"


def test_v3_crew_list() -> None:
    r = client.get("/v3/crew")
    assert r.status_code == 200
    body = r.json()
    assert "crews" in body
