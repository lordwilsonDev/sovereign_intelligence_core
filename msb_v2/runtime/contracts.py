from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass(frozen=True)
class RuntimeContract:
    name: str
    version: str = "0.0.0"
    sha: str = ""
    initialize: Optional[Callable[[], None]] = None
    execute: Optional[Callable[..., Any]] = None
    validate: Optional[Callable[[], bool]] = None
    shutdown: Optional[Callable[[], None]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContractRegistry:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entries: Dict[str, RuntimeContract] = {}

    def register(self, contract: RuntimeContract) -> None:
        with self._lock:
            self._entries[contract.name] = contract

    def get(self, name: str) -> Optional[RuntimeContract]:
        return self._entries.get(name)

    def all(self) -> List[RuntimeContract]:
        return list(self._entries.values())

    def initialize_all(self) -> Dict[str, bool]:
        results = {}
        for name, contract in self._entries.items():
            try:
                if contract.initialize is not None:
                    contract.initialize()
                results[name] = True
            except Exception as exc:
                results[name] = False
        return results

    def shutdown_all(self) -> Dict[str, bool]:
        results = {}
        for name, contract in reversed(list(self._entries.items())):
            try:
                if contract.shutdown is not None:
                    contract.shutdown()
                results[name] = True
            except Exception as exc:
                results[name] = False
        return results


_registry = ContractRegistry()


def registry() -> ContractRegistry:
    return _registry
