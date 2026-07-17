from __future__ import annotations

from msb_v2.engine.merkle_reasoning import MerkleReasoningChain


def test_merkle_reasoning_chain_grows_and_verifies() -> None:
    chain = MerkleReasoningChain()
    step = chain.append("observe", {"note": "initial"})
    assert step.step_id == "step-1"
    assert step.prev_hash == ""
    assert step.step_hash
    assert chain.root_hash() == step.step_hash
    two = chain.append("context", {"note": "next"})
    assert two.prev_hash == step.step_hash
    assert chain.verify() is True


def test_merkle_reasoning_snapshot_returns_stable_view() -> None:
    chain = MerkleReasoningChain()
    chain.append("provenance", {"source": "ledger"})
    snapshot = chain.snapshot("ingest-1")
    assert snapshot["label"] == "ingest-1"
    assert snapshot["len"] == 1
    assert len(snapshot["steps"]) == 1
