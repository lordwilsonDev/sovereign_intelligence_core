"""Evolution API regression tests."""
from __future__ import annotations

from fastapi.testclient import TestClient
import pytest

from msb_v2.api.web import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_evolve_returns_eligible_proposal(client: TestClient) -> None:
    payload = {"mode": "autonomous", "max_refactors": 1}
    r = client.post("/evolution/evolve", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "autonomous"
    assert "training_examples" in body
    assert "next_steps" in body
