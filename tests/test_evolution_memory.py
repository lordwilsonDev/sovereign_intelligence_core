from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from msb_v2.evolution.memory import EvolutionMemory
from msb_v2.evolution.proposal import EvolutionProposal


def _make_proposal(proposal_id: str, title: str, affected_modules=None, risk: str = "medium", status: str = "proposed", failure_reason: str | None = None) -> EvolutionProposal:
    return EvolutionProposal(
        proposal_id=proposal_id,
        title=title,
        affected_modules=affected_modules or ["msb_v2/evolution/scanner.py"],
        rationale="test rationale",
        risk=risk,
        status=status,
        failure_reason=failure_reason,
    )


def test_record_and_all(tmp_path: Path) -> None:
    db = tmp_path / "evolution_memory.db"
    memory = EvolutionMemory(db)
    proposal = _make_proposal("ev-mem-1", "title")
    memory.record(proposal)
    rows = memory.all()
    assert len(rows) == 1
    assert rows[0]["proposal_id"] == "ev-mem-1"
    assert rows[0]["target"] == "msb_v2/evolution/scanner.py"
    assert rows[0]["status"] == "proposed"


def test_should_skip_blocks_repeat_failures(tmp_path: Path) -> None:
    memory = EvolutionMemory(tmp_path / "evolution_memory.db")
    payload = {
      "proposal_id": "prop-1",
      "title": "tune scanner",
      "affected_modules": ["msb_v2/evolution/scanner.py"],
      "rationale": "reduce false positives\n\nScanner findings:\n{}",
      "risk": "medium",
    }
    fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    proposal = EvolutionProposal(**payload, status="failed", failure_reason="simulated")
    memory.record(proposal, target="msb_v2/evolution/scanner.py", fingerprint=fingerprint)
    assert memory.should_skip("msb_v2/evolution/scanner.py", fingerprint) is True


def test_should_skip_allows_new_target(tmp_path: Path) -> None:
    memory = EvolutionMemory(tmp_path / "evolution_memory.db")
    payload = {
      "proposal_id": "prop-2",
      "title": "tune scanner",
      "affected_modules": ["msb_v2/evolution/scanner.py"],
      "rationale": "reduce false positives\n\nScanner findings:\n{}",
      "risk": "medium",
    }
    fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    proposal = EvolutionProposal(**payload, status="failed", failure_reason="simulated")
    memory.record(proposal, target="msb_v2/evolution/scanner.py", fingerprint=fingerprint)
    assert memory.should_skip("msb_v2/bar.py", fingerprint) is False


def test_get_roundtrip(tmp_path: Path) -> None:
    memory = EvolutionMemory(tmp_path / "evolution_memory.db")
    proposal = _make_proposal("ev-mem-4", "title", status="completed")
    memory.record(proposal)
    got = memory.get("ev-mem-4")
    assert got is not None
    assert got.proposal_id == "ev-mem-4"
    assert got.status == "completed"
    assert memory.get("missing") is None


def test_history_records(tmp_path: Path) -> None:
    memory = EvolutionMemory(tmp_path / "evolution_memory.db")
    proposal = _make_proposal("ev-mem-5", "title")
    memory.record(proposal)
    history = memory.history("ev-mem-5")
    assert history[0]["event"] == "recorded"
