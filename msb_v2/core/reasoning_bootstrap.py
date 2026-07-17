from __future__ import annotations

from pathlib import Path

from msb_v2.core.evolution_memory import EvolutionMemory
from msb_v2.core.global_scheduler import GlobalScheduler


_DB_PATH = Path(__file__).resolve().parent.parent / "evaluation_memory.db"


def seed_demo_baseline() -> dict:
    memory = EvolutionMemory(str(_DB_PATH))
    scheduler = GlobalScheduler(memory)
    proposal = {
        "proposal_id": "startup-baseline",
        "module": "demo",
        "update_baseline": True,
    }
    return scheduler.execute_cycle(proposal, mode="operator")


def get_persistent_scheduler():
    memory = EvolutionMemory(str(_DB_PATH))
    return GlobalScheduler(memory)
