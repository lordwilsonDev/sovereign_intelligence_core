from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Sequence

from msb_v2.engine.moie_types import Claim, DebateRound, HiveMindNode
from msb_v2.engine.clerk import Clerk
from msb_v2.engine.moie_judge import Judge
from msb_v2.engine.crystallizer import Crystallizer
from msb_v2.engine.causal_memory import CausalMemory
from msb_v2.engine.rcoh_persistence import RCOHPersistence


class MoIEOrchestrator:
    """Clerk + broadcast debate + Judge + CausalMemory in one local workflow."""

    def __init__(
        self,
        clerk: Clerk | None = None,
        judge: Judge | None = None,
        crystallizer: Crystallizer | None = None,
        persistence: RCOHPersistence | None = None,
        causal_memory: CausalMemory | None = None,
        nodes: Sequence[HiveMindNode] | None = None,
    ) -> None:
        self.clerk = clerk or Clerk()
        self.judge = judge or Judge(persistence=persistence)
        self.crystallizer = crystallizer or Crystallizer(persistence=persistence)
        self.persistence = persistence
        self.causal_memory = causal_memory or CausalMemory()
        self.nodes = list(nodes) if nodes is not None else self._default_nodes()

    @staticmethod
    def _default_nodes() -> List[HiveMindNode]:
        from msb_v2.engine.hive_nodes import default_nodes
        return default_nodes()

    def run(self, query: str) -> Dict[str, Any]:
        claims = self.clerk.decompose(query)
        debate = self._broadcast(query, claims)
        judgment = self.judge.synthesize(debate)
        self.crystallizer.crystallize(judgment)

        for claim_id in judgment.get("validated", []):
            match = next((c for c in claims if c.id == claim_id), None)
            if match:
                self.causal_memory.add(match.inversion_of or query, judgment["consensus_statement"], claim_id)

        output = {
            "query": query,
            "claims_total": len(claims),
            "validated": len(judgment.get("validated", [])),
            "rejected": len(judgment.get("rejected", [])),
            "inconclusive": len(judgment.get("inconclusive", [])),
            "anomaly_score": judgment.get("anomaly_score", 0.0),
            "breakthrough_potential": judgment.get("breakthrough_potential", "low"),
            "transcript_hash": judgment.get("transcript_hash", ""),
            "status": "ok" if claims else "failed",
            "message": "MoIE cycle completed with local deterministic nodes",
        }
        if self.persistence is not None:
            self.persistence.save_artifact("moie", f"{query[:50]}/result", output)
        return output

    def _broadcast(self, query: str, claims: List[Claim]) -> DebateRound:
        votes: List[tuple[str, str, str, float]] = []
        transcript: List[str] = [f"QUERY: {query}", f"CLAIMS: {len(claims)}"]
        for node in self.nodes:
            transcript.append(f"NODE:{node.role}")
            for claim in claims:
                stance, evidence, confidence = node.deliberate(claim, {"query": query})
                votes.append((claim.id, stance, evidence, confidence))
                transcript.append(f"  {claim.id}:{node.role}:{stance}:{confidence:.2f}::{evidence[:80]}")
        transcript_text = "\n".join(transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        return DebateRound(query=query, claims=claims, nodes=[n.role for n in self.nodes], votes=votes, transcript=transcript, transcript_hash=transcript_hash)
