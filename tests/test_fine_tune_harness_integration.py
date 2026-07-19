from __future__ import annotations

import os

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_unsloth_availability_exposed_on_scan(tmp_path) -> None:
    client = TestClient(create_app())
    (tmp_path / "doc.txt").write_text("alpha beta gamma", encoding="utf-8")
    response = client.post("/fine-tune/scan", json={"repo_path": str(tmp_path), "privacy_boundary": "local-only"})
    assert response.status_code == 200
    body = response.json()
    assert body["document_count"] >= 1
    assert body["recommendation"] in {"proceed", "clean", "abort"}
