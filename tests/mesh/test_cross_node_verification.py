"""Cross-Node Verification dispatch regression tests."""
from __future__ import annotations

import pytest

from msb_v2.evolution.cross_node_verification import CrossNodeVerification


def test_dispatch_hits_real_evolve_endpoint(monkeypatch):
    """_dispatch should call /evolution/evolve with the correct payload."""
    requests = pytest.importorskip("requests")
    verifier = CrossNodeVerification()

    captured_url = None
    captured_json = None

    class MockResponse:
        def __init__(self):
            self.status_code = 200
            self.ok = True
        def json(self):
            return {"status": "applied", "proposal_id": "test-proposal"}

    def mock_post(url, json, timeout):
        nonlocal captured_url, captured_json
        captured_url = url
        captured_json = json
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)

    result = verifier._dispatch({"proposal_id": "test-proposal"})
    assert result["local"]["status"] == 200
    assert captured_url == "http://127.0.0.1:8766/evolution/evolve"
    assert captured_json["mode"] == "autonomous"
    assert captured_json["proposal_id"] == "test-proposal"
