from __future__ import annotations

from pathlib import Path

from evals.judges import Judges
from evals.oracle import Oracle
from evals.runner import EvalRunner


def test_eval_runner_deterministic():
    runner = EvalRunner()
    result = runner.run_deterministic("echo_exact", actual="hello", expected="hello")
    assert result.passed is True
    assert result.tier == "tier1_deterministic"


def test_eval_runner_semantic_judge():
    runner = EvalRunner()
    judge = Judges.llm_a_vs_b
    result = runner.run_semantic("summary_intent", output="Retrieved 3 memories about escort", expected_intent="retrieved memories", judge=judge)
    assert result.tier == "tier2_semantic"
    summary = runner.summary()
    assert summary["tier2_total"] >= 1


def test_oracle_writes_and_approves(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "config.yaml").write_text("greeting: hello\n")
    (repo / "proposals").mkdir()
    oracle = Oracle(repo=repo, proposals_dir=repo / "proposals", config_path=repo / "config.yaml")
    proposal = oracle.propose("tool_timeout", {"tool_timeout_ms": 5000})
    assert proposal.proposal_id
    assert (repo / "proposals" / f"{proposal.proposal_id}.json").exists()
    result = oracle.approve(proposal.proposal_id, commit=False)
    assert result["status"] == "ok"
