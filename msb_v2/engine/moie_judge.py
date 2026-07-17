from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Sequence

from msb_v2.engine.moie_types import Claim, DebateRound
from msb_v2.engine.rcoh_persistence import RCOHPersistence


class Judge:
    """Synthesize broadcast debate transcript into validated judgment."""

    def __init__(self, persistence: RCOHPersistence | None = None) -> None:
        self._persistence = persistence

    def synthesize(self, debate: DebateRound) -> Dict[str, Any]:
        transcript_text = "\n".join(debate.transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        validated: List[str] = []
        rejected: List[str] = []
        inconclusive: List[str] = []

        from collections import Counter
        per_claim: Dict[str, Counter] = {}
        for claim_id, stance, evidence, confidence in debate.votes:
            per_claim.setdefault(claim_id, Counter())[stance] += 1

        for claim in debate.claims:
            counts = per_claim.get(claim.id, Counter())
            support = counts.get("support", 0)
            reject = counts.get("reject", 0)
            refine = counts.get("refine", 0)
            if support > reject and support >= refine:
                validated.append(claim.id)
                claim.status = "validated"
            elif reject >= support and reject >= refine:
                rejected.append(claim.id)
                claim.status = "rejected"
            else:
                inconclusive.append(claim.id)
                claim.status = "inconclusive"

        stance_counts = Counter(s for _, s, _, _ in debate.votes)
        dominant = stance_counts.most_common(1)[0][0] if stance_counts else "inconclusive"
        breakthrough_potential = "high" if len(validated) >= len(debate.claims) // 2 else ("medium" if validated else "low")

        judgment: Dict[str, Any] = {
            "query": debate.query,
            "claims": [self._claim_to_dict(c) for c in debate.claims],
            "transcript_hash": transcript_hash,
            "validated": validated,
            "rejected": rejected,
            "inconclusive": inconclusive,
            "consensus_statement": self._build_consensus(debate, validated, dominant),
            "anomaly_score": round((len(validated) * 0.6 + len(inconclusive) * 0.2) / max(1, len(debate.claims)), 4),
            "breakthrough_potential": breakthrough_potential,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if self._persistence is not None:
            self._persistence.save_artifact("moie", f"{debate.query[:50]}/judgment", judgment)
        return judgment

    @staticmethod
    def _claim_to_dict(claim: Claim) -> Dict[str, Any]:
        return {
            "id": claim.id,
            "text": claim.text,
            "source": claim.source,
            "inversion_of": claim.inversion_of,
            "scores": claim.scores,
            "status": claim.status,
        }

    @staticmethod
    def _build_consensus(debate: DebateRound, validated: Sequence[str], dominant: str) -> str:
        validated_texts = [c.text for c in debate.claims if c.id in validated]
        if validated_texts:
            return f"Validated inversions ({len(validated_texts)} of {len(debate.claims)}): " + "; ".join(validated_texts)
        return f"No validated claims after {len(debate.nodes)}-node broadcast; dominant stance={dominant}."
