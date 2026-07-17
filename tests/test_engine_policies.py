from __future__ import annotations

from msb_v2.engine.execution_policy import ActionType, CapabilityBoundary, ExecutionPolicy
from msb_v2.engine.failure_recovery import FailureMode, FailureRecovery


def test_execution_policy_classifies_execute_prefix() -> None:
    policy = ExecutionPolicy(require_approval=False)
    result = policy.classify("run echo hello")
    assert result.type == ActionType.EXECUTE


def test_execution_policy_blocked_pattern_without_approval_is_dangerous() -> None:
    policy = ExecutionPolicy(require_approval=False)
    result = policy.classify("please run sudo rm -rf /tmp")
    assert result.type == ActionType.DANGEROUS


def test_execution_policy_blocked_pattern_with_approval_is_blocked() -> None:
    policy = ExecutionPolicy(require_approval=True)
    result = policy.classify("please run sudo rm -rf /tmp")
    assert result.type == ActionType.BLOCKED


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


def test_capability_boundary_blocks_execute_when_disabled() -> None:
    boundary = CapabilityBoundary(allow_exec=False, max_dangerous_per_min=10)
    assert boundary.is_allowed(ActionType.EXECUTE) is False
    assert boundary.is_allowed(ActionType.DANGEROUS) is False
    assert boundary.is_allowed(ActionType.READ) is True


def test_capability_boundary_allows_execute_within_quota() -> None:
    boundary = CapabilityBoundary(allow_exec=True, max_dangerous_per_min=2)
    assert boundary.is_allowed(ActionType.EXECUTE) is True
    assert boundary.is_allowed(ActionType.EXECUTE) is True
    assert boundary.is_allowed(ActionType.EXECUTE) is False
