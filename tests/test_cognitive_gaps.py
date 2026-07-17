from __future__ import annotations

from typing import Any, Dict

from msb_v2.api.cognitive_verification import (
    MerkleVerifyRequest,
    SemanticDriftRequest,
    semantic_drift,
    verify_merkle,
)
from msb_v2.api.rag import rag_converse, rag_ingest
from msb_v2.api.moie_slug import moie_slug_get, moie_slug_store
from msb_v2.api.torsion import torsion_events


def test_merkle_verify_rejects_tampered_step() -> None:
    payload: Dict[str, Any] = verify_merkle(
        MerkleVerifyRequest(
            root="0" * 64,
            step_id="step-1",
            step_type="provenance",
            payload={"label": "test"},
            prev_hash="0" * 64,
            step_hash="badhash",
        )
    )
    assert payload["status"] == "ok"
    assert payload["result"]["valid"] is False


def test_semantic_drift_returns_drift_score() -> None:
    payload: Dict[str, Any] = semantic_drift(
        SemanticDriftRequest(
            expected="sovereign stack architecture",
            actual="completely unrelated sentence about pizza",
        )
    )
    assert "drift_score" in payload
    assert payload["status"] in {"ok", "watch", "drift"}


def test_rag_ingest_and_converse_round_trip() -> None:
    from msb_v2.api.rag import ConverseRequest, IngestRequest

    ingest: Dict[str, Any] = rag_ingest(IngestRequest(texts=["DeepSeek provenance log"], source="test"))
    assert ingest["ingested"] == 1
    converse: Dict[str, Any] = rag_converse(ConverseRequest(query="DeepSeek provenance", top_k=1))
    assert converse["matches"]


def test_moie_slug_store_and_get() -> None:
    store: Dict[str, Any] = moie_slug_store({"slug": "axiom-inversion", "query": "invert assumptions"})
    assert store["status"] == "ok"
    fetched: Dict[str, Any] = moie_slug_get(store["slug"])
    assert fetched["status"] == "ok"
    assert fetched["artifact"]["query"] == "invert assumptions"


def test_torsion_events_returns_empty_on_empty_history() -> None:
    payload: Dict[str, Any] = torsion_events()
    assert "events" in payload
    assert "deception_signals" in payload
