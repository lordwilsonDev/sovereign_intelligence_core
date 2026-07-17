from __future__ import annotations

from dataclasses import dataclass


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@dataclass
class FailureMode:
    error: str
    phase: str
    next_action: str = "abort"
mutants_xǁFailureRecoveryǁfallback_for__mutmut: MutantDict = {}  # type: ignore


class FailureRecovery:
    @_mutmut_mutated(mutants_xǁFailureRecoveryǁfallback_for__mutmut)
    def fallback_for(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "retry_with_evidence_check"
        if mode.phase == "context":
            return "request_minimal_context"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_orig(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "retry_with_evidence_check"
        if mode.phase == "context":
            return "request_minimal_context"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_1(self, mode: FailureMode) -> str:
        if mode.phase != "execution":
            return "retry_with_evidence_check"
        if mode.phase == "context":
            return "request_minimal_context"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_2(self, mode: FailureMode) -> str:
        if mode.phase == "XXexecutionXX":
            return "retry_with_evidence_check"
        if mode.phase == "context":
            return "request_minimal_context"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_3(self, mode: FailureMode) -> str:
        if mode.phase == "EXECUTION":
            return "retry_with_evidence_check"
        if mode.phase == "context":
            return "request_minimal_context"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_4(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "XXretry_with_evidence_checkXX"
        if mode.phase == "context":
            return "request_minimal_context"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_5(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "RETRY_WITH_EVIDENCE_CHECK"
        if mode.phase == "context":
            return "request_minimal_context"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_6(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "retry_with_evidence_check"
        if mode.phase != "context":
            return "request_minimal_context"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_7(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "retry_with_evidence_check"
        if mode.phase == "XXcontextXX":
            return "request_minimal_context"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_8(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "retry_with_evidence_check"
        if mode.phase == "CONTEXT":
            return "request_minimal_context"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_9(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "retry_with_evidence_check"
        if mode.phase == "context":
            return "XXrequest_minimal_contextXX"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_10(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "retry_with_evidence_check"
        if mode.phase == "context":
            return "REQUEST_MINIMAL_CONTEXT"
        return "safe_abort"
    def xǁFailureRecoveryǁfallback_for__mutmut_11(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "retry_with_evidence_check"
        if mode.phase == "context":
            return "request_minimal_context"
        return "XXsafe_abortXX"
    def xǁFailureRecoveryǁfallback_for__mutmut_12(self, mode: FailureMode) -> str:
        if mode.phase == "execution":
            return "retry_with_evidence_check"
        if mode.phase == "context":
            return "request_minimal_context"
        return "SAFE_ABORT"

mutants_xǁFailureRecoveryǁfallback_for__mutmut['_mutmut_orig'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_orig # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_1'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_1 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_2'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_2 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_3'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_3 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_4'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_4 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_5'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_5 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_6'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_6 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_7'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_7 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_8'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_8 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_9'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_9 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_10'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_10 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_11'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_11 # type: ignore # mutmut generated
mutants_xǁFailureRecoveryǁfallback_for__mutmut['xǁFailureRecoveryǁfallback_for__mutmut_12'] = FailureRecovery.xǁFailureRecoveryǁfallback_for__mutmut_12 # type: ignore # mutmut generated
