from __future__ import annotations

import asyncio
from typing import Optional

from msb_v2.aura.aura_core import AURACore
from msb_v2.aura.models import State


async def run_aura(goal: str, session_id: Optional[str] = None) -> State:
    core = AURACore()
    return await core.run(goal=goal, session_id=session_id)


def main() -> None:
    import sys
    goal = " ".join(sys.argv[1:]) or "Say hello"
    state = asyncio.run(run_aura(goal))
    print({"session_id": state.session_id, "goal": state.current_goal, "step": state.step})
