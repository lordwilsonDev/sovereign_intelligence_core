from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
_MOIE_ROOT = Path("/Users/lordwilson/msb-v2/.artifacts/moie")


class MoIESearchRequest(BaseModel):
    query: str
    top_k: int = 5


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "result"


def _store_artifact(slug: str, blob: Dict[str, Any]) -> str:
    _MOIE_ROOT.mkdir(parents=True, exist_ok=True)
    safe_slug = _slugify(slug)
    path = _MOIE_ROOT / f"{safe_slug}.json"
    path.write_text(json.dumps(blob, indent=2), encoding="utf-8")
    return safe_slug


def _load_artifact(slug: str) -> Optional[Dict[str, Any]]:
    if slug == "search":
        return None
    safe_slug = _slugify(slug)
    path = _MOIE_ROOT / f"{safe_slug}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


@router.post("/store")
def moie_slug_store(payload: Dict[str, Any]) -> Dict[str, Any]:
    slug = str(payload.get("slug") or payload.get("query") or "result")
    blob = {key: value for key, value in payload.items() if key != "slug"}
    safe_slug = _store_artifact(slug, blob)
    return {"status": "ok", "slug": safe_slug}


def _is_reserved_path(slug: str) -> bool:
    return slug in {"search", "store"}


@router.get("/{slug}")
def moie_slug_get(slug: str) -> Dict[str, Any]:
    if _is_reserved_path(slug):
        raise HTTPException(status_code=404, detail=f"MoIE route not found: {slug}")
    artifact = _load_artifact(slug)
    if artifact is None:
        raise HTTPException(status_code=404, detail=f"MoIE artifact not found: {slug}")
    return {"status": "ok", "slug": slug, "artifact": artifact}


@router.get("/{slug}/crystallization")
def moie_slug_crystallization(slug: str) -> Dict[str, Any]:
    if _is_reserved_path(slug):
        raise HTTPException(status_code=404, detail=f"MoIE route not found: {slug}")
    artifact = _load_artifact(slug)
    if artifact is None:
        raise HTTPException(status_code=404, detail=f"MoIE artifact not found: {slug}")
    import msb_v2.engine.crystallizer as crystallizer_module
    crystallizer = crystallizer_module.Crystallizer()
    crystal = crystallizer.crystallize(artifact)
    safe_slug = _slugify(slug)
    _store_artifact(f"{safe_slug}-crystallization", crystal)
    return {"status": "ok", "slug": slug, "crystallization": crystal}


@router.get("/search")
def moie_search(query: str, top_k: int = 5) -> Dict[str, Any]:
    artifacts = []
    for path in sorted(_MOIE_ROOT.glob("*.json")):
        try:
            artifacts.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    if not artifacts:
        return {"status": "ok", "matches": [], "query": query}
    query_terms = [term.lower() for term in query.split() if term]
    results = []
    for art in artifacts:
        text_blob = json.dumps(art).lower()
        score = sum(text_blob.count(term) for term in query_terms)
        if score > 0:
            results.append((score, art))
    results.sort(key=lambda item: item[0], reverse=True)
    return {
        "status": "ok",
        "query": query,
        "matches": [art for _, art in results[:top_k]],
        "total_artifacts": len(artifacts),
    }
