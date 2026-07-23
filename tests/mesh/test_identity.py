"""Mesh identity tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from msb_v2.mesh.identity import (
    ChallengeRequest,
    ChallengeResponse,
    IdentityChallenge,
    KeyPair,
    NodeIdentity,
    NodeRegistry,
)


@pytest.fixture()
def mesh_root(tmp_path: Path) -> Path:
    return tmp_path / "mesh"


@pytest.fixture()
def registry(mesh_root: Path) -> NodeRegistry:
    return NodeRegistry(root=mesh_root)


@pytest.fixture()
def keypair() -> KeyPair:
    return KeyPair(node_id="test-node")


class TestKeyPair:
    def test_generate_and_save(self, mesh_root: Path, keypair: KeyPair) -> None:
        keypair.save()
        loaded = KeyPair.load(keypair.node_id)
        assert loaded is not None
        assert loaded.node_id == keypair.node_id
        assert _encode_hex(loaded.public_key) == _encode_hex(keypair.public_key)
        assert loaded is not keypair

    def test_sign_and_verify(self, keypair: KeyPair) -> None:
        message = b"hello mesh"
        signature = keypair.sign(message)
        assert keypair.verify(message, signature) is True
        assert keypair.verify(b"other message", signature) is False
        tampered = signature[:-1] + bytes([signature[-1] ^ 0xFF])
        assert keypair.verify(message, tampered) is False

    def test_missing_key_returns_none(self, mesh_root: Path) -> None:
        assert KeyPair.load("nonexistent") is None


def _encode_hex(key) -> str:
    from cryptography.hazmat.primitives import serialization
    if isinstance(key, bytes):
        return key.hex()
    return key.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()


class TestNodeRegistry:
    def test_register_and_get(self, registry: NodeRegistry) -> None:
        peer = NodeIdentity(node_id="peer-1", public_key=b"\x00" * 32, display_name="Peer One")
        registry.register(peer)
        fetched = registry.get("peer-1")
        assert fetched is not None
        assert fetched.display_name == "Peer One"
        assert fetched.public_key == b"\x00" * 32

    def test_all_returns_registered(self, registry: NodeRegistry) -> None:
        registry.register(NodeIdentity(node_id="a", public_key=b"\x01" * 32, display_name="A"))
        registry.register(NodeIdentity(node_id="b", public_key=b"\x02" * 32, display_name="B"))
        ids = [p.node_id for p in registry.all()]
        assert ids == ["a", "b"]

    def test_missing_returns_none(self, registry: NodeRegistry) -> None:
        assert registry.get("missing") is None


class TestIdentityChallenge:
    def test_challenge_response_roundtrip(self, keypair: KeyPair) -> None:
        req = IdentityChallenge.issue(keypair.node_id)
        resp = IdentityChallenge.respond(keypair.node_id, keypair, req.challenge)
        assert IdentityChallenge.verify(req, resp) is True
        assert _encode_hex(resp.public_key) == _encode_hex(keypair.public_key)

    def test_wrong_challenge_fails(self, keypair: KeyPair) -> None:
        req = IdentityChallenge.issue(keypair.node_id)
        wrong = ChallengeRequest(node_id=keypair.node_id, challenge=b"\xff" * 32)
        resp = ChallengeResponse(node_id=keypair.node_id, challenge=wrong.challenge, response=b"", public_key=b"")
        assert IdentityChallenge.verify(req, resp) is False

    def test_respond_without_issue_fails(self, keypair: KeyPair) -> None:
        with pytest.raises(ValueError):
            IdentityChallenge.respond("missing", keypair, b"\x00" * 32)
