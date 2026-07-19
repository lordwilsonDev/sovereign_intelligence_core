from __future__ import annotations

from typing import List

from msb_v2.engine.inversion_engine import InversionEngine
from msb_v2.engine.moie_types import Claim
from msb_v2.engine.observability import span


class Clerk:
    """Decompose query into atomic, fact-checkable claims."""

    def __init__(self, engine: InversionEngine | None = None) -> None:
        self.engine = engine or InversionEngine()

    @span("clerks.decompose")
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
