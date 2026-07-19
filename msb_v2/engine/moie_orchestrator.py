from __future__ import annotations

import hashlib
from typing import Any, Dict, List, Sequence

from msb_v2.engine.moie_types import Claim, DebateRound, HiveMindNode
from msb_v2.engine.clerk import Clerk
from msb_v2.engine.moie_judge import Judge
from msb_v2.engine.crystallizer import Crystallizer
from msb_v2.engine.causal_memory import CausalMemory
from msb_v2.engine.rcoh_persistence import RCOHPersistence
from msb_v2.engine.observability import span


class DialecticDepthGauge:
    def __init__(self, min_rounds: int = 2, max_rounds: int = 5) -> None:
        self.min_rounds = min_rounds
        self.max_rounds = max_rounds

    def limit(self, transcript_len: int, node_count: int) -> int:
        lower = self.min_rounds * node_count
        upper = self.max_rounds * node_count
        return max(lower, min(transcript_len, upper))


class MoIEOrchestrator:
    "Clerk + broadcast debate + Judge + CausalMemory in one local workflow."

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
        self.depth_gauge = DialecticDepthGauge()

    @staticmethod
    def _default_nodes() -> List[HiveMindNode]:
        from msb_v2.engine.hive_nodes import default_nodes
        return default_nodes()

    @span("moie.run")
    def run(self, query: str) -> Dict[str, Any]:
        claims = self.clerk.decompose(query)
        debate = self._broadcast(query, claims)
        judgment = self.judge.synthesize(debate)
        self.crystallizer.crystallize(judgment)
        for claim_id in judgment.get("validated", []):
            match = next((c for c in claims if c.id == claim_id), None)
            if match:
                self.causal_memory.link(match.inversion_of or query, judgment["consensus_statement"], relation="validated::" + claim_id)
        output = {
            "query": query,
            "claims_total": len(claims),
            "validated": len(judgment.get("validated", [])),
            "rejected": len(judgment.get("rejected", [])),
            "inconclusive": len(judgment.get("inconclusive", [])),
            "anomaly_score": judgment.get("anomaly_score", 0.0),
            "breakthrough_potential": judgment.get("breakthrough_potential", "low"),
            "transcript_hash": judgment.get("transcript_hash", ""),
            "depth_rounds": len(debate.transcript) // max(1, len(self.nodes)),
            "status": "ok" if claims else "failed",
            "message": "MoIE cycle completed with local deterministic nodes",
        }
        if self.persistence is not None:
            self.persistence.save_artifact("moie", f"{query[:50]}/result", output)
        return output

    @span("moie.broadcast")
    def _broadcast(self, query: str, claims: List[Claim]) -> DebateRound:
        votes: List[tuple[str, str, str, float]] = []
        transcript: List[str] = [f"QUERY: {query}", f"CLAIMS: {len(claims)}"]
        max_entries = self.depth_gauge.limit(0, len(self.nodes))
        node_count = 0
        for node in self.nodes:
            transcript.append(f"NODE:{node.role}")
            node_count += 1
            for claim in claims:
                if len(transcript) >= max_entries:
                    break
                stance, evidence, confidence = node.deliberate(claim, {"query": query})
                votes.append((claim.id, stance, evidence, confidence))
                transcript.append(f"  {claim.id}:{node.role}:{stance}:{confidence:.2f}::{evidence[:80]}")
            if len(transcript) >= max_entries:
                break
        transcript_text = "\n".join(transcript)
        transcript_hash = "sha256:" + hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
        return DebateRound(query=query, claims=claims, nodes=[n.role for n in self.nodes], votes=votes, transcript=transcript, transcript_hash=transcript_hash)
