from __future__ import annotations

from msb_v2.engine.inversion_engine import InversionEngine, InversionResult
from msb_v2.engine.goal_binding import GoalBinding
from msb_v2.engine.priority_decay import PriorityDecay, PriorityScore
from msb_v2.engine.causal_memory import CausalMemory
from msb_v2.engine.execution_policy import ExecutionPolicy, ActionType
from msb_v2.engine.failure_recovery import FailureRecovery, FailureMode
from msb_v2.engine.learning_fingerprint import LearningFingerprint


def test_inversion_engine_produces_scored_output():
    engine = InversionEngine()
    result = engine.invert("local-only deployment is safer")
    assert isinstance(result, InversionResult)
    assert result.inversion == "not(local-only deployment is safer)"
    assert "consequences" in result.scored_output


def test_goal_binding_checksum_changes_on_edit():
    binding = GoalBinding.create("ship v2", ["ship msb-v2 by friday"])
    first = binding.checksum()
    binding.constraints.append("no downtime")
    assert binding.checksum() != first


def test_priority_decay_scores_higher_for_urgent():
    PriorityDecay()
    a = PriorityScore("a", urgency=0.9, impact=0.1)
    b = PriorityScore("b", urgency=0.1, impact=0.9)
    assert a.composite() >= b.composite()


def test_causal_memory_links_cycles():
    mem = CausalMemory()
    mem.link("c1", "c2", relation="enabled")
    assert mem.has_link("c1", "c2")
    assert not mem.has_link("c2", "c1")


def test_execution_policy_blocks_dangerous_without_approval():
    policy = ExecutionPolicy(require_approval=False)
    action = policy.classify("rm -rf /")
    assert action.type == ActionType.DANGEROUS


def test_failure_recovery_fallback_is_safer():
    recovery = FailureRecovery()
    mode = FailureMode(error="connection refused", phase="execution")
    fallback = recovery.fallback_for(mode)
    assert fallback == "retry_with_evidence_check"


def test_learning_fingerprint_prevents_identical_loops():
    fp = LearningFingerprint()
    fp.record("goal1", "hypothesis1")
    assert fp.is_novel("goal1", "hypothesis2")
    assert not fp.is_novel("goal1", "hypothesis1")
