from __future__ import annotations

from typing import Any, Dict

from fastapi.testclient import TestClient

from msb_v2.api.main import create_app


client = TestClient(create_app())


def test_v2_live_endpoints_roundup() -> None:
    created = client.post("/imagination/dreams", json={"seed": "integration", "tags": ["axiom"]}).json()
    dream_id = created["dream"]["id"]
    paths = [
        ("/health", "get", None),
        ("/runtime/ping", "get", None),
        ("/cognitive/ping", "get", None),
        ("/cognitive/mesh/negotiate", "post", {"peers": ["alpha", "beta"]}),
        ("/cognitive/chronos/checkpoint", "post", {"label": "integration"}),
        ("/cognitive/provenance/build", "post", {}),
        ("/cognitive/redteam/run", "post", {}),
        ("/cognitive/semantic/snapshot", "post", {}),
        ("/cognitive/verification/merkle", "post", {"root": "0" * 64, "step_id": "s1", "step_type": "p", "payload": {}, "prev_hash": "0" * 64, "step_hash": "bad"}),
        ("/cognitive/semantic/drift", "post", {"expected": "sovereign stack", "actual": "pizza delivery"}),
        ("/eve/manifest", "get", None),
        ("/eve/schedules", "get", None),
        ("/rag/ingest", "post", {"texts": ["live corpus probe"], "source": "integration"}),
        ("/rag/converse", "post", {"query": "corpus probe", "top_k": 1}),
        ("/moie/slug/store", "post", {"slug": "integration", "query": "store test"}),
        (f"/imagination/dreams/{dream_id}", "get", None),
        ("/moie/slug/integration", "get", None),
        ("/moie/slug/integration/crystallization", "get", None),
        ("/moie/run", "post", {"query": "integration smoke test"}),
        ("/monitor/torsion/events", "post", None),
        ("/deepseek/chat", "post", {"goal": "ping", "messages": [{"role": "user", "content": "ping"}]}),
        ("/imagination/ping", "get", None),
    ]
    results: Dict[str, Any] = {}
    for path, method, payload in paths:
        try:
            if method == "post":
                resp = client.post(path, json=payload or {})
            else:
                resp = client.get(path)
            results[path] = resp.status_code
        except Exception as exc:
            results[path] = f"ERR:{exc}"
    failures = {path: code for path, code in results.items() if code != 200}
    assert not failures, failures


def test_moie_slug_search_and_store_round_trip() -> None:
    from msb_v2.api.moie_slug import moie_search, moie_slug_store
    store = moie_slug_store({"slug": "roundtrip", "query": "store test deep research"})
    assert store["status"] == "ok"
    matches = moie_search("deep research", top_k=1)
    assert matches["status"] == "ok"
    assert matches["matches"]