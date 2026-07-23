"""First Contact API tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_first_contact_start_creates_session(client: TestClient) -> None:
    response = client.post("/first-contact/start")
    assert response.status_code == 200
    body = response.json()
    assert body["current_step"] == "welcome"
    assert body["completed"] is False


def test_first_contact_advance_flow(client: TestClient) -> None:
    started = client.post("/first-contact/start").json()
    session_id = started["session_id"]
    adv = client.post("/first-contact/advance", json={"session_id": session_id, "step": "assumption", "text": "AI cannot reason"}).json()
    assert adv["participant_assumption"] == "AI cannot reason"
    adv = client.post("/first-contact/advance", json={"session_id": session_id, "step": "invert", "text": "AI might reason"}).json()
    assert any(p["text"] == "AI might reason" for p in adv["proposals"])
    adv = client.post("/first-contact/advance", json={"session_id": session_id, "step": "reveal", "text": "I assumed AI cannot change my mind"}).json()
    assert adv["completed"] is True


def test_first_contact_status_returns_session(client: TestClient) -> None:
    started = client.post("/first-contact/start").json()
    session_id = started["session_id"]
    status = client.get(f"/first-contact/status/{session_id}").json()
    assert status["session_id"] == session_id
