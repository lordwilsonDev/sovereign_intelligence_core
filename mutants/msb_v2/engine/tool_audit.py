from __future__ import annotations

from dataclasses import dataclass
from typing import Any


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@dataclass
class ToolCallAudit:
    tool: str
    args_hash: str
    phase: str = ""
    allowed: bool = True
    blocked_reason: str = ""
    result_summary: str = ""
    timestamp: str = ""
mutants_xǁToolAuditǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁToolAuditǁrecord__mutmut: MutantDict = {}  # type: ignore
mutants_xǁToolAuditǁrecent__mutmut: MutantDict = {}  # type: ignore
mutants_xǁToolAuditǁblocked_count__mutmut: MutantDict = {}  # type: ignore


class ToolAudit:
    @_mutmut_mutated(mutants_xǁToolAuditǁ__init____mutmut)
    def __init__(self) -> None:
        self.entries: list[ToolCallAudit] = []
    def xǁToolAuditǁ__init____mutmut_orig(self) -> None:
        self.entries: list[ToolCallAudit] = []
    def xǁToolAuditǁ__init____mutmut_1(self) -> None:
        self.entries: list[ToolCallAudit] = None

    @_mutmut_mutated(mutants_xǁToolAuditǁrecord__mutmut)
    def record(self, **kwargs: Any) -> ToolCallAudit:
        entry = ToolCallAudit(**kwargs)
        self.entries.append(entry)
        return entry

    def xǁToolAuditǁrecord__mutmut_orig(self, **kwargs: Any) -> ToolCallAudit:
        entry = ToolCallAudit(**kwargs)
        self.entries.append(entry)
        return entry

    def xǁToolAuditǁrecord__mutmut_1(self, **kwargs: Any) -> ToolCallAudit:
        entry = None
        self.entries.append(entry)
        return entry

    def xǁToolAuditǁrecord__mutmut_2(self, **kwargs: Any) -> ToolCallAudit:
        entry = ToolCallAudit(**kwargs)
        self.entries.append(None)
        return entry

    @_mutmut_mutated(mutants_xǁToolAuditǁrecent__mutmut)
    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_orig(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_1(self, limit: int = 51) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_2(self, limit: int = 50) -> list[dict[str, Any]]:
        out = None
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_3(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[+limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_4(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                None
            )
        return out

    def xǁToolAuditǁrecent__mutmut_5(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "XXtoolXX": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_6(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "TOOL": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_7(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "XXargs_hashXX": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_8(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "ARGS_HASH": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_9(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "XXphaseXX": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_10(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "PHASE": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_11(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "XXallowedXX": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_12(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "ALLOWED": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_13(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "XXblocked_reasonXX": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_14(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "BLOCKED_REASON": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_15(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "XXresult_summaryXX": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_16(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "RESULT_SUMMARY": e.result_summary,
                    "timestamp": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_17(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "XXtimestampXX": e.timestamp,
                }
            )
        return out

    def xǁToolAuditǁrecent__mutmut_18(self, limit: int = 50) -> list[dict[str, Any]]:
        out = []
        for e in self.entries[-limit:]:
            out.append(
                {
                    "tool": e.tool,
                    "args_hash": e.args_hash,
                    "phase": e.phase,
                    "allowed": e.allowed,
                    "blocked_reason": e.blocked_reason,
                    "result_summary": e.result_summary,
                    "TIMESTAMP": e.timestamp,
                }
            )
        return out

    @_mutmut_mutated(mutants_xǁToolAuditǁblocked_count__mutmut)
    def blocked_count(self) -> int:
        return sum(1 for e in self.entries if not e.allowed)

    def xǁToolAuditǁblocked_count__mutmut_orig(self) -> int:
        return sum(1 for e in self.entries if not e.allowed)

    def xǁToolAuditǁblocked_count__mutmut_1(self) -> int:
        return sum(None)

    def xǁToolAuditǁblocked_count__mutmut_2(self) -> int:
        return sum(2 for e in self.entries if not e.allowed)

    def xǁToolAuditǁblocked_count__mutmut_3(self) -> int:
        return sum(1 for e in self.entries if e.allowed)

mutants_xǁToolAuditǁ__init____mutmut['_mutmut_orig'] = ToolAudit.xǁToolAuditǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁToolAuditǁ__init____mutmut['xǁToolAuditǁ__init____mutmut_1'] = ToolAudit.xǁToolAuditǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁToolAuditǁrecord__mutmut['_mutmut_orig'] = ToolAudit.xǁToolAuditǁrecord__mutmut_orig # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecord__mutmut['xǁToolAuditǁrecord__mutmut_1'] = ToolAudit.xǁToolAuditǁrecord__mutmut_1 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecord__mutmut['xǁToolAuditǁrecord__mutmut_2'] = ToolAudit.xǁToolAuditǁrecord__mutmut_2 # type: ignore # mutmut generated

mutants_xǁToolAuditǁrecent__mutmut['_mutmut_orig'] = ToolAudit.xǁToolAuditǁrecent__mutmut_orig # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_1'] = ToolAudit.xǁToolAuditǁrecent__mutmut_1 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_2'] = ToolAudit.xǁToolAuditǁrecent__mutmut_2 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_3'] = ToolAudit.xǁToolAuditǁrecent__mutmut_3 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_4'] = ToolAudit.xǁToolAuditǁrecent__mutmut_4 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_5'] = ToolAudit.xǁToolAuditǁrecent__mutmut_5 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_6'] = ToolAudit.xǁToolAuditǁrecent__mutmut_6 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_7'] = ToolAudit.xǁToolAuditǁrecent__mutmut_7 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_8'] = ToolAudit.xǁToolAuditǁrecent__mutmut_8 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_9'] = ToolAudit.xǁToolAuditǁrecent__mutmut_9 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_10'] = ToolAudit.xǁToolAuditǁrecent__mutmut_10 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_11'] = ToolAudit.xǁToolAuditǁrecent__mutmut_11 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_12'] = ToolAudit.xǁToolAuditǁrecent__mutmut_12 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_13'] = ToolAudit.xǁToolAuditǁrecent__mutmut_13 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_14'] = ToolAudit.xǁToolAuditǁrecent__mutmut_14 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_15'] = ToolAudit.xǁToolAuditǁrecent__mutmut_15 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_16'] = ToolAudit.xǁToolAuditǁrecent__mutmut_16 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_17'] = ToolAudit.xǁToolAuditǁrecent__mutmut_17 # type: ignore # mutmut generated
mutants_xǁToolAuditǁrecent__mutmut['xǁToolAuditǁrecent__mutmut_18'] = ToolAudit.xǁToolAuditǁrecent__mutmut_18 # type: ignore # mutmut generated

mutants_xǁToolAuditǁblocked_count__mutmut['_mutmut_orig'] = ToolAudit.xǁToolAuditǁblocked_count__mutmut_orig # type: ignore # mutmut generated
mutants_xǁToolAuditǁblocked_count__mutmut['xǁToolAuditǁblocked_count__mutmut_1'] = ToolAudit.xǁToolAuditǁblocked_count__mutmut_1 # type: ignore # mutmut generated
mutants_xǁToolAuditǁblocked_count__mutmut['xǁToolAuditǁblocked_count__mutmut_2'] = ToolAudit.xǁToolAuditǁblocked_count__mutmut_2 # type: ignore # mutmut generated
mutants_xǁToolAuditǁblocked_count__mutmut['xǁToolAuditǁblocked_count__mutmut_3'] = ToolAudit.xǁToolAuditǁblocked_count__mutmut_3 # type: ignore # mutmut generated
