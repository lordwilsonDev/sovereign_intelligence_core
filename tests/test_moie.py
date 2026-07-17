from __future__ import annotations

from msb_v2.engine.clerk import Clerk
from msb_v2.engine.moie_judge import Judge
from msb_v2.engine.moie_orchestrator import MoIEOrchestrator
from msb_v2.engine.moie_types import Claim, DebateRound
from msb_v2.engine.rcoh_persistence import RCOHPersistence


def test_clerk_decompose_returns_claims(tmp_path):
    import os
    os.environ.setdefault("RCOH_DB_PATH", str(tmp_path / "rcoh.db"))
    clerk = Clerk()
    claims = clerk.decompose("all data must live in cloud databases")
    assert 1 <= len(claims) <= 7
    assert all(isinstance(c, Claim) for c in claims)
    assert claims[0].source == "clerk"


def test_clerk_decompose_respects_max(tmp_path):
    import os
    os.environ.setdefault("RCOH_DB_PATH", str(tmp_path / "rcoh.db"))
    clerk = Clerk()
    claims = clerk.decompose("AI safety depends only on algorithmic transparency", max_claims=3)
    assert len(claims) <= 3


def test_judge_synthesizes_and_writes_manifest(tmp_path):
    import os
    os.environ.setdefault("RCOH_DB_PATH", str(tmp_path / "rcoh.db"))
    persistence = RCOHPersistence()
    judge = Judge(persistence=persistence)
    claims = [Claim(id="c01", text="invert X", source="clerk", scores={}, status="pending")]
    debate = DebateRound(
        query="invert X",
        claims=claims,
        nodes=["technical"],
        votes=[("c01", "support", "evidence", 0.9)],
        transcript=["technical:c01:support:0.90::evidence"],
        transcript_hash="sha256:abc",
    )
    judgment = judge.synthesize(debate)
    assert "transcript_hash" in judgment
    assert judgment["breakthrough_potential"] in {"low", "medium", "high"}
    assert len(judgment["validated"]) + len(judgment["rejected"]) + len(judgment["inconclusive"]) == len(claims)


def test_moie_round_trip_returns_contract():
    moie = MoIEOrchestrator()
    result = moie.run("micropayments for field inspections")
    assert result["claims_total"] >= 1
    assert "anomaly_score" in result
    assert "transcript_hash" in result
    assert result["status"] == "ok"
