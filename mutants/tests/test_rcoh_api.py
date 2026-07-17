from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.main import app

client = TestClient(app)


def test_rcoh_start_returns_cycle_id():
    resp = client.post("/rcoh/start", json={})
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["cycle_id"].startswith("rcoh-")
    assert body["cycle"]["phase"] is not None


def test_rcoh_start_with_context_and_goals():
    resp = client.post("/rcoh/start", json={
        "context_summary": "test run",
        "goals": ["verify wiring"],
        "max_iterations": 2
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["cycle"]["context_summary"] == "test run"
    assert "verify wiring" in body["cycle"]["goals"]


def test_rcoh_get_cycle_returns_saved_state():
    # Start a cycle first so we have something to fetch
    start_resp = client.post("/rcoh/start", json={"context_summary": "get test"})
    assert start_resp.status_code == 200
    cycle_id = start_resp.json()["cycle_id"]

    # Now fetch it back
    get_resp = client.get(f"/rcoh/{cycle_id}")
    assert get_resp.status_code == 200
    body = get_resp.json()
    assert body["cycle_id"] == cycle_id
    assert body["phase"] is not None


def test_rcoh_get_cycle_404_for_unknown():
    resp = client.get("/rcoh/rcoh-doesnotexist-00000")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()


def test_rcoh_recent_cycles_returns_list():
    # Start a cycle so the list isn't empty
    client.post("/rcoh/start", json={"context_summary": "recent test"})

    resp = client.get("/rcoh/cycles/recent")
    assert resp.status_code == 200
    body = resp.json()
    assert "cycles" in body
    assert isinstance(body["cycles"], list)
    assert len(body["cycles"]) >= 1


def test_rcoh_recent_cycles_respects_limit():
    # Start 3 cycles
    for i in range(3):
        client.post("/rcoh/start", json={"context_summary": f"limit test {i}"})

    resp = client.get("/rcoh/cycles/recent?limit=2")
    assert resp.status_code == 200
    assert len(resp.json()["cycles"]) <= 2


def test_rcoh_recent_not_swallowed_by_cycle_id_route():
    """Ensure /cycles/recent doesn't get matched as /{cycle_id}=cycles."""
    resp = client.get("/rcoh/cycles/recent")
    assert resp.status_code == 200
    assert "cycles" in resp.json()
