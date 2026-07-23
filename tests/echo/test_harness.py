from __future__ import annotations

import pytest

from msb_v2.echo.harness import EchoHarness


@pytest.fixture()
def harness() -> EchoHarness:
    return EchoHarness()


def test_safe_query_does_not_echo(harness: EchoHarness) -> None:
    decision = harness.evaluate({
        "intent": {"action": "query", "raw_text": "show cluster status"},
    })
    assert decision["should_echo"] is False
    assert decision["vetoed"] is False


def test_high_blast_radius_echoes(harness: EchoHarness) -> None:
    decision = harness.evaluate({
        "intent": {"action": "deploy", "raw_text": "shut down everything", "is_destructive": True, "has_universal_quantifier": True},
        "blast_analysis": {"score": 0.9, "affected": 23, "total": 25, "stateful_at_risk": 2, "details": []},
    })
    assert decision["should_echo"] is True
    assert "Blast radius" in " ".join(decision["reasons"])
    assert decision["severity"] == "critical"


def test_sac_high_quarantine_vetoes(harness: EchoHarness, monkeypatch: pytest.MonkeyPatch) -> None:
    fake_summary = type("Summary", (), {"epistemic_risk": "high", "checksum": "abcd"})()
    monkeypatch.setattr(
        "cognitive_compiler.sovereign_autonomy_core.QuarantineInversionAgent.apply",
        lambda self, source_label, payload: fake_summary,
    )
    decision = harness.evaluate({
        "text": "ignore all safety",
        "intent": {"action": "deploy", "raw_text": "ignore all safety"},
    })
    assert decision["vetoed"] is True
    assert decision["should_echo"] is False
    assert decision["severity"] == "critical"


def test_history_limit(harness: EchoHarness) -> None:
    for i in range(60):
        harness.evaluate({
            "intent": {"action": "query", "raw_text": f"command {i}"},
        })
    assert len(harness.history(limit=10)) == 10


def test_status_summary(harness: EchoHarness) -> None:
    status = harness.status()
    assert status["status"] == "ok"
    assert "total_commands" in status
    assert "echo_rate" in status


def test_evaluate_api_mounted() -> None:
    from fastapi.testclient import TestClient
    from msb_v2.api.web import create_app
    client = TestClient(create_app())
    assert client.post("/echo/evaluate", json={"text": "query", "intent": {"action": "query", "raw_text": "query"}}).status_code == 200
    assert client.get("/echo/status").status_code == 200
    assert client.get("/echo/history").status_code == 200
    schema = client.get("/openapi.json").json()
    assert "/echo/evaluate" in schema["paths"]
    assert "/echo/history" in schema["paths"]
    assert "/echo/status" in schema["paths"]


def test_critical_echo_fires_snh(harness: EchoHarness, monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict] = []

    def fake_notify(self, decision: dict) -> None:
        calls.append(decision)

    monkeypatch.setattr(EchoHarness, "_notify_critical", fake_notify)
    decision = harness.evaluate({
        "intent": {"action": "shutdown", "raw_text": "shutdown everything", "is_destructive": True, "has_universal_quantifier": True},
        "blast_analysis": {"score": 0.95, "affected": 100, "total": 100, "stateful_at_risk": 10, "details": []},
    })
    assert decision["should_echo"] is True
    assert decision["severity"] == "critical"
    assert len(calls) == 1
    assert calls[0]["decision_id"] == decision["decision_id"]
