"""Cross-Node Task Verification tests."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from msb_v2.evolution.cross_node_verification import CrossNodeVerification


@pytest.fixture()
def engine(tmp_path: Path):
    peers = tmp_path / "mesh_peers.json"
    peers.write_text(json.dumps({"peers": [
        {"node_id": "p1", "address": "127.0.0.1", "port": 8766},
        {"node_id": "p2", "address": "127.0.0.1", "port": 8766},
    ]}, indent=2))
    with patch("msb_v2.evolution.cross_node_verification.MeshDiscovery") as mock_disc:
        instance = mock_disc.return_value
        instance.list_peers.return_value = [
            {"node_id": "p1", "address": "127.0.0.1", "port": 8766},
            {"node_id": "p2", "address": "127.0.0.1", "port": 8766},
        ]
        yield CrossNodeVerification(peers_path=peers)


def test_submit_task_returns_task_id(engine: CrossNodeVerification) -> None:
    with patch("msb_v2.evolution.cross_node_verification.requests.post") as mock_post:
        mock_post.return_value.ok = True
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ok": True}
        result = engine.submit_task({"action": "ping"})
    assert result["task_id"]
    assert result["consensus"]["status"] in ("CONSENSUS", "NO_RESULTS", "DIVERGENT")


def test_consensus_detects_divergence(engine: CrossNodeVerification) -> None:
    from msb_v2.evolution.cross_node_verification import TaskAssignment
    task = TaskAssignment(task_id="div", payload={}, assigned_to=["p1", "p2"])
    task.results = {
        "p1": {"status": 200, "body": {"v": 1}},
        "p2": {"status": 200, "body": {"v": 2}},
    }
    consensus = engine._verify_consensus(task)
    assert consensus["status"] == "DIVERGENT"


def test_consensus_detects_no_results(engine: CrossNodeVerification) -> None:
    from msb_v2.evolution.cross_node_verification import TaskAssignment
    task = TaskAssignment(task_id="empty", payload={}, assigned_to=["p1"])
    task.results = {"p1": {"status": 500, "body": {"error": 500}}}
    consensus = engine._verify_consensus(task)
    assert consensus["status"] == "NO_RESULTS"
