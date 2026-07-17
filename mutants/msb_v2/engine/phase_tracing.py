from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@dataclass
class PhaseSpan:
    phase: str
    started_at: str
    finished_at: str = ""
    duration_ms: float = 0.0
    evidence_count: int = 0
    assumption_count: int = 0
    tool_calls: int = 0
    result: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)
mutants_xǁPhaseTracerǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁPhaseTracerǁbegin__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPhaseTracerǁend__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPhaseTracerǁexport__mutmut: MutantDict = {}  # type: ignore


class PhaseTracer:
    @_mutmut_mutated(mutants_xǁPhaseTracerǁ__init____mutmut)
    def __init__(self) -> None:
        self.spans: list[PhaseSpan] = []
    def xǁPhaseTracerǁ__init____mutmut_orig(self) -> None:
        self.spans: list[PhaseSpan] = []
    def xǁPhaseTracerǁ__init____mutmut_1(self) -> None:
        self.spans: list[PhaseSpan] = None

    @_mutmut_mutated(mutants_xǁPhaseTracerǁbegin__mutmut)
    def begin(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=phase,
            started_at=datetime.now(timezone.utc).isoformat(),
            metadata=meta or {},
        )
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_orig(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=phase,
            started_at=datetime.now(timezone.utc).isoformat(),
            metadata=meta or {},
        )
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_1(self, phase: str, **meta: Any) -> PhaseSpan:
        span = None
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_2(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=None,
            started_at=datetime.now(timezone.utc).isoformat(),
            metadata=meta or {},
        )
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_3(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=phase,
            started_at=None,
            metadata=meta or {},
        )
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_4(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=phase,
            started_at=datetime.now(timezone.utc).isoformat(),
            metadata=None,
        )
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_5(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            started_at=datetime.now(timezone.utc).isoformat(),
            metadata=meta or {},
        )
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_6(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=phase,
            metadata=meta or {},
        )
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_7(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=phase,
            started_at=datetime.now(timezone.utc).isoformat(),
            )
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_8(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=phase,
            started_at=datetime.now(None).isoformat(),
            metadata=meta or {},
        )
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_9(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=phase,
            started_at=datetime.now(timezone.utc).isoformat(),
            metadata=meta and {},
        )
        self.spans.append(span)
        return span

    def xǁPhaseTracerǁbegin__mutmut_10(self, phase: str, **meta: Any) -> PhaseSpan:
        span = PhaseSpan(
            phase=phase,
            started_at=datetime.now(timezone.utc).isoformat(),
            metadata=meta or {},
        )
        self.spans.append(None)
        return span

    @_mutmut_mutated(mutants_xǁPhaseTracerǁend__mutmut)
    def end(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_orig(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_1(self, span: PhaseSpan, result: str = "XXunknownXX", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_2(self, span: PhaseSpan, result: str = "UNKNOWN", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_3(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = None
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_4(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(None)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_5(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = None
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_6(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = None
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_7(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() / 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_8(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00")) + datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_9(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(None)
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_10(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace(None, "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_11(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", None))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_12(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_13(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", ))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_14(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("XXZXX", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_15(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_16(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "XX+00:00XX"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_17(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(None)
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_18(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace(None, "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_19(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", None))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_20(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_21(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", ))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_22(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("XXZXX", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_23(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_24(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "XX+00:00XX"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_25(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1001
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_26(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = None
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_27(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra and {}).items():
            if hasattr(span, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_28(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(None, k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_29(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, None):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_30(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(k):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_31(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, ):
                setattr(span, k, v)

    def xǁPhaseTracerǁend__mutmut_32(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(None, k, v)

    def xǁPhaseTracerǁend__mutmut_33(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, None, v)

    def xǁPhaseTracerǁend__mutmut_34(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, None)

    def xǁPhaseTracerǁend__mutmut_35(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(k, v)

    def xǁPhaseTracerǁend__mutmut_36(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, v)

    def xǁPhaseTracerǁend__mutmut_37(self, span: PhaseSpan, result: str = "unknown", **extra: Any) -> None:
        now = datetime.now(timezone.utc)
        span.finished_at = now.isoformat()
        span.duration_ms = (
            datetime.fromisoformat(span.finished_at.replace("Z", "+00:00"))
            - datetime.fromisoformat(span.started_at.replace("Z", "+00:00"))
        ).total_seconds() * 1000
        span.result = result
        for k, v in (extra or {}).items():
            if hasattr(span, k):
                setattr(span, k, )

    @_mutmut_mutated(mutants_xǁPhaseTracerǁexport__mutmut)
    def export(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_orig(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_1(self) -> list[dict[str, Any]]:
        out = None
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_2(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                None
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_3(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "XXphaseXX": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_4(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "PHASE": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_5(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "XXstarted_atXX": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_6(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "STARTED_AT": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_7(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "XXfinished_atXX": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_8(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "FINISHED_AT": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_9(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "XXduration_msXX": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_10(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "DURATION_MS": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_11(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "XXevidence_countXX": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_12(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "EVIDENCE_COUNT": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_13(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "XXassumption_countXX": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_14(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "ASSUMPTION_COUNT": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_15(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "XXtool_callsXX": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_16(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "TOOL_CALLS": s.tool_calls,
                    "result": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_17(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "XXresultXX": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_18(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "RESULT": s.result,
                    "metadata": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_19(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "XXmetadataXX": s.metadata,
                }
            )
        return out

    def xǁPhaseTracerǁexport__mutmut_20(self) -> list[dict[str, Any]]:
        out = []
        for s in self.spans:
            out.append(
                {
                    "phase": s.phase,
                    "started_at": s.started_at,
                    "finished_at": s.finished_at,
                    "duration_ms": s.duration_ms,
                    "evidence_count": s.evidence_count,
                    "assumption_count": s.assumption_count,
                    "tool_calls": s.tool_calls,
                    "result": s.result,
                    "METADATA": s.metadata,
                }
            )
        return out

mutants_xǁPhaseTracerǁ__init____mutmut['_mutmut_orig'] = PhaseTracer.xǁPhaseTracerǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁ__init____mutmut['xǁPhaseTracerǁ__init____mutmut_1'] = PhaseTracer.xǁPhaseTracerǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁPhaseTracerǁbegin__mutmut['_mutmut_orig'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁbegin__mutmut['xǁPhaseTracerǁbegin__mutmut_1'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁbegin__mutmut['xǁPhaseTracerǁbegin__mutmut_2'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁbegin__mutmut['xǁPhaseTracerǁbegin__mutmut_3'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁbegin__mutmut['xǁPhaseTracerǁbegin__mutmut_4'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁbegin__mutmut['xǁPhaseTracerǁbegin__mutmut_5'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁbegin__mutmut['xǁPhaseTracerǁbegin__mutmut_6'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁbegin__mutmut['xǁPhaseTracerǁbegin__mutmut_7'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁbegin__mutmut['xǁPhaseTracerǁbegin__mutmut_8'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁbegin__mutmut['xǁPhaseTracerǁbegin__mutmut_9'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁbegin__mutmut['xǁPhaseTracerǁbegin__mutmut_10'] = PhaseTracer.xǁPhaseTracerǁbegin__mutmut_10 # type: ignore # mutmut generated

mutants_xǁPhaseTracerǁend__mutmut['_mutmut_orig'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_1'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_2'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_3'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_4'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_5'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_6'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_7'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_8'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_9'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_10'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_11'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_12'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_13'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_14'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_15'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_16'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_17'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_18'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_19'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_20'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_20 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_21'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_21 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_22'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_22 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_23'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_23 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_24'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_24 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_25'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_25 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_26'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_26 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_27'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_27 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_28'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_28 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_29'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_29 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_30'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_30 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_31'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_31 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_32'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_32 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_33'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_33 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_34'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_34 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_35'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_35 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_36'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_36 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁend__mutmut['xǁPhaseTracerǁend__mutmut_37'] = PhaseTracer.xǁPhaseTracerǁend__mutmut_37 # type: ignore # mutmut generated

mutants_xǁPhaseTracerǁexport__mutmut['_mutmut_orig'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_1'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_2'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_3'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_4'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_5'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_6'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_7'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_8'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_9'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_9 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_10'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_10 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_11'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_11 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_12'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_12 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_13'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_13 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_14'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_14 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_15'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_15 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_16'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_16 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_17'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_17 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_18'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_18 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_19'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_19 # type: ignore # mutmut generated
mutants_xǁPhaseTracerǁexport__mutmut['xǁPhaseTracerǁexport__mutmut_20'] = PhaseTracer.xǁPhaseTracerǁexport__mutmut_20 # type: ignore # mutmut generated
