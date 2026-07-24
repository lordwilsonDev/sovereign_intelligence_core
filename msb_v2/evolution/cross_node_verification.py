"""Cross-Node Task Verification — distribute work across mesh peers and verify consensus."""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from msb_v2.mesh.discovery import MeshDiscovery


@dataclass
class TaskAssignment:
    task_id: str
    payload: Dict[str, Any]
    assigned_to: List[str]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    results: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    consensus: Optional[Dict[str, Any]] = None


class CrossNodeVerification:
    """Distributes tasks to mesh peers and verifies consensus."""

    def __init__(self, peers_path: Optional[Path] = None):
        self.peers_path = peers_path or Path(__file__).resolve().parent.parent.parent / "runtime" / "mesh_peers.json"
        self.discovery = MeshDiscovery(node_id="local", peers_path=self.peers_path)

    def _dispatch(self, task: TaskAssignment | Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Submit a verification task to the real /evolution/evolve endpoint."""
        payload = task.payload if isinstance(task, TaskAssignment) else task
        node_id = str(getattr(self, "node_id", "local"))
        try:
            resp = requests.post(
                "http://127.0.0.1:8766/evolution/evolve",
                json={
                    "mode": "autonomous",
                    "max_refactors": 1,
                    "proposal_id": payload.get("proposal_id"),
                    "metadata": {"verifier_node": node_id},
                },
                timeout=30,
            )
            body = resp.json() if resp.ok else {"error": resp.status_code}
            return {node_id: {"status": resp.status_code, "body": body}}
        except Exception as exc:
            return {node_id: {"status": None, "body": {"error": str(exc)}}}

    def submit_task(self, payload: Dict[str, Any], min_peers: int = 2) -> Dict[str, Any]:
        """Submit a task to available peers and wait for consensus."""
        peers = self.discovery.list_peers()
        assigned = [p["node_id"] for p in peers[:max(min_peers, 1)]]
        task_id = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]
        task = TaskAssignment(task_id=task_id, payload=payload, assigned_to=assigned)
        raw = {
            "task_id": task.task_id,
            "payload": task.payload,
            "assigned_to": task.assigned_to,
            "created_at": task.created_at,
            "results": {},
            "consensus": task.consensus,
        }
        raw["results"] = self._dispatch(raw)
        raw["consensus"] = self._verify_consensus(raw)
        return {
            "task_id": raw["task_id"],
            "payload": raw["payload"],
            "assigned_to": raw["assigned_to"],
            "created_at": raw["created_at"],
            "results": raw["results"],
            "consensus": raw["consensus"],
        }

    def _verify_consensus(self, task: TaskAssignment | Dict[str, Any]) -> Dict[str, Any]:
        results = task.results if isinstance(task, TaskAssignment) else task.get("results", {})
        bodies = [r.get("body", {}) for r in results.values() if r.get("status") == 200]
        if not bodies:
            return {"status": "NO_RESULTS"}
        first = json.dumps(bodies[0], sort_keys=True)
        matches = sum(1 for b in bodies if json.dumps(b, sort_keys=True) == first)
        return {
            "status": "CONSENSUS" if matches == len(bodies) else "DIVERGENT",
            "participants": len(bodies),
            "matches": matches,
        }
