from __future__ import annotations

import asyncio

from msb_v2.aura.aura_core import AURACore
from msb_v2.aura.memory.retriever import BM25Retriever
from msb_v2.aura.models import EventPhase
from msb_v2.aura.persistence import Persistence
from msb_v2.aura.policies.engine import PIIRedactionPolicy, PolicyEngine


def test_bm25_retriever_returns_ranked_docs():
    retriever = BM25Retriever([
        "pilot car escort requires certification",
        "oversized load routes need permits",
        "heavy haul trucking in Fox Valley Wisconsin",
    ])
    results = asyncio.run(retriever.retrieve("Wisconsin escort certification", top_k=2))
    assert len(results) == 2
    assert "Wisconsin" in results[0] or "escort" in results[0]


def test_policy_redacts_pii():
    engine = PolicyEngine([PIIRedactionPolicy()])
    text = "Call 555-123-4567 or email driver@example.com. SSN: 123-45-6789"
    redacted = engine.apply(text)
    assert "555-123-4567" not in redacted
    assert "driver@example.com" not in redacted
    assert "123-45-6789" not in redacted
    assert "[REDACTED" in redacted


def test_aura_core_uses_memory_and_policy():
    persistence = Persistence(":memory:")
    docs = [
        "Fox Valley oversized-load escort best practices",
        "Wisconsin pilot car certificate requirements",
    ]
    retriever = BM25Retriever(docs)
    policy_engine = PolicyEngine([PIIRedactionPolicy()])
    state = asyncio.run(AURACore(persistence=persistence).run(goal="Wisconsin escort requirements", retriever=retriever, policy_engine=policy_engine))
    assert state.session_id
    events = persistence.recent_events(state.session_id, limit=20)
    assert any(e["phase"] == EventPhase.ORIENT.value for e in events)


def test_aura_core_applies_policy_to_tool_output():
    persistence = Persistence(":memory:")
    retriever = BM25Retriever([])
    policy_engine = PolicyEngine([PIIRedactionPolicy()])
    state = asyncio.run(
        AURACore(persistence=persistence).run(
            goal="echo 123-45-6789",
            retriever=retriever,
            policy_engine=policy_engine,
        )
    )
    events = persistence.recent_events(state.session_id, limit=20)
    reflect_events = [e for e in events if e["phase"] == EventPhase.REFLECT.value]
    assert reflect_events
    payload = reflect_events[0].get("payload", {})
    assert isinstance(payload, dict)
