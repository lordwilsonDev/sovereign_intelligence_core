from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class DigitalTwin:
    twin_id: str
    name: str
    state: Dict[str, Any]
    snapshot_id: Optional[str] = None
    fork_of: Optional[str] = None


@dataclass
class DigitalTwinHook:
    def __init__(self) -> None:
        self._twins: Dict[str, DigitalTwin] = {}

    def create(self, name: str, state: Dict[str, Any], fork_of: Optional[str] = None) -> DigitalTwin:
        twin_id = f"twin-{name}-{len(self._twins) + 1}"
        twin = DigitalTwin(
            twin_id=twin_id,
            name=name,
            state=copy.deepcopy(state),
            fork_of=fork_of,
        )
        self._twins[twin_id] = twin
        return twin

    def snapshot(self, twin_id: str) -> Optional[DigitalTwin]:
        twin = self._twins.get(twin_id)
        if twin is None:
            return None
        snap = DigitalTwin(
            twin_id=f"{twin_id}-snap-{len(self._twins) + 1}",
            name=twin.name,
            state=copy.deepcopy(twin.state),
            snapshot_id=twin_id,
            fork_of=twin.fork_of,
        )
        self._twins[snap.twin_id] = snap
        return snap

    def evolve(self, twin_id: str, delta: Dict[str, Any]) -> Optional[DigitalTwin]:
        twin = self._twins.get(twin_id)
        if twin is None:
            return None
        new_state = copy.deepcopy(twin.state)
        new_state.update(delta)
        evolved = DigitalTwin(
            twin_id=f"{twin_id}-evolved-{len(self._twins) + 1}",
            name=twin.name,
            state=new_state,
            snapshot_id=twin_id,
            fork_of=twin.fork_of,
        )
        self._twins[evolved.twin_id] = evolved
        return evolved

    def get(self, twin_id: str) -> Optional[DigitalTwin]:
        return self._twins.get(twin_id)

    def summary(self) -> Dict[str, Any]:
        return {
            "count": len(self._twins),
            "twins": [t.__dict__ for t in self._twins.values()],
        }
