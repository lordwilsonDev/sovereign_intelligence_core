from __future__ import annotations

from dataclasses import dataclass
from typing import List


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


@dataclass
class PriorityScore:
    label: str
    urgency: float = 0.5
    impact: float = 0.5
    confidence: float = 0.5

    def composite(self) -> float:
        return (self.urgency * 0.4) + (self.impact * 0.4) + (self.confidence * 0.2)
mutants_xǁPriorityDecayǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁPriorityDecayǁadd__mutmut: MutantDict = {}  # type: ignore
mutants_xǁPriorityDecayǁranked__mutmut: MutantDict = {}  # type: ignore


class PriorityDecay:
    @_mutmut_mutated(mutants_xǁPriorityDecayǁ__init____mutmut)
    def __init__(self) -> None:
        self.scores: List[PriorityScore] = []
    def xǁPriorityDecayǁ__init____mutmut_orig(self) -> None:
        self.scores: List[PriorityScore] = []
    def xǁPriorityDecayǁ__init____mutmut_1(self) -> None:
        self.scores: List[PriorityScore] = None

    @_mutmut_mutated(mutants_xǁPriorityDecayǁadd__mutmut)
    def add(self, score: PriorityScore) -> None:
        self.scores.append(score)

    def xǁPriorityDecayǁadd__mutmut_orig(self, score: PriorityScore) -> None:
        self.scores.append(score)

    def xǁPriorityDecayǁadd__mutmut_1(self, score: PriorityScore) -> None:
        self.scores.append(None)

    @_mutmut_mutated(mutants_xǁPriorityDecayǁranked__mutmut)
    def ranked(self) -> List[tuple[str, float]]:
        return sorted([(s.label, s.composite()) for s in self.scores], key=lambda x: x[1], reverse=True)

    def xǁPriorityDecayǁranked__mutmut_orig(self) -> List[tuple[str, float]]:
        return sorted([(s.label, s.composite()) for s in self.scores], key=lambda x: x[1], reverse=True)

    def xǁPriorityDecayǁranked__mutmut_1(self) -> List[tuple[str, float]]:
        return sorted(None, key=lambda x: x[1], reverse=True)

    def xǁPriorityDecayǁranked__mutmut_2(self) -> List[tuple[str, float]]:
        return sorted([(s.label, s.composite()) for s in self.scores], key=None, reverse=True)

    def xǁPriorityDecayǁranked__mutmut_3(self) -> List[tuple[str, float]]:
        return sorted([(s.label, s.composite()) for s in self.scores], key=lambda x: x[1], reverse=None)

    def xǁPriorityDecayǁranked__mutmut_4(self) -> List[tuple[str, float]]:
        return sorted(key=lambda x: x[1], reverse=True)

    def xǁPriorityDecayǁranked__mutmut_5(self) -> List[tuple[str, float]]:
        return sorted([(s.label, s.composite()) for s in self.scores], reverse=True)

    def xǁPriorityDecayǁranked__mutmut_6(self) -> List[tuple[str, float]]:
        return sorted([(s.label, s.composite()) for s in self.scores], key=lambda x: x[1], )

    def xǁPriorityDecayǁranked__mutmut_7(self) -> List[tuple[str, float]]:
        return sorted([(s.label, s.composite()) for s in self.scores], key=lambda x: None, reverse=True)

    def xǁPriorityDecayǁranked__mutmut_8(self) -> List[tuple[str, float]]:
        return sorted([(s.label, s.composite()) for s in self.scores], key=lambda x: x[2], reverse=True)

    def xǁPriorityDecayǁranked__mutmut_9(self) -> List[tuple[str, float]]:
        return sorted([(s.label, s.composite()) for s in self.scores], key=lambda x: x[1], reverse=False)

mutants_xǁPriorityDecayǁ__init____mutmut['_mutmut_orig'] = PriorityDecay.xǁPriorityDecayǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁ__init____mutmut['xǁPriorityDecayǁ__init____mutmut_1'] = PriorityDecay.xǁPriorityDecayǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁPriorityDecayǁadd__mutmut['_mutmut_orig'] = PriorityDecay.xǁPriorityDecayǁadd__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁadd__mutmut['xǁPriorityDecayǁadd__mutmut_1'] = PriorityDecay.xǁPriorityDecayǁadd__mutmut_1 # type: ignore # mutmut generated

mutants_xǁPriorityDecayǁranked__mutmut['_mutmut_orig'] = PriorityDecay.xǁPriorityDecayǁranked__mutmut_orig # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁranked__mutmut['xǁPriorityDecayǁranked__mutmut_1'] = PriorityDecay.xǁPriorityDecayǁranked__mutmut_1 # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁranked__mutmut['xǁPriorityDecayǁranked__mutmut_2'] = PriorityDecay.xǁPriorityDecayǁranked__mutmut_2 # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁranked__mutmut['xǁPriorityDecayǁranked__mutmut_3'] = PriorityDecay.xǁPriorityDecayǁranked__mutmut_3 # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁranked__mutmut['xǁPriorityDecayǁranked__mutmut_4'] = PriorityDecay.xǁPriorityDecayǁranked__mutmut_4 # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁranked__mutmut['xǁPriorityDecayǁranked__mutmut_5'] = PriorityDecay.xǁPriorityDecayǁranked__mutmut_5 # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁranked__mutmut['xǁPriorityDecayǁranked__mutmut_6'] = PriorityDecay.xǁPriorityDecayǁranked__mutmut_6 # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁranked__mutmut['xǁPriorityDecayǁranked__mutmut_7'] = PriorityDecay.xǁPriorityDecayǁranked__mutmut_7 # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁranked__mutmut['xǁPriorityDecayǁranked__mutmut_8'] = PriorityDecay.xǁPriorityDecayǁranked__mutmut_8 # type: ignore # mutmut generated
mutants_xǁPriorityDecayǁranked__mutmut['xǁPriorityDecayǁranked__mutmut_9'] = PriorityDecay.xǁPriorityDecayǁranked__mutmut_9 # type: ignore # mutmut generated
