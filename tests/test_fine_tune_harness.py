from __future__ import annotations

import contextlib
import os

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app
from msb_v2.api.middleware import set_local_bypass as _set_local_bypass


@contextlib.contextmanager
def _client_with_bypass():
    client = TestClient(create_app())
    _set_local_bypass(True)
    try:
        yield client
    finally:
        _set_local_bypass(False)


def test_fine_tune_scan_requires_bearer_token(tmp_path) -> None:
    (tmp_path / "doc.txt").write_text("alpha beta gamma", encoding="utf-8")
    client = TestClient(create_app())
    _set_local_bypass(False)
    try:
        r = client.post("/fine-tune/scan", json={"repo_path": str(tmp_path), "privacy_boundary": "local-only"})
    finally:
        _set_local_bypass(None)
    assert r.status_code != 200


def test_fine_tune_scan_returns_readiness_report(tmp_path) -> None:
    with _client_with_bypass() as client:
        (tmp_path / "doc.txt").write_text("alpha beta gamma", encoding="utf-8")
        r = client.post("/fine-tune/scan", json={"repo_path": str(tmp_path), "privacy_boundary": "local-only"})
        assert r.status_code == 200
        body = r.json()
        assert body["document_count"] >= 1
        assert body["recommendation"] in {"proceed", "clean", "abort"}


def test_fine_tune_distill_requires_bearer_token(tmp_path) -> None:
    (tmp_path / "doc.txt").write_text("alpha beta gamma", encoding="utf-8")
    client = TestClient(create_app())
    _set_local_bypass(False)
    try:
        r = client.post("/fine-tune/distill", json={"repo_path": str(tmp_path), "max_pairs": 2})
    finally:
        _set_local_bypass(None)
    assert r.status_code != 200


def test_fine_tune_distill_returns_validation(tmp_path) -> None:
    with _client_with_bypass() as client:
        (tmp_path / "doc.txt").write_text("alpha beta gamma", encoding="utf-8")
        r = client.post("/fine-tune/distill", json={"repo_path": str(tmp_path), "max_pairs": 2})
        assert r.status_code == 200
        body = r.json()
        assert body["pairs_generated"] >= 1
        assert "validation" in body


def test_fine_tune_train_requires_bearer_token(tmp_path) -> None:
    (tmp_path / "doc.txt").write_text("alpha beta gamma", encoding="utf-8")
    client = TestClient(create_app())
    _set_local_bypass(False)
    try:
        r = client.post("/fine-tune/train", json={"repo_path": str(tmp_path), "base_model": "local-base"})
    finally:
        _set_local_bypass(None)
    assert r.status_code != 200


def test_fine_tune_train_returns_integration_report(tmp_path) -> None:
    with _client_with_bypass() as client:
        (tmp_path / "doc.txt").write_text("alpha beta gamma", encoding="utf-8")
        r = client.post("/fine-tune/train", json={"repo_path": str(tmp_path), "base_model": "local-base"})
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "completed"
        report = body["integration_report"]
        assert report["validation_passed"] is True
        assert "falsification_condition" in report
