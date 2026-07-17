from __future__ import annotations

from typing import Any, Dict

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_cognitive_ping() -> None:
    resp = client.get("/cognitive/ping")
    assert resp.status_code == 200
    payload: Dict[str, Any] = resp.json()
    assert payload["status"] == "ok"
    assert payload["module"] == "cognitive"


def test_mesh_negotiate_returns_adjacency() -> None:
    payload: Dict[str, Any] = client.post("/cognitive/mesh/negotiate", json={"peers": ["alpha", "beta"]}).json()
    assert payload["status"] == "ok"
    assert payload["mesh"] is True
    assert payload["adjacency"]["alpha"] == ["beta"]


def test_chronos_checkpoint_returns_root_hash() -> None:
    payload: Dict[str, Any] = client.post("/cognitive/chronos/checkpoint", json={"label": "test"}).json()
    assert payload["status"] == "ok"
    assert "root" in payload
    assert payload["label"] == "test"


def test_provenance_build_returns_root() -> None:
    payload: Dict[str, Any] = client.post("/cognitive/provenance/build").json()
    assert payload["status"] == "ok"
    assert "root" in payload
    assert "links" in payload


def test_redteam_run_returns_findings() -> None:
    payload: Dict[str, Any] = client.post("/cognitive/redteam/run").json()
    assert payload["status"] == "ok"
    assert "allowed" in payload
    assert isinstance(payload["redactions"], int)


def test_semantic_snapshot_returns_tools() -> None:
    payload: Dict[str, Any] = client.post("/cognitive/semantic/snapshot").json()
    assert payload["status"] == "ok"
    assert "available_tools" in payload
