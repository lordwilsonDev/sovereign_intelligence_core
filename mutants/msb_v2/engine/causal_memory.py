from __future__ import annotations

from typing import Dict, List


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁCausalMemoryǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁCausalMemoryǁlink__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCausalMemoryǁhas_link__mutmut: MutantDict = {}  # type: ignore
mutants_xǁCausalMemoryǁreasons_for__mutmut: MutantDict = {}  # type: ignore


class CausalMemory:
    @_mutmut_mutated(mutants_xǁCausalMemoryǁ__init____mutmut)
    def __init__(self) -> None:
        self.links: Dict[str, List[tuple[str, str]]] = {}
    def xǁCausalMemoryǁ__init____mutmut_orig(self) -> None:
        self.links: Dict[str, List[tuple[str, str]]] = {}
    def xǁCausalMemoryǁ__init____mutmut_1(self) -> None:
        self.links: Dict[str, List[tuple[str, str]]] = None

    @_mutmut_mutated(mutants_xǁCausalMemoryǁlink__mutmut)
    def link(self, source: str, target: str, relation: str = "caused") -> None:
        self.links.setdefault(source, []).append((target, relation))

    def xǁCausalMemoryǁlink__mutmut_orig(self, source: str, target: str, relation: str = "caused") -> None:
        self.links.setdefault(source, []).append((target, relation))

    def xǁCausalMemoryǁlink__mutmut_1(self, source: str, target: str, relation: str = "XXcausedXX") -> None:
        self.links.setdefault(source, []).append((target, relation))

    def xǁCausalMemoryǁlink__mutmut_2(self, source: str, target: str, relation: str = "CAUSED") -> None:
        self.links.setdefault(source, []).append((target, relation))

    def xǁCausalMemoryǁlink__mutmut_3(self, source: str, target: str, relation: str = "caused") -> None:
        self.links.setdefault(source, []).append(None)

    def xǁCausalMemoryǁlink__mutmut_4(self, source: str, target: str, relation: str = "caused") -> None:
        self.links.setdefault(None, []).append((target, relation))

    def xǁCausalMemoryǁlink__mutmut_5(self, source: str, target: str, relation: str = "caused") -> None:
        self.links.setdefault(source, None).append((target, relation))

    def xǁCausalMemoryǁlink__mutmut_6(self, source: str, target: str, relation: str = "caused") -> None:
        self.links.setdefault([]).append((target, relation))

    def xǁCausalMemoryǁlink__mutmut_7(self, source: str, target: str, relation: str = "caused") -> None:
        self.links.setdefault(source, ).append((target, relation))

    @_mutmut_mutated(mutants_xǁCausalMemoryǁhas_link__mutmut)
    def has_link(self, source: str, target: str) -> bool:
        relations = self.links.get(source, [])
        return any(t == target for t, _ in relations)

    def xǁCausalMemoryǁhas_link__mutmut_orig(self, source: str, target: str) -> bool:
        relations = self.links.get(source, [])
        return any(t == target for t, _ in relations)

    def xǁCausalMemoryǁhas_link__mutmut_1(self, source: str, target: str) -> bool:
        relations = None
        return any(t == target for t, _ in relations)

    def xǁCausalMemoryǁhas_link__mutmut_2(self, source: str, target: str) -> bool:
        relations = self.links.get(None, [])
        return any(t == target for t, _ in relations)

    def xǁCausalMemoryǁhas_link__mutmut_3(self, source: str, target: str) -> bool:
        relations = self.links.get(source, None)
        return any(t == target for t, _ in relations)

    def xǁCausalMemoryǁhas_link__mutmut_4(self, source: str, target: str) -> bool:
        relations = self.links.get([])
        return any(t == target for t, _ in relations)

    def xǁCausalMemoryǁhas_link__mutmut_5(self, source: str, target: str) -> bool:
        relations = self.links.get(source, )
        return any(t == target for t, _ in relations)

    def xǁCausalMemoryǁhas_link__mutmut_6(self, source: str, target: str) -> bool:
        relations = self.links.get(source, [])
        return any(None)

    def xǁCausalMemoryǁhas_link__mutmut_7(self, source: str, target: str) -> bool:
        relations = self.links.get(source, [])
        return any(t != target for t, _ in relations)

    @_mutmut_mutated(mutants_xǁCausalMemoryǁreasons_for__mutmut)
    def reasons_for(self, node: str) -> List[str]:
        out = []
        for src, targets in self.links.items():
            for tgt, relation in targets:
                if tgt == node:
                    out.append(f"{src}->{node}::{relation}")
        return out

    def xǁCausalMemoryǁreasons_for__mutmut_orig(self, node: str) -> List[str]:
        out = []
        for src, targets in self.links.items():
            for tgt, relation in targets:
                if tgt == node:
                    out.append(f"{src}->{node}::{relation}")
        return out

    def xǁCausalMemoryǁreasons_for__mutmut_1(self, node: str) -> List[str]:
        out = None
        for src, targets in self.links.items():
            for tgt, relation in targets:
                if tgt == node:
                    out.append(f"{src}->{node}::{relation}")
        return out

    def xǁCausalMemoryǁreasons_for__mutmut_2(self, node: str) -> List[str]:
        out = []
        for src, targets in self.links.items():
            for tgt, relation in targets:
                if tgt != node:
                    out.append(f"{src}->{node}::{relation}")
        return out

    def xǁCausalMemoryǁreasons_for__mutmut_3(self, node: str) -> List[str]:
        out = []
        for src, targets in self.links.items():
            for tgt, relation in targets:
                if tgt == node:
                    out.append(None)
        return out

