"""Mesh peer discovery via mDNS and configurable peer lists."""
from __future__ import annotations

import json
import socket
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class MeshDiscovery:
    """Discovers peer nodes on the local network and from configured lists."""

    def __init__(
        self,
        node_id: str,
        port: int = 8766,
        peers_path: Optional[Path] = None,
        bind_host: str = "0.0.0.0",
    ) -> None:
        self.node_id = node_id
        self.port = port
        self.bind_host = bind_host
        self.peers_path = peers_path or Path("mesh_peers.json")
        self._peers: Dict[str, dict] = {}
        self._load_peers()

    def _load_peers(self) -> None:
        """Load manually configured peers from disk."""
        if self.peers_path.exists():
            try:
                data = json.loads(self.peers_path.read_text())
                for peer in data.get("peers", []):
                    self._peers[peer["node_id"]] = peer
            except Exception:
                pass

    def save_peers(self) -> None:
        """Persist the current peer list to disk."""
        payload = {"peers": list(self._peers.values()), "updated_at": time.time()}
        self.peers_path.write_text(json.dumps(payload, indent=2))

    def add_peer(self, node_id: str, address: str, port: int = 8766, metadata: Optional[dict] = None) -> None:
        """Manually add a peer to the registry."""
        entry = {
            "node_id": node_id,
            "address": address,
            "port": port,
            "added_at": time.time(),
        }
        if metadata:
            entry["metadata"] = metadata
        self._peers[node_id] = entry
        self.save_peers()

    def remove_peer(self, node_id: str) -> bool:
        """Remove a peer from the registry."""
        if node_id in self._peers:
            del self._peers[node_id]
            self.save_peers()
            return True
        return False

    def list_peers(self) -> List[dict]:
        """Return all known peers."""
        return list(self._peers.values())

    def announce(self) -> dict:
        """Return this node's announcement payload for peer exchange."""
        hostname = socket.gethostname()
        return {
            "node_id": self.node_id,
            "hostname": hostname,
            "address": self.bind_host,
            "port": self.port,
            "timestamp": time.time(),
        }

    def discover_local(self) -> List[dict]:
        """Placeholder for mDNS-based local peer discovery."""
        return self.list_peers()

    def peer_health(self, peer: Dict[str, Any]) -> Dict[str, Any]:
        """Return basic reachability metadata for a configured peer."""
        try:
            import urllib.request
            address = peer.get("address", "127.0.0.1")
            port = int(peer.get("port", 8766) or 8766)
            url = f"http://{address}:{port}/health"
            with urllib.request.urlopen(url, timeout=3) as response:
                status = response.status
        except Exception as exc:
            return {
                "node_id": peer.get("node_id"),
                "address": peer.get("address"),
                "port": peer.get("port"),
                "reachable": False,
                "status_code": None,
                "error": str(exc),
            }
        base = {
            "node_id": peer.get("node_id"),
            "address": peer.get("address"),
            "port": peer.get("port"),
            "reachable": status == 200,
            "status_code": status,
        }
        meta = peer.get("metadata")
        if isinstance(meta, dict):
            base["metadata"] = meta
        return base
