from __future__ import annotations

import asyncio
from typing import Optional

from msb_v2.aura.aura_core import AURACore
from msb_v2.aura.models import State


from mutmut.mutation.trampoline import wrap_in_trampoline as _mutmut_mutated, MutantDict
mutants_x_run_aura__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_run_aura__mutmut)
async def run_aura(goal: str, session_id: Optional[str] = None) -> State:
    core = AURACore()
    return await core.run(goal=goal, session_id=session_id)


async def x_run_aura__mutmut_orig(goal: str, session_id: Optional[str] = None) -> State:
    core = AURACore()
    return await core.run(goal=goal, session_id=session_id)


async def x_run_aura__mutmut_1(goal: str, session_id: Optional[str] = None) -> State:
    core = None
    return await core.run(goal=goal, session_id=session_id)


async def x_run_aura__mutmut_2(goal: str, session_id: Optional[str] = None) -> State:
    core = AURACore()
    return await core.run(goal=None, session_id=session_id)


async def x_run_aura__mutmut_3(goal: str, session_id: Optional[str] = None) -> State:
    core = AURACore()
    return await core.run(goal=goal, session_id=None)


async def x_run_aura__mutmut_4(goal: str, session_id: Optional[str] = None) -> State:
    core = AURACore()
    return await core.run(session_id=session_id)


async def x_run_aura__mutmut_5(goal: str, session_id: Optional[str] = None) -> State:
    core = AURACore()
    return await core.run(goal=goal, )

mutants_x_run_aura__mutmut['_mutmut_orig'] = x_run_aura__mutmut_orig # type: ignore # mutmut generated
mutants_x_run_aura__mutmut['x_run_aura__mutmut_1'] = x_run_aura__mutmut_1 # type: ignore # mutmut generated
mutants_x_run_aura__mutmut['x_run_aura__mutmut_2'] = x_run_aura__mutmut_2 # type: ignore # mutmut generated
mutants_x_run_aura__mutmut['x_run_aura__mutmut_3'] = x_run_aura__mutmut_3 # type: ignore # mutmut generated
mutants_x_run_aura__mutmut['x_run_aura__mutmut_4'] = x_run_aura__mutmut_4 # type: ignore # mutmut generated
mutants_x_run_aura__mutmut['x_run_aura__mutmut_5'] = x_run_aura__mutmut_5 # type: ignore # mutmut generated
mutants_x_main__mutmut: MutantDict = {}  # type: ignore


@_mutmut_mutated(mutants_x_main__mutmut)
def main() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_orig() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_1() -> None:
    import sys
    goal = None
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_2() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) and "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_3() -> None:
    import sys
    goal = " ".join(None) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_4() -> None:
    import sys
    goal = "XX XX".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_5() -> None:
    import sys
    goal = " ".join(sys.argv[2:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_6() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "XXSay helloXX"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_7() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_8() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "SAY HELLO"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_9() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = None
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_10() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(None)
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_11() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(None))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_12() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print(None)


def x_main__mutmut_13() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"XXsession_idXX": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_14() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"SESSION_ID": state.session_id, "goal": state.current_goal, "step": state.step})


def x_main__mutmut_15() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "XXgoalXX": state.current_goal, "step": state.step})


def x_main__mutmut_16() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "GOAL": state.current_goal, "step": state.step})


def x_main__mutmut_17() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "XXstepXX": state.step})


def x_main__mutmut_18() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "STEP": state.step})

mutants_x_main__mutmut['_mutmut_orig'] = x_main__mutmut_orig # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_1'] = x_main__mutmut_1 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_2'] = x_main__mutmut_2 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_3'] = x_main__mutmut_3 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_4'] = x_main__mutmut_4 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_5'] = x_main__mutmut_5 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_6'] = x_main__mutmut_6 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_7'] = x_main__mutmut_7 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_8'] = x_main__mutmut_8 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_9'] = x_main__mutmut_9 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_10'] = x_main__mutmut_10 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_11'] = x_main__mutmut_11 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_12'] = x_main__mutmut_12 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_13'] = x_main__mutmut_13 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_14'] = x_main__mutmut_14 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_15'] = x_main__mutmut_15 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_16'] = x_main__mutmut_16 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_17'] = x_main__mutmut_17 # type: ignore # mutmut generated
mutants_x_main__mutmut['x_main__mutmut_18'] = x_main__mutmut_18 # type: ignore # mutmut generated
