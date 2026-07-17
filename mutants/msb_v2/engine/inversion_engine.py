from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@dataclass
class InversionResult:
    original: str
    inversion: str
    consequences: list[str] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    score: float = 0.0
    scored_output: dict[str, Any] = field(default_factory=dict)
    impact: float = 0.5
    confidence: float = 0.5
mutants_xǁInversionEngineǁinvert__mutmut: MutantDict = {}  # type: ignore
mutants_xǁInversionEngineǁinvert_many__mutmut: MutantDict = {}  # type: ignore
mutants_xǁInversionEngineǁ_build__mutmut: MutantDict = {}  # type: ignore


class InversionEngine:
    @_mutmut_mutated(mutants_xǁInversionEngineǁinvert__mutmut)
    def invert(self, assumption: str) -> InversionResult:
        return self._build(assumption)
    def xǁInversionEngineǁinvert__mutmut_orig(self, assumption: str) -> InversionResult:
        return self._build(assumption)
    def xǁInversionEngineǁinvert__mutmut_1(self, assumption: str) -> InversionResult:
        return self._build(None)

    @_mutmut_mutated(mutants_xǁInversionEngineǁinvert_many__mutmut)
    def invert_many(self, assumption: str) -> Sequence[InversionResult]:
        return [self._build(assumption)]

    def xǁInversionEngineǁinvert_many__mutmut_orig(self, assumption: str) -> Sequence[InversionResult]:
        return [self._build(assumption)]

    def xǁInversionEngineǁinvert_many__mutmut_1(self, assumption: str) -> Sequence[InversionResult]:
        return [self._build(None)]

    @staticmethod
    @_mutmut_mutated(mutants_xǁInversionEngineǁ_build__mutmut)
    def _build(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_orig(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_1(assumption: str) -> InversionResult:
        inv = None
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_2(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = None
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_3(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=None,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_4(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=None,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_5(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=None,
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_6(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=None,
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_7(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=None,
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_8(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=None,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_9(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output=None,
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_10(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=None,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_11(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=None,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_12(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_13(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_14(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_15(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_16(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_17(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_18(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_19(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_20(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_21(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["XXReconsider architecture under inversionXX"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_22(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_23(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["RECONSIDER ARCHITECTURE UNDER INVERSION"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_24(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["XXInversion may introduce new dependenciesXX"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_25(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_26(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["INVERSION MAY INTRODUCE NEW DEPENDENCIES"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_27(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=1.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_28(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "XXconsequencesXX": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_29(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "CONSEQUENCES": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_30(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 1.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_31(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "XXopportunitiesXX": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_32(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "OPPORTUNITIES": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_33(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 1.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_34(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "XXrisksXX": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_35(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "RISKS": 0.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_36(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 1.34,
            },
            impact=0.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_37(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=1.5,
            confidence=0.5,
        )
        return result

    @staticmethod
    def xǁInversionEngineǁ_build__mutmut_38(assumption: str) -> InversionResult:
        inv = f"not({assumption})"
        result = InversionResult(
            original=assumption,
            inversion=inv,
            consequences=[f"Consequence of assuming: {inv}"],
            opportunities=["Reconsider architecture under inversion"],
            risks=["Inversion may introduce new dependencies"],
            score=0.5,
            scored_output={
                "consequences": 0.33,
                "opportunities": 0.33,
                "risks": 0.34,
            },
            impact=0.5,
            confidence=1.5,
        )
        return result

mutants_xǁInversionEngineǁinvert__mutmut['_mutmut_orig'] = InversionEngine.xǁInversionEngineǁinvert__mutmut_orig # type: ignore # mutmut generated
mutants_xǁInversionEngineǁinvert__mutmut['xǁInversionEngineǁinvert__mutmut_1'] = InversionEngine.xǁInversionEngineǁinvert__mutmut_1 # type: ignore # mutmut generated

mutants_xǁInversionEngineǁinvert_many__mutmut['_mutmut_orig'] = InversionEngine.xǁInversionEngineǁinvert_many__mutmut_orig # type: ignore # mutmut generated
mutants_xǁInversionEngineǁinvert_many__mutmut['xǁInversionEngineǁinvert_many__mutmut_1'] = InversionEngine.xǁInversionEngineǁinvert_many__mutmut_1 # type: ignore # mutmut generated

mutants_xǁInversionEngineǁ_build__mutmut['_mutmut_orig'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_orig # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_1'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_1 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_2'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_2 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_3'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_3 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_4'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_4 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_5'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_5 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_6'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_6 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_7'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_7 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_8'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_8 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_9'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_9 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_10'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_10 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_11'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_11 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_12'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_12 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_13'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_13 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_14'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_14 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_15'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_15 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_16'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_16 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_17'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_17 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_18'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_18 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_19'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_19 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_20'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_20 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_21'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_21 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_22'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_22 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_23'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_23 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_24'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_24 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_25'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_25 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_26'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_26 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_27'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_27 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_28'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_28 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_29'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_29 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_30'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_30 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_31'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_31 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_32'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_32 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_33'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_33 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_34'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_34 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_35'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_35 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_36'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_36 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_37'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_37 # type: ignore # mutmut generated
mutants_xǁInversionEngineǁ_build__mutmut['xǁInversionEngineǁ_build__mutmut_38'] = InversionEngine.xǁInversionEngineǁ_build__mutmut_38 # type: ignore # mutmut generated
