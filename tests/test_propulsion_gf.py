from __future__ import annotations

import pytest

from fastapi.testclient import TestClient

from msb_v2.api.web import create_app
from msb_v3.validation.core.propulsion_engine import DiscoveryCandidate, PropulsionEngine


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_propulsion_evaluate_returns_scored_candidate(client: TestClient) -> None:
    payload = {
        "id": "p1",
        "problem": "Scientific discovery is slowing",
        "assumption": "More data improves progress",
        "inverse": "What if selectivity improves progress?",
        "novelty": 0.9,
        "explanatory_power": 0.8,
        "predictive_value": 0.8,
    }
    response = client.post("/validation/propulsion/evaluate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "scored" in body
    assert "ranked" in body
    scored = body["scored"]
    assert scored["id"] == "p1"
    assert isinstance(scored["score"], float)
    assert scored["score"] >= 0.0


def test_propulsion_ranked_returns_ordered_candidates() -> None:
    engine = PropulsionEngine()
    engine.evaluate(
        DiscoveryCandidate(
            id="low",
            problem="Low impact",
            assumption="A",
            inverse="B",
            novelty=0.1,
            explanatory_power=0.1,
            predictive_value=0.1,
            impact=0.1,
            cost=1.0,
            complexity=1.0,
            risk=1.0,
            timing=0.1,
            leverage=0.1,
        )
    )
    engine.evaluate(
        DiscoveryCandidate(
            id="high",
            problem="High impact",
            assumption="C",
            inverse="D",
            novelty=1.0,
            explanatory_power=1.0,
            predictive_value=1.0,
            impact=1.0,
            cost=0.1,
            complexity=0.1,
            risk=0.1,
            timing=1.0,
            leverage=1.0,
        )
    )
    ranked = engine.ranked()
    assert ranked[0]["id"] == "high"
    assert ranked[-1]["id"] == "low"
