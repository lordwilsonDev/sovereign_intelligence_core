from __future__ import annotations

import os

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


def test_fine_tune_scan_returns_readiness_report(tmp_path) -> None:
    client = TestClient(create_app())
    (tmp_path / "doc.txt").write_text("alpha beta gamma", encoding="utf-8")
    r = client.post("/fine-tune/scan", json={"repo_path": str(tmp_path), "privacy_boundary": "local-only"})
    assert r.status_code == 200
    body = r.json()
    assert body["document_count"] >= 1
    assert body["recommendation"] in {"proceed", "clean", "abort"}


def test_fine_tune_distill_returns_validation(tmp_path) -> None:
    client = TestClient(create_app())
    (tmp_path / "doc.txt").write_text("alpha beta gamma", encoding="utf-8")
    r = client.post("/fine-tune/distill", json={"repo_path": str(tmp_path), "max_pairs": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["pairs_generated"] >= 1
    assert "validation" in body


def test_fine_tune_train_returns_integration_report(tmp_path) -> None:
    client = TestClient(create_app())
    (tmp_path / "doc.txt").write_text("alpha beta gamma", encoding="utf-8")
    r = client.post("/fine-tune/train", json={"repo_path": str(tmp_path), "base_model": "local-base"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "completed"
    report = body["integration_report"]
    assert report["validation_passed"] is True
    assert "falsification_condition" in report
