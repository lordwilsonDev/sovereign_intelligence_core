"""Tests for mesh peer discovery."""
from __future__ import annotations

import tempfile
from pathlib import Path

from msb_v2.mesh.discovery import MeshDiscovery


def test_add_and_list_peers() -> None:
    tmp = Path(tempfile.mkdtemp()) / "peers.json"
    discovery = MeshDiscovery(node_id="node-1", peers_path=tmp)
    discovery.add_peer("node-2", "192.168.1.2", 8766)
    peers = discovery.list_peers()
    assert len(peers) == 1
    assert peers[0]["node_id"] == "node-2"


def test_remove_peer() -> None:
    tmp = Path(tempfile.mkdtemp()) / "peers.json"
    discovery = MeshDiscovery(node_id="node-1", peers_path=tmp)
    discovery.add_peer("node-3", "10.0.0.1", 8766)
    assert discovery.remove_peer("node-3") is True
    assert len(discovery.list_peers()) == 0


def test_remove_nonexistent_peer() -> None:
    tmp = Path(tempfile.mkdtemp()) / "peers.json"
    discovery = MeshDiscovery(node_id="node-1", peers_path=tmp)
    assert discovery.remove_peer("ghost") is False


def test_announce_matches_state() -> None:
    discovery = MeshDiscovery(node_id="node-1", port=9000)
    announce = discovery.announce()
    assert announce["node_id"] == "node-1"
    assert announce["port"] == 9000
    assert "address" in announce
    assert "timestamp" in announce


def test_persistence_survives_reload() -> None:
    tmp = Path(tempfile.mkdtemp()) / "peers.json"
    d1 = MeshDiscovery(node_id="node-1", peers_path=tmp)
    d1.add_peer("node-4", "172.16.0.1", 8766)
    d1.save_peers()

    d2 = MeshDiscovery(node_id="node-1", peers_path=tmp)
    peers = d2.list_peers()
    assert len(peers) == 1
    assert peers[0]["node_id"] == "node-4"
