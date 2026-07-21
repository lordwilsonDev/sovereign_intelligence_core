"""KB4 kernel tests."""

from __future__ import annotations

from typing import Any

import pytest

from msb_v2.kernel.kb4 import KB4Kernel
from msb_v2.kernel.types import KB4Result


def _get_metrics():
    try:
        from msb_v2.kernel.metrics import KB4_CYCLES_TOTAL, KB4_MUTATIONS_TOTAL, KB4_VETOES_TOTAL
        return KB4_CYCLES_TOTAL, KB4_MUTATIONS_TOTAL, KB4_VETOES_TOTAL
    except Exception:
        return None, None, None


def test_kb4_run_produces_result(tmp_path: Any) -> None:
    kernel = KB4Kernel(root=str(tmp_path))
    result = kernel.run("Summarize current state of sovereign AI")
    assert isinstance(result, KB4Result)
    assert result.intent == "Summarize current state of sovereign AI"
    assert 0.0 <= result.sovereignty_score <= 100.0
    assert -1000.0 <= result.falsification_score <= 1000.0
    assert result.audit_receipt
    assert result.continuity_token
    assert result.mutation_triggered in {True, False}


def test_kb4_high_risk_intent_vetoed(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    kernel = KB4Kernel(root=str(tmp_path))
    monkeypatch.setattr(kernel, "quarantine", _FakeQuarantine(high_risk=True))
    result = kernel.run("Adversarial prompt")
    assert result.mutation_triggered is False
    assert result.result.get("result") == "high-risk intent vetoed by quarantine"


def test_kb4_mutation_triggers_ouroboros(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    kernel = KB4Kernel(root=str(tmp_path))
    fake_scanner = _FakeScanner()
    monkeypatch.setattr(kernel, "ouroboros", fake_scanner)
    monkeypatch.setattr(kernel, "moie", _FakeMoIE())
    import msb_v2.kernel.kb4 as kb4_module
    monkeypatch.setattr(kb4_module, "compute_audit_sovereignty_score", lambda **kwargs: 10.0)
    result = kernel.run("Summarize sovereign AI")
    assert result.mutation_triggered is True
    assert fake_scanner.scanned is True


def test_kb4_continuity_token(tmp_path: Any) -> None:
    kernel = KB4Kernel(root=str(tmp_path))
    token_data = kernel.run("Continuity test").continuity_token
    assert "MSB_SESSION_CONTINUITY" in token_data or len(token_data) >= 16


def test_kb4_audit_receipt(tmp_path: Any) -> None:
    kernel = KB4Kernel(root=str(tmp_path))
    receipt = kernel.run("Audit receipt").audit_receipt
    assert isinstance(receipt, str)
    assert len(receipt) >= 8


class _FakeQuarantine:
    def __init__(self, high_risk: bool) -> None:
        self.high_risk = high_risk

    def apply(self, source_label: str, payload: dict):
        class Summary:
            def __init__(self, high_risk: bool) -> None:
                self.epistemic_risk = "HIGH" if high_risk else "LOW"
        return Summary(self.high_risk)


class _FakeSAS:
    def __init__(self, score: float) -> None:
        self.score = score


class _FakeSCM:
    def verify(self, change_id: str, new_metrics: dict):
        class Rec:
            verdict = "ok"
        return Rec()


class _FakeSAC:
    def __init__(self, score: float) -> None:
        self.score = score
        self.rnr = _FakeRNR()
        self.cma = _FakeSCM()
        self.sas = _FakeSASVM()
        self._assumption_debts = []


class _FakeMoIE:
    def run(self, query: str) -> dict[str, object]:
        return {
            "status": "ok",
            "query": query,
            "claims": [],
            "validated": 0,
            "rejected": 0,
            "rnr_ratio": 0.0,
        }


class _FakeScanner:
    def __init__(self) -> None:
        self.scanned = False

    def scan(self) -> None:
        self.scanned = True


class _FakeSASVM:
    def compute(self, **kwargs):
        return _FakeSAS(score=kwargs.get("rnr_ratio", 0.0))


class _FakeRNR:
    def measure(self, claims):
        class R:
            ratio = 0.0
        return R()