mutants_xǁCausalMemoryǁ__init____mutmut['_mutmut_orig'] = CausalMemory.xǁCausalMemoryǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁ__init____mutmut['xǁCausalMemoryǁ__init____mutmut_1'] = CausalMemory.xǁCausalMemoryǁ__init____mutmut_1 # type: ignore # mutmut generated

mutants_xǁCausalMemoryǁlink__mutmut['_mutmut_orig'] = CausalMemory.xǁCausalMemoryǁlink__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁlink__mutmut['xǁCausalMemoryǁlink__mutmut_1'] = CausalMemory.xǁCausalMemoryǁlink__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁlink__mutmut['xǁCausalMemoryǁlink__mutmut_2'] = CausalMemory.xǁCausalMemoryǁlink__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁlink__mutmut['xǁCausalMemoryǁlink__mutmut_3'] = CausalMemory.xǁCausalMemoryǁlink__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁlink__mutmut['xǁCausalMemoryǁlink__mutmut_4'] = CausalMemory.xǁCausalMemoryǁlink__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁlink__mutmut['xǁCausalMemoryǁlink__mutmut_5'] = CausalMemory.xǁCausalMemoryǁlink__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁlink__mutmut['xǁCausalMemoryǁlink__mutmut_6'] = CausalMemory.xǁCausalMemoryǁlink__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁlink__mutmut['xǁCausalMemoryǁlink__mutmut_7'] = CausalMemory.xǁCausalMemoryǁlink__mutmut_7 # type: ignore # mutmut generated

mutants_xǁCausalMemoryǁhas_link__mutmut['_mutmut_orig'] = CausalMemory.xǁCausalMemoryǁhas_link__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁhas_link__mutmut['xǁCausalMemoryǁhas_link__mutmut_1'] = CausalMemory.xǁCausalMemoryǁhas_link__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁhas_link__mutmut['xǁCausalMemoryǁhas_link__mutmut_2'] = CausalMemory.xǁCausalMemoryǁhas_link__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁhas_link__mutmut['xǁCausalMemoryǁhas_link__mutmut_3'] = CausalMemory.xǁCausalMemoryǁhas_link__mutmut_3 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁhas_link__mutmut['xǁCausalMemoryǁhas_link__mutmut_4'] = CausalMemory.xǁCausalMemoryǁhas_link__mutmut_4 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁhas_link__mutmut['xǁCausalMemoryǁhas_link__mutmut_5'] = CausalMemory.xǁCausalMemoryǁhas_link__mutmut_5 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁhas_link__mutmut['xǁCausalMemoryǁhas_link__mutmut_6'] = CausalMemory.xǁCausalMemoryǁhas_link__mutmut_6 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁhas_link__mutmut['xǁCausalMemoryǁhas_link__mutmut_7'] = CausalMemory.xǁCausalMemoryǁhas_link__mutmut_7 # type: ignore # mutmut generated

mutants_xǁCausalMemoryǁreasons_for__mutmut['_mutmut_orig'] = CausalMemory.xǁCausalMemoryǁreasons_for__mutmut_orig # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁreasons_for__mutmut['xǁCausalMemoryǁreasons_for__mutmut_1'] = CausalMemory.xǁCausalMemoryǁreasons_for__mutmut_1 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁreasons_for__mutmut['xǁCausalMemoryǁreasons_for__mutmut_2'] = CausalMemory.xǁCausalMemoryǁreasons_for__mutmut_2 # type: ignore # mutmut generated
mutants_xǁCausalMemoryǁreasons_for__mutmut['xǁCausalMemoryǁreasons_for__mutmut_3'] = CausalMemory.xǁCausalMemoryǁreasons_for__mutmut_3 # type: ignore # mutmut generated
