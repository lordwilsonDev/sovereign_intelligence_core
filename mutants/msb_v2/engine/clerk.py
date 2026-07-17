from __future__ import annotations

from typing import List

from msb_v2.engine.inversion_engine import InversionEngine
from msb_v2.engine.moie_types import Claim


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_xǁClerkǁ__init____mutmut: MutantDict = {}  # type: ignore
mutants_xǁClerkǁdecompose__mutmut: MutantDict = {}  # type: ignore


class Clerk:
    """Decompose query into atomic, fact-checkable claims."""

    @_mutmut_mutated(mutants_xǁClerkǁ__init____mutmut)
    def __init__(self, engine: InversionEngine | None = None) -> None:
        self.engine = engine or InversionEngine()

    def xǁClerkǁ__init____mutmut_orig(self, engine: InversionEngine | None = None) -> None:
        self.engine = engine or InversionEngine()

    def xǁClerkǁ__init____mutmut_1(self, engine: InversionEngine | None = None) -> None:
        self.engine = None

    def xǁClerkǁ__init____mutmut_2(self, engine: InversionEngine | None = None) -> None:
        self.engine = engine and InversionEngine()

    @_mutmut_mutated(mutants_xǁClerkǁdecompose__mutmut)
    def decompose(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_orig(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_1(self, query: str, max_claims: int = 8) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_2(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = None
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_3(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(None)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_4(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = None
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_5(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = None
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_6(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(None, start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_7(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=None):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_8(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_9(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], ):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_10(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=2):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_11(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = None
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_12(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text and text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_13(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_14(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text not in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_15(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                break
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_16(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(None)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_17(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = None
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_18(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=None,
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_19(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=None,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_20(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source=None,
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_21(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=None,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_22(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores=None,
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_23(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_24(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_25(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_26(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_27(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_28(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="XXclerkXX",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_29(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="CLERK",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_30(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"XXimpactXX": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_31(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"IMPACT": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_32(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "XXconfidenceXX": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_33(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "CONFIDENCE": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_34(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(None)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_35(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_36(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                None
            )
        return claims

    def xǁClerkǁdecompose__mutmut_37(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id=None,
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_38(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=None,
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_39(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source=None,
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_40(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores=None,
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_41(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_42(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_43(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_44(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_45(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="XXc01XX",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_46(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="C01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_47(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="XXclerkXX",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_48(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="CLERK",
                    scores={"impact": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_49(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"XXimpactXX": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_50(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"IMPACT": 0.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_51(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 1.5, "confidence": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_52(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "XXconfidenceXX": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_53(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "CONFIDENCE": 0.5},
                )
            )
        return claims

    def xǁClerkǁdecompose__mutmut_54(self, query: str, max_claims: int = 7) -> List[Claim]:
        inversions = self.engine.invert_many(query)
        claims: List[Claim] = []
        seen_texts = set()
        for idx, inv in enumerate(inversions[:max_claims], start=1):
            text = inv.inversion.strip()
            if not text or text in seen_texts:
                continue
            seen_texts.add(text)
            claim = Claim(
                id=f"c{idx:02d}",
                text=text,
                source="clerk",
                inversion_of=inv.original,
                scores={"impact": inv.impact, "confidence": inv.confidence},
            )
            claims.append(claim)
        if not claims:
            claims.append(
                Claim(
                    id="c01",
                    text=f"Invert assumption in: {query}",
                    source="clerk",
                    scores={"impact": 0.5, "confidence": 1.5},
                )
            )
        return claims

mutants_xǁClerkǁ__init____mutmut['_mutmut_orig'] = Clerk.xǁClerkǁ__init____mutmut_orig # type: ignore # mutmut generated
mutants_xǁClerkǁ__init____mutmut['xǁClerkǁ__init____mutmut_1'] = Clerk.xǁClerkǁ__init____mutmut_1 # type: ignore # mutmut generated
mutants_xǁClerkǁ__init____mutmut['xǁClerkǁ__init____mutmut_2'] = Clerk.xǁClerkǁ__init____mutmut_2 # type: ignore # mutmut generated

mutants_xǁClerkǁdecompose__mutmut['_mutmut_orig'] = Clerk.xǁClerkǁdecompose__mutmut_orig # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_1'] = Clerk.xǁClerkǁdecompose__mutmut_1 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_2'] = Clerk.xǁClerkǁdecompose__mutmut_2 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_3'] = Clerk.xǁClerkǁdecompose__mutmut_3 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_4'] = Clerk.xǁClerkǁdecompose__mutmut_4 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_5'] = Clerk.xǁClerkǁdecompose__mutmut_5 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_6'] = Clerk.xǁClerkǁdecompose__mutmut_6 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_7'] = Clerk.xǁClerkǁdecompose__mutmut_7 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_8'] = Clerk.xǁClerkǁdecompose__mutmut_8 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_9'] = Clerk.xǁClerkǁdecompose__mutmut_9 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_10'] = Clerk.xǁClerkǁdecompose__mutmut_10 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_11'] = Clerk.xǁClerkǁdecompose__mutmut_11 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_12'] = Clerk.xǁClerkǁdecompose__mutmut_12 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_13'] = Clerk.xǁClerkǁdecompose__mutmut_13 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_14'] = Clerk.xǁClerkǁdecompose__mutmut_14 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_15'] = Clerk.xǁClerkǁdecompose__mutmut_15 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_16'] = Clerk.xǁClerkǁdecompose__mutmut_16 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_17'] = Clerk.xǁClerkǁdecompose__mutmut_17 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_18'] = Clerk.xǁClerkǁdecompose__mutmut_18 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_19'] = Clerk.xǁClerkǁdecompose__mutmut_19 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_20'] = Clerk.xǁClerkǁdecompose__mutmut_20 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_21'] = Clerk.xǁClerkǁdecompose__mutmut_21 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_22'] = Clerk.xǁClerkǁdecompose__mutmut_22 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_23'] = Clerk.xǁClerkǁdecompose__mutmut_23 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_24'] = Clerk.xǁClerkǁdecompose__mutmut_24 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_25'] = Clerk.xǁClerkǁdecompose__mutmut_25 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_26'] = Clerk.xǁClerkǁdecompose__mutmut_26 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_27'] = Clerk.xǁClerkǁdecompose__mutmut_27 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_28'] = Clerk.xǁClerkǁdecompose__mutmut_28 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_29'] = Clerk.xǁClerkǁdecompose__mutmut_29 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_30'] = Clerk.xǁClerkǁdecompose__mutmut_30 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_31'] = Clerk.xǁClerkǁdecompose__mutmut_31 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_32'] = Clerk.xǁClerkǁdecompose__mutmut_32 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_33'] = Clerk.xǁClerkǁdecompose__mutmut_33 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_34'] = Clerk.xǁClerkǁdecompose__mutmut_34 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_35'] = Clerk.xǁClerkǁdecompose__mutmut_35 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_36'] = Clerk.xǁClerkǁdecompose__mutmut_36 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_37'] = Clerk.xǁClerkǁdecompose__mutmut_37 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_38'] = Clerk.xǁClerkǁdecompose__mutmut_38 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_39'] = Clerk.xǁClerkǁdecompose__mutmut_39 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_40'] = Clerk.xǁClerkǁdecompose__mutmut_40 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_41'] = Clerk.xǁClerkǁdecompose__mutmut_41 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_42'] = Clerk.xǁClerkǁdecompose__mutmut_42 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_43'] = Clerk.xǁClerkǁdecompose__mutmut_43 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_44'] = Clerk.xǁClerkǁdecompose__mutmut_44 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_45'] = Clerk.xǁClerkǁdecompose__mutmut_45 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_46'] = Clerk.xǁClerkǁdecompose__mutmut_46 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_47'] = Clerk.xǁClerkǁdecompose__mutmut_47 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_48'] = Clerk.xǁClerkǁdecompose__mutmut_48 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_49'] = Clerk.xǁClerkǁdecompose__mutmut_49 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_50'] = Clerk.xǁClerkǁdecompose__mutmut_50 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_51'] = Clerk.xǁClerkǁdecompose__mutmut_51 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_52'] = Clerk.xǁClerkǁdecompose__mutmut_52 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_53'] = Clerk.xǁClerkǁdecompose__mutmut_53 # type: ignore # mutmut generated
mutants_xǁClerkǁdecompose__mutmut['xǁClerkǁdecompose__mutmut_54'] = Clerk.xǁClerkǁdecompose__mutmut_54 # type: ignore # mutmut generated
