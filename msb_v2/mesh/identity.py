"""Distributed Mesh Protocol — node identity and challenge-response."""

from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import utils as asym_utils
from cryptography.hazmat.backends import default_backend


_MESH_ROOT = Path(os.environ.get("MSB_MESH_ROOT", "./runtime/mesh"))
_KEY_DIR = _MESH_ROOT / "keys"
_PEER_REGISTRY = _MESH_ROOT / "peers.jsonl"


def _ensure_dirs() -> None:
    _MESH_ROOT.mkdir(parents=True, exist_ok=True)
    _KEY_DIR.mkdir(parents=True, exist_ok=True)


def _public_bytes(public) -> bytes:
    if hasattr(public, "public_bytes"):
        return public.public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw
        )
    if hasattr(public, "public_key"):
        public = public.public_key()
    return public.public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw
    )


def _private_bytes(private) -> bytes:
    if hasattr(private, "private_bytes"):
        return private.private_bytes(
            serialization.Encoding.Raw,
            serialization.PrivateFormat.Raw,
            serialization.NoEncryption(),
        )
    raise TypeError("expected private key object")


def _encode_public(public) -> bytes:
    return _public_bytes(public)


def _encode_private(private) -> bytes:
    return _private_bytes(private)


def _decode_public(data: bytes) -> Ed25519PublicKey:
    return Ed25519PublicKey.from_public_bytes(data)


def _decode_private(data: bytes) -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(data)


@dataclass(frozen=True)
class NodeIdentity:
    node_id: str
    public_key: bytes
    display_name: str
    endpoints: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    last_seen: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> Dict[str, object]:
        return {
            "node_id": self.node_id,
            "public_key": self.public_key.hex(),
            "display_name": self.display_name,
            "endpoints": list(self.endpoints),
            "created_at": self.created_at,
            "last_seen": self.last_seen,
        }

    @staticmethod
    def from_dict(data: Dict[str, object]) -> NodeIdentity:
        return NodeIdentity(
            node_id=str(data["node_id"]),
            public_key=bytes.fromhex(str(data["public_key"])),
            display_name=str(data.get("display_name", data["node_id"])),
            endpoints=[str(e) for e in data.get("endpoints", [])],
            created_at=str(data.get("created_at", "")),
            last_seen=str(data.get("last_seen", "")),
        )


class KeyPair:
    def __init__(self, node_id: str) -> None:
        self.node_id = node_id
        self.private_key = Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def sign(self, message: bytes) -> bytes:
        return self.private_key.sign(message)

    def verify(self, message: bytes, signature: bytes) -> bool:
        try:
            _decode_public(_encode_public(self.public_key)).verify(signature, message)
            return True
        except Exception:
            return False

    def save(self) -> None:
        _ensure_dirs()
        path = _KEY_DIR / f"{self.node_id}_private.json"
        payload = {
            "node_id": self.node_id,
            "private_key": _encode_private(self.private_key).hex(),
            "public_key": _encode_public(self.public_key).hex(),
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp.replace(path)

    @classmethod
    def load(cls, node_id: str) -> Optional[KeyPair]:
        path = _KEY_DIR / f"{node_id}_private.json"
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        kp = cls.__new__(cls)
        kp.node_id = str(payload["node_id"])
        kp.private_key = _decode_private(bytes.fromhex(payload["private_key"]))
        kp.public_key = _decode_public(bytes.fromhex(payload["public_key"]))
        return kp


@dataclass
class ChallengeRequest:
    node_id: str
    challenge: bytes
    issued_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> Dict[str, object]:
        return {
            "node_id": self.node_id,
            "challenge": self.challenge.hex(),
            "issued_at": self.issued_at,
        }

    @staticmethod
    def from_dict(data: Dict[str, object]) -> ChallengeRequest:
        return ChallengeRequest(
            node_id=str(data["node_id"]),
            challenge=bytes.fromhex(str(data["challenge"])),
            issued_at=str(data.get("issued_at", "")),
        )


@dataclass
class ChallengeResponse:
    node_id: str
    challenge: bytes
    response: bytes
    public_key: bytes
    issued_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))

    def to_dict(self) -> Dict[str, object]:
        return {
            "node_id": self.node_id,
            "challenge": self.challenge.hex(),
            "response": self.response.hex(),
            "public_key": self.public_key.hex(),
            "issued_at": self.issued_at,
        }

    @staticmethod
    def from_dict(data: Dict[str, object]) -> ChallengeResponse:
        return ChallengeResponse(
            node_id=str(data["node_id"]),
            challenge=bytes.fromhex(str(data["challenge"])),
            response=bytes.fromhex(str(data["response"])),
            public_key=bytes.fromhex(str(data["public_key"])),
            issued_at=str(data.get("issued_at", "")),
        )


class _InMemoryChallengeStore:
    def __init__(self) -> None:
        self._store: Dict[str, ChallengeRequest] = {}

    def add(self, req: ChallengeRequest) -> None:
        self._store[req.node_id] = req

    def pop(self, node_id: str) -> Optional[ChallengeRequest]:
        return self._store.pop(node_id, None)

    def exists(self, node_id: str) -> bool:
        return node_id in self._store


_challenge_store = _InMemoryChallengeStore()


class NodeRegistry:
    def __init__(self, root: Path = _MESH_ROOT, peers_path: Optional[Path] = None) -> None:
        self.root = root
        self.peers_path = peers_path or (root / "peers.jsonl")
        self.peers: Dict[str, NodeIdentity] = {}
        self._load()

    def _load(self) -> None:
        if not self.peers_path.exists():
            self.peers_path.parent.mkdir(parents=True, exist_ok=True)
            self.peers_path.write_text("", encoding="utf-8")
            return
        for line in self.peers_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                record = NodeIdentity.from_dict(json.loads(line))
                self.peers[record.node_id] = record
            except Exception:
                continue

    def _persist(self, peer: NodeIdentity) -> None:
        line = json.dumps(peer.to_dict())
        tmp = self.peers_path.with_suffix(".tmp")
        with tmp.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        tmp.replace(self.peers_path)

    def register(self, peer: NodeIdentity) -> None:
        self.peers[peer.node_id] = peer
        self._persist(peer)

    def get(self, node_id: str) -> Optional[NodeIdentity]:
        return self.peers.get(node_id)

    def all(self) -> List[NodeIdentity]:
        return list(self.peers.values())


_registry = NodeRegistry()


class IdentityChallenge:
    @staticmethod
    def issue(to_node_id: str) -> ChallengeRequest:
        challenge = os.urandom(32)
        req = ChallengeRequest(node_id=to_node_id, challenge=challenge)
        _challenge_store.add(req)
        return req

    @staticmethod
    def respond(node_id: str, keypair: KeyPair, challenge: bytes) -> ChallengeResponse:
        if not _challenge_store.exists(node_id):
            raise ValueError("challenge not issued")
        signature = keypair.sign(challenge)
        return ChallengeResponse(
            node_id=keypair.node_id, challenge=challenge, response=signature, public_key=_encode_public(keypair.public_key)
        )

    @staticmethod
    def verify(req: ChallengeRequest, resp: ChallengeResponse) -> bool:
        if req.challenge != resp.challenge:
            return False
        try:
            pub = _decode_public(resp.public_key)
            pub.verify(resp.response, resp.challenge)
            return True
        except Exception:
            return False
