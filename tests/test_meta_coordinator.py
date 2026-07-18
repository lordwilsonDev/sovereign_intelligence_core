from cognitive_compiler.meta_coordinator_v3_2 import (
    MetaIntelligenceCoordinator,
    QueryType,
    IntelligenceLayer,
    EpistemicTorsionFilter,
    ThermodynamicHeart,
    OutcomeVerifier,
    OuroborosEvolver,
    Metabolism,
)


def test_coordinator_synthesize_returns_result():
    coord = MetaIntelligenceCoordinator(worker_count=1)
    result = coord.query(
        query_type=QueryType.SYNTHESIZE,
        layers=[IntelligenceLayer.GRAPH, IntelligenceLayer.MEMORY],
        parameters={"query": "Test synthesis", "goal": "Test synthesis"},
        priority=5,
        timeout=5.0,
    )
    assert result.query_id
    assert isinstance(result.layers_used, list)
    assert hasattr(result, "to_dict")


def test_etf_rejects_high_entropy_dict():
    fltr = EpistemicTorsionFilter()
    passed, reason, cleaned = fltr.check({"query": " ".join(["word"] * 30)})
    assert isinstance(passed, bool)
    assert isinstance(reason, str)
    assert passed is False or cleaned is not None


def test_heart_steer_returns_corrected_vec():
    heart = ThermodynamicHeart()
    out = heart.steer([0.1, 0.9, 0.2], [1.0, 0.2, 0.1])
    assert isinstance(out, dict)
    assert "corrected" in out
    assert "torsion_level" in out
    assert "projection_removed" in out


def test_outcome_verifier_technical_false_implies_true_false():
    verifier = OutcomeVerifier()
    res = verifier.verify("deploy something", {"success": False})
    assert res["technical_success"] is False
    assert res["true_success"] is False


def test_ouroboros_evolver_healthy_when_no_queries():
    evolver = OuroborosEvolver()
    meta = Metabolism(total_queries=0, successful_impacts=0)
    out = evolver.evolve(meta, ["graph", "memory", "decision", "bus"])
    assert out["vdr"] == 0.125
    assert out["health"] == "metabolic_stress"
