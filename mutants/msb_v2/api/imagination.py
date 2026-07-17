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


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict


class DreamRequest(BaseModel):
    seed: str | None = None
    tags: list[str] | None = None
mutants_x__ensure_dir__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__ensure_dir__mutmut)
def _ensure_dir() -> None:
    _DREAMS_DIR.mkdir(parents=True, exist_ok=True)


def x__ensure_dir__mutmut_orig() -> None:
    _DREAMS_DIR.mkdir(parents=True, exist_ok=True)


def x__ensure_dir__mutmut_1() -> None:
    _DREAMS_DIR.mkdir(parents=None, exist_ok=True)


def x__ensure_dir__mutmut_2() -> None:
    _DREAMS_DIR.mkdir(parents=True, exist_ok=None)


def x__ensure_dir__mutmut_3() -> None:
    _DREAMS_DIR.mkdir(exist_ok=True)


def x__ensure_dir__mutmut_4() -> None:
    _DREAMS_DIR.mkdir(parents=True, )


def x__ensure_dir__mutmut_5() -> None:
    _DREAMS_DIR.mkdir(parents=False, exist_ok=True)


def x__ensure_dir__mutmut_6() -> None:
    _DREAMS_DIR.mkdir(parents=True, exist_ok=False)

mutants_x__ensure_dir__mutmut['_mutmut_orig'] = x__ensure_dir__mutmut_orig # type: ignore # mutmut generated
mutants_x__ensure_dir__mutmut['x__ensure_dir__mutmut_1'] = x__ensure_dir__mutmut_1 # type: ignore # mutmut generated
mutants_x__ensure_dir__mutmut['x__ensure_dir__mutmut_2'] = x__ensure_dir__mutmut_2 # type: ignore # mutmut generated
mutants_x__ensure_dir__mutmut['x__ensure_dir__mutmut_3'] = x__ensure_dir__mutmut_3 # type: ignore # mutmut generated
mutants_x__ensure_dir__mutmut['x__ensure_dir__mutmut_4'] = x__ensure_dir__mutmut_4 # type: ignore # mutmut generated
mutants_x__ensure_dir__mutmut['x__ensure_dir__mutmut_5'] = x__ensure_dir__mutmut_5 # type: ignore # mutmut generated
mutants_x__ensure_dir__mutmut['x__ensure_dir__mutmut_6'] = x__ensure_dir__mutmut_6 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__store_dream__mutmut)
def _store_dream(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def x__store_dream__mutmut_orig(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def x__store_dream__mutmut_1(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = None
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def x__store_dream__mutmut_2(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR * f"{dream_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def x__store_dream__mutmut_3(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(None, encoding="utf-8")


def x__store_dream__mutmut_4(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding=None)


def x__store_dream__mutmut_5(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(encoding="utf-8")


def x__store_dream__mutmut_6(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(payload, indent=2), )


def x__store_dream__mutmut_7(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(None, indent=2), encoding="utf-8")


def x__store_dream__mutmut_8(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(payload, indent=None), encoding="utf-8")


def x__store_dream__mutmut_9(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(indent=2), encoding="utf-8")


def x__store_dream__mutmut_10(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(payload, ), encoding="utf-8")


def x__store_dream__mutmut_11(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(payload, indent=3), encoding="utf-8")


def x__store_dream__mutmut_12(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="XXutf-8XX")


def x__store_dream__mutmut_13(dream_id: str, payload: Dict[str, Any]) -> None:
    _ensure_dir()
    path = _DREAMS_DIR / f"{dream_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="UTF-8")

mutants_x__store_dream__mutmut['_mutmut_orig'] = x__store_dream__mutmut_orig # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_1'] = x__store_dream__mutmut_1 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_2'] = x__store_dream__mutmut_2 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_3'] = x__store_dream__mutmut_3 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_4'] = x__store_dream__mutmut_4 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_5'] = x__store_dream__mutmut_5 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_6'] = x__store_dream__mutmut_6 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_7'] = x__store_dream__mutmut_7 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_8'] = x__store_dream__mutmut_8 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_9'] = x__store_dream__mutmut_9 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_10'] = x__store_dream__mutmut_10 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_11'] = x__store_dream__mutmut_11 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_12'] = x__store_dream__mutmut_12 # type: ignore # mutmut generated
mutants_x__store_dream__mutmut['x__store_dream__mutmut_13'] = x__store_dream__mutmut_13 # type: ignore # mutmut generated
mutants_x__load_dream__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__load_dream__mutmut)
def _load_dream(dream_id: str) -> Dict[str, Any] | None:
    path = _DREAMS_DIR / f"{dream_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def x__load_dream__mutmut_orig(dream_id: str) -> Dict[str, Any] | None:
    path = _DREAMS_DIR / f"{dream_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def x__load_dream__mutmut_1(dream_id: str) -> Dict[str, Any] | None:
    path = None
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def x__load_dream__mutmut_2(dream_id: str) -> Dict[str, Any] | None:
    path = _DREAMS_DIR * f"{dream_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def x__load_dream__mutmut_3(dream_id: str) -> Dict[str, Any] | None:
    path = _DREAMS_DIR / f"{dream_id}.json"
    if path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def x__load_dream__mutmut_4(dream_id: str) -> Dict[str, Any] | None:
    path = _DREAMS_DIR / f"{dream_id}.json"
    if not path.exists():
        return None
    return json.loads(None)


def x__load_dream__mutmut_5(dream_id: str) -> Dict[str, Any] | None:
    path = _DREAMS_DIR / f"{dream_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding=None))


def x__load_dream__mutmut_6(dream_id: str) -> Dict[str, Any] | None:
    path = _DREAMS_DIR / f"{dream_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="XXutf-8XX"))


def x__load_dream__mutmut_7(dream_id: str) -> Dict[str, Any] | None:
    path = _DREAMS_DIR / f"{dream_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="UTF-8"))

mutants_x__load_dream__mutmut['_mutmut_orig'] = x__load_dream__mutmut_orig # type: ignore # mutmut generated
mutants_x__load_dream__mutmut['x__load_dream__mutmut_1'] = x__load_dream__mutmut_1 # type: ignore # mutmut generated
mutants_x__load_dream__mutmut['x__load_dream__mutmut_2'] = x__load_dream__mutmut_2 # type: ignore # mutmut generated
mutants_x__load_dream__mutmut['x__load_dream__mutmut_3'] = x__load_dream__mutmut_3 # type: ignore # mutmut generated
mutants_x__load_dream__mutmut['x__load_dream__mutmut_4'] = x__load_dream__mutmut_4 # type: ignore # mutmut generated
mutants_x__load_dream__mutmut['x__load_dream__mutmut_5'] = x__load_dream__mutmut_5 # type: ignore # mutmut generated
mutants_x__load_dream__mutmut['x__load_dream__mutmut_6'] = x__load_dream__mutmut_6 # type: ignore # mutmut generated
mutants_x__load_dream__mutmut['x__load_dream__mutmut_7'] = x__load_dream__mutmut_7 # type: ignore # mutmut generated


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
