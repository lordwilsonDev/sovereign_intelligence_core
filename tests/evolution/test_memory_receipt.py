from __future__ import annotations

from fastapi.testclient import TestClient
import pytest

from msb_v2.api.web import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_receipt_endpoint_returns_hash_chain(client: TestClient) -> None:
    response = client.get("/evolution/memory/receipt")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in {"ok", "empty"}
    if data["status"] == "ok":
        assert "entry" in data
        assert "merkle_root" in data
        assert "hash_chain" in data
        assert isinstance(data["hash_chain"], list)
        assert len(data["hash_chain"]) >= 1
