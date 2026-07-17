from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from msb_v2.engine.merkle_reasoning import MerkleReasoningChain

router = APIRouter()
_DREAMS_DIR = Path("/Users/lordwilson/msb-v2/.artifacts/dreams")


class DreamRequest(BaseModel):
    seed: str | None = None
    tags: list[str] | None = None


def _ensure_dir() -> None:
    _DREAMS_DIR.mkdir(parents=True, exist_ok=True)


def _store_dream(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _load_dream(dream_id: str) -> Dict[str, Any] | None:
    path = _DREAMS_DIR / f"{dream_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


@router.get("/ping")
def imagination_ping() -> dict:
    return {"status": "ok", "module": "imagination"}


@router.post("/dreams")
def imagination_dream(payload: DreamRequest) -> dict:
    seed = payload.seed or uuid.uuid4().hex
    chain = MerkleReasoningChain()
    chain.append("dream", {"seed": seed, "tags": payload.tags or []})
    dream = {
        "id": uuid.uuid4().hex,
        "seed": seed,
        "tags": payload.tags or [],
        "root": chain.root_hash(),
    }
    _store_dream(dream["id"], dream)
    return {"status": "ok", "dream": dream}


@router.get("/dreams/{dream_id}")
def imagination_dream_get(dream_id: str) -> dict:
    dream = _load_dream(dream_id)
    if dream is None:
        raise HTTPException(status_code=404, detail="dream not found")
    return {"status": "ok", "dream": dream}
