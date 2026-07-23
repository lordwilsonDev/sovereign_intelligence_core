from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


@pytest.fixture()
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


def test_register_identity_creates_peer(client: TestClient) -> None:
    r = client.post(
        "/mesh/identity/register",
        json={
            "node_id": "node-1",
            "public_key": "abcd" * 16,
            "display_name": "Node One",
            "endpoints": ["http://127.0.0.1:9101"],
        },
        headers={"Authorization": "Bearer tok"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "registered"
    assert body["node_id"] == "node-1"


def test_challenge_issue_and_respond(client: TestClient) -> None:
    client.post(
        "/mesh/identity/register",
        json={"node_id": "node-1", "public_key": "abcd" * 16, "display_name": "Node One"},
        headers={"Authorization": "Bearer tok"},
    )
    r = client.post(
        "/mesh/identity/challenge",
        json={"node_id": "node-1"},
        headers={"Authorization": "Bearer tok"},
    )
    assert r.status_code == 200
    challenge = r.json()["challenge"]

    from msb_v2.mesh.identity import KeyPair

    kp = KeyPair(node_id="node-1")
    import os
    signature = kp.sign(bytes.fromhex(challenge))

    r2 = client.post(
        "/mesh/identity/respond",
        json={
            "node_id": "node-1",
            "challenge": challenge,
            "response": signature.hex(),
            "public_key": kp.public_key.public_bytes(
                __import__("cryptography.hazmat.primitives.serialization", fromlist=["serialization"]).Encoding.Raw,  # type: ignore[union-attr]
                __import__("cryptography.hazmat.primitives.serialization", fromlist=["serialization"]).PublicFormat.Raw,  # type: ignore[union-attr]
            ).hex(),
        },
        headers={"Authorization": "Bearer tok"},
    )
    assert r2.status_code == 200
    assert r2.json()["valid"] is True


def test_list_peers(client: TestClient) -> None:
    r = client.get("/mesh/peers", headers={"Authorization": "Bearer tok"})
    assert r.status_code == 200
    assert r.json()["count"] >= 1
