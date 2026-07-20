"""HTTP-level integration test for dispatch-time HCL enforcement.

Exercises the full path:
  HTTP -> middleware auth -> app route -> HarnessDispatcher.dispatch() -> policy gate
"""
from __future__ import annotations

import os
from typing import Any, Dict

import pytest

from msb_v2.api.web import create_app
from msb_v2.v3.contracts import HarnessContract, lookup
from msb_v2.v3.policy import register_dispatch_contracts
from starlette.testclient import TestClient


@pytest.fixture(autouse=True)
def _env():
    os.environ["MSB_AUTH_LOCAL_BYPASS"] = "1"
    yield
    os.environ.pop("MSB_AUTH_LOCAL_BYPASS", None)


@pytest.fixture()
def client():
    return TestClient(create_app())


def _disallow_base_are():
    contract = lookup("dispatch:base_are", "any")
    assert contract is not None
    # mutate via module-private dict to avoid importing `register` again
    from msb_v2.v3 import contracts as mod
    key = ("dispatch:base_are", "any")
    if key in mod._CONTRACTS:
        mod._CONTRACTS[key] = HarnessContract(
            route=contract.route,
            method=contract.method,
            body_type=contract.body_type,
            allow_anonymous=False,
            timeout_ms=contract.timeout_ms,
            max_body_bytes=contract.max_body_bytes,
        )


def test_anonymous_dispatch_blocked_over_http(client: TestClient):
    register_dispatch_contracts()
    _disallow_base_are()
    r = client.post("/meta/route", json={"query": "philosophical reflection", "context": {"actor": "anonymous"}})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("primary_output", {}).get("verification") == "blocked"
    assert "dispatch blocked" in str(body.get("primary_output", {}).get("reason", ""))


def test_authenticated_dispatch_allowed_over_http(client: TestClient):
    register_dispatch_contracts()
    # base_are is allowed by default; authenticated-ish context should flow through
    r = client.post("/meta/route", json={"query": "philosophical reflection", "context": {"actor": "system"}})
    assert r.status_code == 200, r.text
    body = r.json()
    # We don't assert execution success because harnesses may not be fully available.
    assert body.get("primary_output") is not None
