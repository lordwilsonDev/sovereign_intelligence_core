from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
_ARTIFACT_ROOT = Path("/Users/lordwilson/msb-v2/.artifacts/rag")
_QUERY_LOG_ROOT = Path("/Users/lordwilson/msb-v2/.artifacts/rag_queries")


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class IngestRequest(BaseModel):
    texts: List[str]
    source: Optional[str] = None


class ConverseRequest(BaseModel):
    query: str
    top_k: int = 3
mutants_x__ensure_dirs__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__ensure_dirs__mutmut)
def _ensure_dirs() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=True)


def x__ensure_dirs__mutmut_orig() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=True)


def x__ensure_dirs__mutmut_1() -> None:
    _ARTIFACT_ROOT.mkdir(parents=None, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=True)


def x__ensure_dirs__mutmut_2() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=None)
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=True)


def x__ensure_dirs__mutmut_3() -> None:
    _ARTIFACT_ROOT.mkdir(exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=True)


def x__ensure_dirs__mutmut_4() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, )
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=True)


def x__ensure_dirs__mutmut_5() -> None:
    _ARTIFACT_ROOT.mkdir(parents=False, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=True)


def x__ensure_dirs__mutmut_6() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=False)
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=True)


def x__ensure_dirs__mutmut_7() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=None, exist_ok=True)


def x__ensure_dirs__mutmut_8() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=None)


def x__ensure_dirs__mutmut_9() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(exist_ok=True)


def x__ensure_dirs__mutmut_10() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=True, )


def x__ensure_dirs__mutmut_11() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=False, exist_ok=True)


def x__ensure_dirs__mutmut_12() -> None:
    _ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    _QUERY_LOG_ROOT.mkdir(parents=True, exist_ok=False)

mutants_x__ensure_dirs__mutmut['_mutmut_orig'] = x__ensure_dirs__mutmut_orig # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_1'] = x__ensure_dirs__mutmut_1 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_2'] = x__ensure_dirs__mutmut_2 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_3'] = x__ensure_dirs__mutmut_3 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_4'] = x__ensure_dirs__mutmut_4 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_5'] = x__ensure_dirs__mutmut_5 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_6'] = x__ensure_dirs__mutmut_6 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_7'] = x__ensure_dirs__mutmut_7 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_8'] = x__ensure_dirs__mutmut_8 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_9'] = x__ensure_dirs__mutmut_9 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_10'] = x__ensure_dirs__mutmut_10 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_11'] = x__ensure_dirs__mutmut_11 # type: ignore # mutmut generated
mutants_x__ensure_dirs__mutmut['x__ensure_dirs__mutmut_12'] = x__ensure_dirs__mutmut_12 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__bm25_match__mutmut)
def _bm25_match(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_orig(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_1(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = None
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_2(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.upper() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_3(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = None
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_4(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = None
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_5(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).upper()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_6(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(None).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_7(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get(None, "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_8(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", None)).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_9(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_10(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", )).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_11(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("XXtextXX", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_12(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("TEXT", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_13(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "XXXX")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_14(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = None
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_15(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(None)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_16(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(None) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_17(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append(None)
    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_18(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=None, reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_19(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=None)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_20(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_21(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], )
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_22(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: None, reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_23(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[1], reverse=True)
    return [doc for _, doc in scored[:top_k]]


def x__bm25_match__mutmut_24(query: str, documents: List[Dict[str, Any]], top_k: int) -> List[Dict[str, Any]]:
    query_terms = [term.lower() for term in query.split() if term]
    scored = []
    for doc in documents:
        text = str(doc.get("text", "")).lower()
        score = sum(text.count(term) for term in query_terms)
        scored.append((score, doc))
    scored.sort(key=lambda item: item[0], reverse=False)
    return [doc for _, doc in scored[:top_k]]

mutants_x__bm25_match__mutmut['_mutmut_orig'] = x__bm25_match__mutmut_orig # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_1'] = x__bm25_match__mutmut_1 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_2'] = x__bm25_match__mutmut_2 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_3'] = x__bm25_match__mutmut_3 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_4'] = x__bm25_match__mutmut_4 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_5'] = x__bm25_match__mutmut_5 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_6'] = x__bm25_match__mutmut_6 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_7'] = x__bm25_match__mutmut_7 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_8'] = x__bm25_match__mutmut_8 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_9'] = x__bm25_match__mutmut_9 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_10'] = x__bm25_match__mutmut_10 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_11'] = x__bm25_match__mutmut_11 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_12'] = x__bm25_match__mutmut_12 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_13'] = x__bm25_match__mutmut_13 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_14'] = x__bm25_match__mutmut_14 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_15'] = x__bm25_match__mutmut_15 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_16'] = x__bm25_match__mutmut_16 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_17'] = x__bm25_match__mutmut_17 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_18'] = x__bm25_match__mutmut_18 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_19'] = x__bm25_match__mutmut_19 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_20'] = x__bm25_match__mutmut_20 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_21'] = x__bm25_match__mutmut_21 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_22'] = x__bm25_match__mutmut_22 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_23'] = x__bm25_match__mutmut_23 # type: ignore # mutmut generated
mutants_x__bm25_match__mutmut['x__bm25_match__mutmut_24'] = x__bm25_match__mutmut_24 # type: ignore # mutmut generated


@router.post("/ingest")
def rag_ingest(payload: IngestRequest) -> Dict[str, Any]:
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
def rag_converse(payload: ConverseRequest) -> Dict[str, Any]:
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
