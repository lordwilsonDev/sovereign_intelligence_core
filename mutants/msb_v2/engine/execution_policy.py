from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class ActionType(str, Enum):
    READ = "read"
    WRITE = "write"
    DANGEROUS = "dangerous"
    BLOCKED = "blocked"


@dataclass
class ClassifiedAction:
    action: str
    type: ActionType
    requires_approval: bool = True
    reason: str = ""
mutants_xǁExecutionPolicyǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁExecutionPolicyǁclassify__mutmut: MutantDict = {}  # type: ignore


class ExecutionPolicy:
    @_mutmut_mutated(mutants_xǁExecutionPolicyǁ__init____mutmut)
    def __init__(self, require_approval: bool = False) -> None:
        self.require_approval = require_approval
        self.blocked_patterns = ["rm -rf /", "sudo rm"]
    def xǁExecutionPolicyǁ__init____mutmut_orig(self, require_approval: bool = False) -> None:
        self.require_approval = require_approval
        self.blocked_patterns = ["rm -rf /", "sudo rm"]
    def xǁExecutionPolicyǁ__init____mutmut_1(self, require_approval: bool = True) -> None:
        self.require_approval = require_approval
        self.blocked_patterns = ["rm -rf /", "sudo rm"]
    def xǁExecutionPolicyǁ__init____mutmut_2(self, require_approval: bool = False) -> None:
        self.require_approval = None
        self.blocked_patterns = ["rm -rf /", "sudo rm"]
    def xǁExecutionPolicyǁ__init____mutmut_3(self, require_approval: bool = False) -> None:
        self.require_approval = require_approval
        self.blocked_patterns = None
    def xǁExecutionPolicyǁ__init____mutmut_4(self, require_approval: bool = False) -> None:
        self.require_approval = require_approval
        self.blocked_patterns = ["XXrm -rf /XX", "sudo rm"]
    def xǁExecutionPolicyǁ__init____mutmut_5(self, require_approval: bool = False) -> None:
        self.require_approval = require_approval
        self.blocked_patterns = ["RM -RF /", "sudo rm"]
    def xǁExecutionPolicyǁ__init____mutmut_6(self, require_approval: bool = False) -> None:
        self.require_approval = require_approval
        self.blocked_patterns = ["rm -rf /", "XXsudo rmXX"]
    def xǁExecutionPolicyǁ__init____mutmut_7(self, require_approval: bool = False) -> None:
        self.require_approval = require_approval
        self.blocked_patterns = ["rm -rf /", "SUDO RM"]

    @_mutmut_mutated(mutants_xǁExecutionPolicyǁclassify__mutmut)
    def classify(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_orig(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_1(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern not in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_2(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=None,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_3(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=None,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_4(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=None,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_5(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=None,
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_6(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_7(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_8(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_9(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_10(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=False,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_11(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=None, type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_12(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=None, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_13(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, requires_approval=None)

    def xǁExecutionPolicyǁclassify__mutmut_14(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(type=ActionType.READ, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_15(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, requires_approval=self.require_approval)

    def xǁExecutionPolicyǁclassify__mutmut_16(self, action: str) -> ClassifiedAction:
        for pattern in self.blocked_patterns:
            if pattern in action:
                return ClassifiedAction(
                    action=action,
                    type=ActionType.BLOCKED if self.require_approval else ActionType.DANGEROUS,
                    requires_approval=True,
                    reason=f"blocked pattern: {pattern}",
                )
        return ClassifiedAction(action=action, type=ActionType.READ, )

mutants_xǁExecutionPolicyǁ__init____mutmut['_mutmut_orig'] = ExecutionPolicy.xǁExecutionPolicyǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁ__init____mutmut['xǁExecutionPolicyǁ__init____mutmut_1'] = ExecutionPolicy.xǁExecutionPolicyǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁ__init____mutmut['xǁExecutionPolicyǁ__init____mutmut_2'] = ExecutionPolicy.xǁExecutionPolicyǁ__init____mutmut_2 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁ__init____mutmut['xǁExecutionPolicyǁ__init____mutmut_3'] = ExecutionPolicy.xǁExecutionPolicyǁ__init____mutmut_3 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁ__init____mutmut['xǁExecutionPolicyǁ__init____mutmut_4'] = ExecutionPolicy.xǁExecutionPolicyǁ__init____mutmut_4 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁ__init____mutmut['xǁExecutionPolicyǁ__init____mutmut_5'] = ExecutionPolicy.xǁExecutionPolicyǁ__init____mutmut_5 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁ__init____mutmut['xǁExecutionPolicyǁ__init____mutmut_6'] = ExecutionPolicy.xǁExecutionPolicyǁ__init____mutmut_6 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁ__init____mutmut['xǁExecutionPolicyǁ__init____mutmut_7'] = ExecutionPolicy.xǁExecutionPolicyǁ__init____mutmut_7 # type: ignore # mutmut generated

mutants_xǁExecutionPolicyǁclassify__mutmut['_mutmut_orig'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_orig # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_1'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_1 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_2'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_2 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_3'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_3 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_4'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_4 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_5'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_5 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_6'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_6 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_7'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_7 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_8'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_8 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_9'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_9 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_10'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_10 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_11'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_11 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_12'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_12 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_13'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_13 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_14'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_14 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_15'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_15 # type: ignore # mutmut generated
mutants_xǁExecutionPolicyǁclassify__mutmut['xǁExecutionPolicyǁclassify__mutmut_16'] = ExecutionPolicy.xǁExecutionPolicyǁclassify__mutmut_16 # type: ignore # mutmut generated
