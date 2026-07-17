from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from msb_v2.engine.causal_memory import CausalMemory
from msb_v2.engine.crystallizer import Crystallizer
from msb_v2.engine.hive_nodes import default_nodes
from msb_v2.engine.moie_judge import Judge
from msb_v2.engine.moie_orchestrator import MoIEOrchestrator
from msb_v2.engine.rcoh_persistence import RCOHPersistence

router = APIRouter()

_moie: MoIEOrchestrator | None = None


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x__get_moie__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x__get_moie__mutmut)
def _get_moie() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_orig() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_1() -> MoIEOrchestrator:
    global _moie
    if _moie is not None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_2() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = None
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_3() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = None
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_4() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = None
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_5() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=None)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_6() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = None
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_7() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=None)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_8() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = None
    return _moie


def x__get_moie__mutmut_9() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=None, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_10() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=None, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_11() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=None, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_12() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=None, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_13() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=None)
    return _moie


def x__get_moie__mutmut_14() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_15() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, persistence=persistence, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_16() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, causal_memory=causal_memory, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_17() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, nodes=default_nodes())
    return _moie


def x__get_moie__mutmut_18() -> MoIEOrchestrator:
    global _moie
    if _moie is None:
        persistence = RCOHPersistence()
        causal_memory = CausalMemory()
        judge = Judge(persistence=persistence)
        crystallizer = Crystallizer(persistence=persistence)
        _moie = MoIEOrchestrator(judge=judge, crystallizer=crystallizer, persistence=persistence, causal_memory=causal_memory, )
    return _moie

mutants_x__get_moie__mutmut['_mutmut_orig'] = x__get_moie__mutmut_orig # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_1'] = x__get_moie__mutmut_1 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_2'] = x__get_moie__mutmut_2 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_3'] = x__get_moie__mutmut_3 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_4'] = x__get_moie__mutmut_4 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_5'] = x__get_moie__mutmut_5 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_6'] = x__get_moie__mutmut_6 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_7'] = x__get_moie__mutmut_7 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_8'] = x__get_moie__mutmut_8 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_9'] = x__get_moie__mutmut_9 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_10'] = x__get_moie__mutmut_10 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_11'] = x__get_moie__mutmut_11 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_12'] = x__get_moie__mutmut_12 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_13'] = x__get_moie__mutmut_13 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_14'] = x__get_moie__mutmut_14 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_15'] = x__get_moie__mutmut_15 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_16'] = x__get_moie__mutmut_16 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_17'] = x__get_moie__mutmut_17 # type: ignore # mutmut generated
mutants_x__get_moie__mutmut['x__get_moie__mutmut_18'] = x__get_moie__mutmut_18 # type: ignore # mutmut generated


class QueryRequest(BaseModel):
    query: str


@router.post("/run")
def moie_run(payload: QueryRequest) -> dict[str, Any]:
    moie = _get_moie()
    result = moie.run(payload.query)
    result["status"] = "ok" if result.get("status") != "failed" else "failed"
    return result
