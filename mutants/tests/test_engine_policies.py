from __future__ import annotations

from msb_v2.engine.execution_policy import ExecutionPolicy
from msb_v2.engine.failure_recovery import FailureMode, FailureRecovery


def test_execution_policy_classifies_safe_actions() -> None:
    policy = ExecutionPolicy(require_approval=True)
    result = policy.classify("read config file")
    assert result.type.value == "read"
    assert result.requires_approval is True


def test_execution_policy_blocks_dangerous_patterns() -> None:
    policy = ExecutionPolicy(require_approval=True)
    result = policy.classify("run sudo rm -rf /tmp")
    assert result.type.value == "blocked"


def test_failure_recovery_for_execution_retries() -> None:
    recovery = FailureRecovery()
    mode = FailureMode(error="null pointer", phase="execution")
    assert recovery.fallback_for(mode) == "retry_with_evidence_check"


def test_failure_recovery_for_context_requests_minimal() -> None:
    recovery = FailureRecovery()
    mode = FailureMode(error="missing token", phase="context")
    assert recovery.fallback_for(mode) == "request_minimal_context"


def test_failure_recovery_default_aborts() -> None:
    recovery = FailureRecovery()
    mode = FailureMode(error="weird thing", phase="unknown")
    assert recovery.fallback_for(mode) == "safe_abort"
