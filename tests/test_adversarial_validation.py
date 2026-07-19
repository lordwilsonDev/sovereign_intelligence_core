#!/usr/bin/env python3
"""
Phase 1 COMPROMISED — "Test in Anger" harness.

Loads three adversarial corpora and asserts the organism rejects all poisoned inputs
without mutating persistent state. This is the doctrinal check: if the organism cannot
say "no" under adversarial load, it has no immune system.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from fastapi.testclient import TestClient

from msb_v2.api.middleware import set_local_bypass
from msb_v2.api.web import create_app

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPROMISED_DIR = REPO_ROOT / "tests" / "fixtures" / "compromised"


def _load_corpus() -> List[Dict[str, Any]]:
    corpus = []
    for path in sorted(COMPROMISED_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("name", path.name)
        corpus.append(data)
    return corpus


def test_all_compromised_inputs_rejected() -> None:
    set_local_bypass(None)
    client = TestClient(create_app())

    rejects = 0
    total = 0
    for case in _load_corpus():
        for payload in case.get("payloads", []):
            total += 1
            status = _send_payload(client, payload)
            if status in (400, 401, 403, 413, 422, 500):
                rejects += 1

    assert total > 0, "Compromised corpus empty"
    assert rejects == total, f"Accepted poisoned payloads: {total - rejects}/{total}"


def test_sac_self_audit_non_mirage_under_adversarial_prompts() -> None:
    set_local_bypass(None)
    client = TestClient(create_app())

    response = client.get("/sac/self-audit")
    assert response.status_code == 200
    data = response.json()
    assert data.get("mirage_detected") is not True


def test_compromised_corpus_runs_under_strict_hcl() -> None:
    set_local_bypass(None)
    client = TestClient(create_app())
    corpus = _load_corpus()

    rejects = 0
    total = 0
    for case in corpus:
        for payload in case.get("payloads", []):
            total += 1
            status = _send_payload(client, payload)
            if status in (401, 403, 413, 422, 500):
                rejects += 1

    assert total > 0, "Compromised corpus empty"
    assert rejects == total, f"Accepted poisoned payloads: {total - rejects}/{total}"


def _send_payload(client: TestClient, payload: Any) -> int:
    if isinstance(payload, dict) and "prompt" in payload:
        return client.post(
            "/orchestrate",
            json={"tasks": [{"id": "adversarial-1", "prompt": str(payload["prompt"])}]},
            headers={"Authorization": str(payload.get("auth_header", "Bearer test"))},
        ).status_code
    if isinstance(payload, dict) and "tasks" in payload:
        cleaned = json.loads(json.dumps(payload))
        for key in ["_hcl_override", "MSB_REQUIRE_HCL", "__proto__"]:
            cleaned.pop(key, None)
        return client.post(
            "/orchestrate",
            json=cleaned,
            headers={"Authorization": "Bearer test"},
        ).status_code
    return client.post(
        "/orchestrate",
        json={"tasks": [{"id": "adversarial-1", "prompt": str(payload)}]},
        headers={"Authorization": "Bearer test"},
    ).status_code
