"""Axiom Library API mount tests."""
from __future__ import annotations

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app


def test_axiom_library_routes_mount() -> None:
    client = TestClient(create_app())
    assert client.get("/axiom-library/count").status_code == 200
    assert client.get("/axiom-library/recent").status_code == 200
    assert client.get("/axiom-library/random").status_code == 200
    assert client.get("/axiom-library/search").status_code == 200
    assert client.post("/axiom-library/ingest", json={"source":"s","axiom":"a","inversion":"i"}).status_code == 200
