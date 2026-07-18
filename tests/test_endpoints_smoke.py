from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app

client = TestClient(create_app())


def test_health_endpoint_exists() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"


def test_aura_run_endpoint_exists() -> None:
    response = client.post("/aura/run", json={"goal": "ping"})
    assert response.status_code == 200
    assert response.json().get("status") == "ok"


def test_v3_memory_endpoints_exist() -> None:
    assert client.get("/v3/memory/routes").status_code == 200
    assert client.get("/v3/memory/recent").status_code == 200
    assert client.get("/v3/memory/search", params={"q": "x"}).status_code == 200


def test_v3_crew_endpoint_exists() -> None:
    response = client.post("/v3/crew", json={"name": "smoke"})
    assert response.status_code == 200
    assert response.json().get("crew_id")


def test_v3_tools_endpoint_exists() -> None:
    assert client.get("/v3/tools").status_code == 200
    assert client.get("/v3/tools/schema").status_code == 200


def test_brain_run_endpoint_exists() -> None:
    response = client.post("/brain/run", json={"intent": "query", "query": "ping"})
    assert response.status_code == 200
