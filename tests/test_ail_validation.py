from __future__ import annotations

import pytest

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_mine_assumptions_from_text(client: TestClient) -> None:
    response = client.post("/validation/ail/mine", json={
        "text": "Cancer progresses because mutations accumulate. Since the tumor microenvironment is immune-suppressed, targeted therapy fails."
    })
    assert response.status_code == 200
    body = response.json()
    assert body["count"] >= 1
    assert any("mutations accumulate" in a["statement"] for a in body["assumptions"])


def test_invert_assumption_generates_inverses(client: TestClient) -> None:
    response = client.post("/validation/ail/invert", json={"assumption": "Mutation accumulation drives cancer"})
    assert response.status_code == 200
    body = response.json()
    assert body["assumption"] == "Mutation accumulation drives cancer"
    assert len(body["inversions"]) >= 2
