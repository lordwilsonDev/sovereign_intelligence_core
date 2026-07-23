"""Mesh Discovery API — peer registration, listing, and removal."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException

from msb_v2.mesh.discovery import MeshDiscovery
from msb_v2.mesh.identity import NodeIdentity

router = APIRouter(tags=["mesh-discovery"])

_identity = NodeIdentity(
    node_id=__import__("socket").gethostname(),
    public_key=b"\x00" * 32,
    display_name=__import__("socket").gethostname(),
)
_discovery = MeshDiscovery(node_id=_identity.node_id, peers_path=Path("runtime/mesh/peers.json"))


@router.get("/peers")
def list_peers() -> dict:
    """Return all known peers."""
    return {"peers": _discovery.list_peers()}


@router.post("/peers")
def add_peer(node_id: str, address: str, port: int = 8766) -> dict:
    """Manually register a peer."""
    _discovery.add_peer(node_id, address, port)
    return {"status": "added", "node_id": node_id}


@router.delete("/peers/{node_id}")
def remove_peer(node_id: str) -> dict:
    """Remove a peer from the registry."""
    success = _discovery.remove_peer(node_id)
    if not success:
        raise HTTPException(status_code=404, detail="Peer not found")
    return {"status": "removed", "node_id": node_id}


@router.get("/announce")
def announce() -> dict:
    """Return this node's announcement payload."""
    return _discovery.announce()


@router.get("/discover")
def discover_local() -> dict:
    """Trigger local peer discovery."""
    return {"peers": _discovery.discover_local()}
