from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModelCapabilities:
    reasoning: bool = False
    extraction: bool = False
    classification: bool = False
    coding: bool = False
    cost_per_1k_tokens: float = 0.0


@dataclass
class RegisteredModel:
    name: str
    provider: str
    capabilities: ModelCapabilities
    max_tokens: int = 4096
    fallback: Optional[str] = None
    enabled: bool = True


class ModelRegistry:
    def __init__(self) -> None:
        self.models: Dict[str, RegisteredModel] = {}

    def register(self, model: RegisteredModel) -> None:
        self.models[model.name] = model

    def get(self, name: str) -> Optional[RegisteredModel]:
        return self.models.get(name)

    def available(self, capability: str) -> List[RegisteredModel]:
        return [m for m in self.models.values() if getattr(m.capabilities, capability, False) and m.enabled]


default_registry = ModelRegistry()
default_registry.register(RegisteredModel("claude", "anthropic", ModelCapabilities(reasoning=True, cost_per_1k_tokens=0.003), max_tokens=8192, fallback="deepseek"))
default_registry.register(RegisteredModel("deepseek", "deepseek", ModelCapabilities(reasoning=True, extraction=True, cost_per_1k_tokens=0.0005), max_tokens=8192, fallback="claude"))
default_registry.register(RegisteredModel("local", "local", ModelCapabilities(reasoning=True, classification=True, cost_per_1k_tokens=0.0), max_tokens=4096, fallback="claude"))
