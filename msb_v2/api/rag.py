from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from msb_v2.api.middleware import require_bearer_token

from msb_v2.v3.contracts import HarnessContract
from msb_v2.v3.contracts import register as _register_contract
router = APIRouter()
_ARTIFACT_ROOT = Path("/Users/lordwilson/msb-v2/.artifacts/rag")
_QUERY_LOG_ROOT = Path("/Users/lordwilson/msb-v2/.artifacts/rag_queries")


class IngestRequest(BaseModel):
    texts: List[str]
    source: Optional[str] = None


class ConverseRequest(BaseModel):
    query: str
    top_k: int = 3


def _ensure_dirs() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=True)


def _bm25_match(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


@router.post("/ingest")
def rag_ingest(payload: IngestRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    _ensure_dirs()
    source = payload.source or "inline"
    stored: List[Dict[str, Any]] = []
    for idx, text in enumerate(payload.texts, start=1):
        doc_id = f"{int(time.time())}-{idx}"
        doc = {"id": doc_id, "source": source, "text": text, "ingested_at": time.time()}
        path = _ARTIFACT_ROOT / f"{doc_id}.json"
        path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
        stored.append(doc)
    return {"status": "ok", "ingested": len(stored), "documents": stored}


@router.post("/converse")
def rag_converse(payload: ConverseRequest, auth: Dict[str, Any] = Depends(require_bearer_token)) -> Dict[str, Any]:
    _ensure_dirs()
    documents: List[Dict[str, Any]] = []
    for path in sorted(_ARTIFACT_ROOT.glob("*.json")):
        try:
            documents.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    if not documents:
        return {"status": "ok", "matches": [], "query": payload.query, "note": "empty corpus"}
    matches = _bm25_match(payload.query, documents, payload.top_k)
    log = {
        "query": payload.query,
        "top_k": payload.top_k,
        "matches": len(matches),
        "ts": time.time(),
    }
    log_path = _QUERY_LOG_ROOT / f"{int(time.time())}.json"
    log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")
    return {"status": "ok", "query": payload.query, "matches": matches}
# HCL contract registration
_register_contract(HarnessContract(route="/rag/ingest", method="post", allow_anonymous=False))
_register_contract(HarnessContract(route="/rag/converse", method="post", allow_anonymous=False))
